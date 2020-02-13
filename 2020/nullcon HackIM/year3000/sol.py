#!/usr/bin/env python3
from pwn import *
import base64

POS_ARCH = 0x4
POS_LEN = (0x661, 0x819)
POS_CHR = (0x668, 0x820)
POS_TRAIL = (0x1008, 0x1010)
TRAIL_LEN = (4, 8)

def solve_bin(n):
    print("Solving ...", n)
    with open('./bins/' + str(n) + '.bin', 'rb') as f:
        f.seek(0x4)
        arch = int.from_bytes(f.read(1), 'little') - 1
        f.seek(POS_LEN[arch])
        l = int.from_bytes(f.read(4), 'little')
        f.seek(POS_CHR[arch])
        c = f.read(1)
        f.seek(POS_TRAIL[arch])
        trail = f.read(TRAIL_LEN[arch])
    return c * l + trail

r = remote('re.ctf.nullcon.net', 1234)
while True:
    num = r.readline().strip()
    pos = num.find(b'.')
    if pos == -1:
        print(num)
        break
    num = int(num[:pos])
    r.sendlineafter(b'> ', base64.b64encode(solve_bin(num)))
    result = r.readline()
    if result[2] != ord('W'):
        print(result)
        break
