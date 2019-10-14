#!/usr/bin/env python3

from pwn import *
import subprocess

r = remote("3.115.122.69", 30261)

r.recvline()
h = r.recvline().split()[-1]
print("Computing PoW...")
out = subprocess.check_output(["hashcash", "-mb25", h])
r.send(out)

with open('sol.evm', 'rb') as f:
    b = f.read()

print("Len :", len(b))
r.sendline(str(len(b)))
r.send(b)
r.interactive()
