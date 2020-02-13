# nullcon HackIM 2020

## pwn / 100 - meek boi

### Solution

By [@jaidTw](https://github.com/jaidTw)

This challenges accepts some shellcode, then it will fork a child to execute it, but `stdin`, `stdout`, `stderr` are all redirect to `/dev/null` so it looks like we have no input and output. 
Actually there are no any seccomp constraints, just open a socket connect to my machine and spawn a reverse shell, that's all.

[sol.py](./sol.py)
