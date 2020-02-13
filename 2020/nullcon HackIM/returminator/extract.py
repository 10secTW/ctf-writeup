#!/usr/bin/env python3

o = [296, 272, 272, 272, 296, 360, 272, 424, 272, 208, 120, 120, 120, 96, 120, 120, 120, 120, 120, 120, 120, 208, 120, 120, 208, 208, 208, 208, 208, 272, 120, 208, 208]
r = [208, 225, 237, 20, 214, 183, 79, 105, 207, 217, 125, 66, 123, 104, 97, 99, 107 , 105, 109, 50, 48, 202, 111, 111, 29, 63, 223, 36, 0, 124, 100, 219, 32]
comments = {
    0x40119a: 'pop rdi; ret',
    0x40119c: 'pop rsi; ret',
    0x40119e: 'pop rdx; ret',
    0x4011a0: 'pop rcx; ret',
    0x4011a2: 'pop rax; ret',
    0x4011a4: 'add rax, rdi; ret',
    0x4011a8: 'add rax, rsi; ret',
    0x4011ac: 'add rax, rdx; ret',
    0x4011b0: 'add rax, rcx; ret',
    0x4011b4: 'add rax, rax; ret',
    0x4011b8: 'add rax, 0x1; ret',
    0x4011bd: 'xor rax, rax; ret',
    0x4011c1: 'sub rax, rdi; ret',
    0x4011c5: 'sub rax, rsi; ret',
    0x4011c9: 'sub rax, rdx; ret',
    0x4011cd: 'sub rax, rcx; ret',
    0x4011d1: 'sub rax, 0x1; ret',
    0x4011d6: 'movzx rdi, BYTE PTR[rdi]; ret',
    0x4011db: 'movzx rsi, BYTE PTR[rsi]; ret',
    0x4011e0: 'movzx rdx, BYTE PTR[rdx]; ret',
    0x4011e5: 'movzx rcx, BYTE PTR[rcx]; ret',
    0x4011ea: 'mov rdi, rax; ret',
    0x4011ee: 'mov rsi, rax; ret',
    0x4011f2: 'mov rdx, rax; ret',
    0x4011f6: 'mov rcx, rax; ret',
    0x4011fa: 'mov edi, 0; call 4010a0 <exit@plt>',
    0x4011ff: 'call 4010a0 <exit@plt>',
    0x4040a0: 'flag'
}

with open('blob', 'rb') as f:
    for c, offset in enumerate(o):
        data = f.read(offset)
        with open('payloads/' + str(c), 'w+') as o:
            for i in range(0, len(data), 8):
                val = int.from_bytes(data[i:i+8], 'little')
                if val == 0x6161616161616161:
                    continue
                o.write(hex(val))
                if val in comments:
                    o.write('\t|' + comments[val])
                o.write('\n')
            o.write('-----------------------\n')
            o.write('Out: ' + str(r[c]) + '\n')
