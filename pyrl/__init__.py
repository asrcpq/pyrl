import sys, termios, tty

def pr(s):
	print(s, end = "")

s = 0
cur = 0
history = []
result = ""

def move(o):
	global cur
	if o > 0:
		cur += o
		pr(f"[{o}C")
	elif o < 0:
		o = -o
		cur -= o
		pr(f"[{o}D")

def clear():
	global cur, result
	move(-cur)
	result = ""

def print_cursor_right():
	global cur, result
	pr("[0K")
	pr(result[cur:])
	moveback = len(result) - cur
	if moveback > 0:
		pr(f"[{moveback}D")

def proc(d):
	global s, cur, result
	if s == 1:
		if d == "[":
			s = 2
		else:
			s = 0
		return
	if s == 2:
		if d == "C":
			if cur < len(result):
				move(1)
		if d == "D":
			if cur > 0:
				move(-1)
		s = 0
		return
	if d == "\x03":
		raise KeyboardInterrupt
	if d == "\x04":
		raise EOFError
	if d == "\x10":
		clear()
		result = history[-1]
		pr(result)
		cur = len(result)
		return
	if not d:
		print("ERROR: read empty", file = sys.stderr)
		return
	if d[0] == "":
		s = 1
		return
	if d == "\x7f":
		if cur > 0:
			result = result[0:cur - 1] + result[cur:]
			cur -= 1
			pr("[D")
		else:
			return
	else:
		result = result[0:cur] + d + result[cur:]
		pr(d)
		cur += 1
	print_cursor_right()

def readline(offset):
	fd = sys.stdin.fileno()
	global s, cur, result, history
	s = 0
	cur = 0
	result = ""
	restore = termios.tcgetattr(fd)
	try: 
		tty.setraw(sys.stdin.fileno())
		sys.stdin.flush()
		while True:
			sys.stdout.flush()
			d = sys.stdin.read(1)
			if d == "\r":
				break
			# print(repr(d), file = sys.stderr)
			proc(d)
	finally:
		termios.tcsetattr(fd, termios.TCSADRAIN, restore)
	print()
	history.append(result)
	return result
