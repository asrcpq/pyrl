from pyrl import readline
import sys

while True:
	print("[32mhi> [0m", end = "")
	cmd = readline(4)
	print()
	print("get command", cmd)
	if cmd == "exit" or not cmd:
		sys.exit(0)
