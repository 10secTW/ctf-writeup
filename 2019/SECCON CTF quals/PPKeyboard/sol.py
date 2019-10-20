
with open('dump', 'r') as f:
    data = f.read()

output = ""

for p in data.split():
    p = p[-2:] + p[-4:-2] + p[-6:-4] + p[-8:-6]
    i = int(p, 16) >> 8
    if i >= 0x7F0000:
        if (i & 0xFF) == 0x97:
            output += " 0x%x" % (((i & 0xFFF) - 0x97) >> 8)
        elif (i & 0xFF) == 0x99:
            output += "%x" % (((i & 0xFFF) - 0x99) >> 8)

print("".join([chr(int(c, 16)) for c in output.split()]))

