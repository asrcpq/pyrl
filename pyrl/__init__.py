import sys, termios, tty

def pr(s):
	print(s, end = "")

s = 0
cur = 0
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
				cur += 1
				pr("[C")
		if d == "D":
			if cur > 0:
				cur -= 1
				pr("[D")
		s = 0
		return
	if d == "\x03":
		raise KeyboardInterrupt
	if d == "\x04":
		raise EOFError
	if not d:
		print("ERROR: read empty", file = sys.stderr)
		return
	if d[0] == "":
		s = 1
		return
	if d == "\x7f":
		if result:
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
	global s, cur, result
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
	return result
