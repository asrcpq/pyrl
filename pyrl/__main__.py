from pyrl import readline
import sys, subprocess
import time

# this is just a workaround of rlwrap
# terminal sucks, we will not working on this framework
p = subprocess.Popen(sys.argv[1], stdin = subprocess.PIPE)
while True:
	cmd = readline(0)
	print("get cmd:", cmd, file = sys.stderr)
	p.stdin.write(cmd.encode() + b"\n")
	p.stdin.flush()
	time.sleep(1)
