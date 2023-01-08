import sys, termios, tty

def pr(s):
	print(s, end = "")

def readline(offset):
	fd = sys.stdin.fileno()
	result = ""
	state = 0
	cur = 0
	restore = termios.tcgetattr(fd)
	try: 
		tty.setraw(sys.stdin.fileno())
		sys.stdin.flush()
		while True:
			sys.stdout.flush()
			d = sys.stdin.read(1)
			# print(repr(d), file = sys.stderr)
			if state == 1:
				if d == "[":
					state = 2
				else:
					state = 0
				continue
			if state == 2:
				if d == "C":
					if cur < len(result):
						cur += 1
						pr("[C")
				if d == "D":
					if cur > 0:
						cur -= 1
						pr("[D")
				state = 0
				continue
			if d == "\x03":
				raise KeyboardInterrupt
			if d == "\x04":
				raise EOFError
			if d == "\r":
				break
			if d == "\x7f":
				if result:
					result = result[0:cur - 1] + result[cur:]
					cur -= 1
					pr("[D [D")
				continue
			if not d:
				print("ERROR: read empty", file = sys.stderr)
				continue
			if d[0] == "":
				state = 1
				continue
			result = result[0:cur] + d + result[cur:]
			pr("[0K")
			pr(result[cur:])
			cur += 1
			moveback = len(result) - cur
			if moveback > 0:
				pr(f"[{moveback}D")
	finally:
		termios.tcsetattr(fd, termios.TCSADRAIN, restore)
	print()
	return result
