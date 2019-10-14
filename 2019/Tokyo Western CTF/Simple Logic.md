# Tokyo Western CTF - 2019

## Crypto / 50 - Simple Logic

### Solution

By [@Bandit](https://github.com/rex978956)
Credits to [@ScottChen](https://github.com/scott987)

> Simple cipher is always strong.
> [color=#33ccff]
```ruby=
require 'securerandom'
require 'openssl'

ROUNDS = 765
BITS = 128
PAIRS = 6

def encrypt(msg, key)
    enc = msg
    mask = (1 << BITS) - 1
    ROUNDS.times do
        enc = (enc + key) & mask
        enc = enc ^ key
    end
    enc
end

def decrypt(msg, key)
    enc = msg
    mask = (1 << BITS) - 1
    ROUNDS.times do
        enc = enc ^ key
        enc = (enc - key) & mask
    end
    enc
end

fail unless BITS % 8 == 0

flag = SecureRandom.bytes(BITS / 8).unpack1('H*').to_i(16)
key = SecureRandom.bytes(BITS / 8).unpack1('H*').to_i(16)

STDERR.puts "The flag: TWCTF{%x}" % flag
STDERR.puts "Key=%x" % key
STDOUT.puts "Encrypted flag: %x" % encrypt(flag, key)
fail unless decrypt(encrypt(flag, key), key) == flag # Decryption Check

PAIRS.times do |i|
    plain = SecureRandom.bytes(BITS / 8).unpack1('H*').to_i(16)
    enc = encrypt(plain, key)
    STDOUT.puts "Pair %d: plain=%x enc=%x" % [-~i, plain, enc]
end
```

### Solution
Decrypt method use xor and addition, so we need to think about carry. 
We can use brute-force to calculate the key from low digit to high digit with six pairs of plain text and encrypted text:
```python=
p=[0x29abc13947b5373b86a1dc1d423807a,0xeeb83b72d3336a80a853bf9c61d6f254,
0x7a0e5ffc7208f978b81475201fbeb3a0,0xc464714f5cdce458f32608f8b5e2002e,
0xf944aaccf6779a65e8ba74795da3c41d,0x552682756304d662fa18e624b09b2ac5]


e=[0xb36b6b62a7e685bd1158744662c5d04a,0x614d86b5b6653cdc8f33368c41e99254,
0x292a7ff7f12b4e21db00e593246be5a0,0x64f930da37d494c634fa22a609342ffe,
0xaa3825e62d053fb0eb8e7e2621dabfe7,0xf2ffdf4beb933681844c70190ecf60bf]

key=[]

def encrypt(msg, key, bits):
    enc = msg
    mask = (1 << bits) - 1
    for _ in range(765):
        enc = (enc + key) & mask
        enc = enc ^ key
    return enc

for i in range(2,129):
    key.insert(0,"1")
    for j in range(6):
        # think about carry
        if encrypt((p[j]&((1<<i)-1)),int("".join(key),2),i)!=(e[j]&((1<<i)-1)):
            key[1]="0"
            if encrypt((p[j]&((1<<i)-1)),int("".join(key),2),i)!=(e[j]&((1<<i)-1)):
                key[1]="1"
                key[0]="0"
                if encrypt((p[j]&((1<<i)-1)),int("".join(key),2),i)!=(e[j]&((1<<i)-1)):
                    key[1]="0"
                    if encrypt((p[j]&((1<<i)-1)),int("".join(key),2),i)!=(e[j]&((1<<i)-1)):
                        print("SHIT!!!!") # Can't find the key, just a shit problem
                        exit(1)
print(hex(int("".join(key),2)))
```

### Flag
```TWCTF{ade4850ad48b8d21fa7dae86b842466d}```
