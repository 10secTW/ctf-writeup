# HITCON CTF Quals - 2019

## Crypto / 200 - Very Simple Haskell

>
> It can't be easier.
>
> [very_simple_haskell-787b99eed31be779ccfb7bd4f78b280387c173c4.tar.gz](./prob)
>
>
>
> Author: lyc
>
> 64 Teams solved.
>

### Solution

By [@oToToT](https://github.com/oToToT)

這是一題讀Haskell Code題目，感覺其實沒甚麼密碼學成分在內XD
因為我Haskell很爛，所以我是先努力翻成python之後才解的

下面擺個我翻譯出來Python Code
```python
from Crypto.Util.number import *
import functools

n = 134896036104102133446208954973118530800743044711419303630456535295204304771800100892609593430702833309387082353959992161865438523195671760946142657809228938824313865760630832980160727407084204864544706387890655083179518455155520501821681606874346463698215916627632418223019328444607858743434475109717014763667
k = 131
primes, p = [], 2
while len(primes) < k:
    if isPrime(p):
        primes.append(p)
    p += 1

def stringToInteger(s):
    r = 0
    for c in s:
        r = r * 256 + ord(c)
    return r
def numToBits(x):
    r = []
    while x > 0:
        r = [x&1] + r
        x >>= 1
    return r
def extendBits(blockLen, bits):
    return [0]*((blockLen-len(bits)%blockLen)%blockLen) + bits

def calc(num, arr):
    if not arr:
        return num
    num2 = num * num % n
    block, restArr = arr[:k], arr[k:]
    mul = functools.reduce(lambda x,y: x*y, map(lambda x: x[0]*x[1]%n if x[0]!=0 else 1, zip(block, primes)))
    return calc(mul*num2%n, restArr)

def magic(s):
    num = stringToInteger(s)
    bits = numToBits(num)
    extended = extendBits(8, bits)
    extended.reverse()
    oriLen = len(extended)
    extendedBits = extendBits(k, extended)
    oriLenBits = numToBits(oriLen)
    extendedOriLenBits = extendBits(k, oriLenBits)
    finalBits = extendedOriLenBits + extendedBits
    finalBits.reverse()
    return calc(1, finalBits)

if __name__ == '__main__':
    flag = open('flag').read()
    print(len(flag))
    print(magic("the flag is hitcon{%s}"%flag))
```

稍微印點東西出來後發現他是計算
![$70998196091606985545993711787111356453960854621421971918477501437269263801218145273626982609030910240112248874611888516366214608505^4 \cdot x^2 \cdot 3553\bmod{134896036104102133446208954973118530800743044711419303630456535295204304771800100892609593430702833309387082353959992161865438523195671760946142657809228938824313865760630832980160727407084204864544706387890655083179518455155520501821681606874346463698215916627632418223019328444607858743434475109717014763667}$](https://latex.codecogs.com/svg.latex?70998196091606985545993711787111356453960854621421971918477501437269263801218145273626982609030910240112248874611888516366214608505^4%20\cdot%20x^2%20\cdot%203553\bmod{134896036104102133446208954973118530800743044711419303630456535295204304771800100892609593430702833309387082353959992161865438523195671760946142657809228938824313865760630832980160727407084204864544706387890655083179518455155520501821681606874346463698215916627632418223019328444607858743434475109717014763667})
其中![$x$](https://latex.codecogs.com/svg.latex?x)是根據flag不同而有所不同的東西

因為模的數跟前![$k$](https://latex.codecogs.com/svg.latex?k)個質數都互質，所以逆元必定存在，然後就知道![$x^2\equiv 7408044823834091445627740990217334429796080152087544113221510708319937062359606887419717571527922650647181489064390504405177358050423185864015397222739025$](https://latex.codecogs.com/svg.latex?x^2\equiv%207408044823834091445627740990217334429796080152087544113221510708319937062359606887419717571527922650647181489064390504405177358050423185864015397222739025)

原本想說![$n$](https://latex.codecogs.com/svg.latex?n)不是質數，原根也不一定存在，不知道怎麼做，後來大膽的把根號開下去後發現居然開得動，所以就做完了XD

附上最後把它換成string的code
```python
from Crypto.Util.number import *

def bitsToString(bits):
    s = ''
    for i in range(0, len(bits), 8):
        c = 0
        for j in range(8):
            c = c * 2 + bits[i+j]
        s += chr(c)
    return s

primes, p = [], 2
while len(primes) < 131:
    if isPrime(p):
        primes.append(p)
    p += 1

wtf = 86069999557535094979972980224444072409353136887603982605698150750263262001655

result = []
for p in primes:
    if wtf % p == 0:
        result.append(1)
        wtf //= p
    else:
        result.append(0)

print('hitcon{'+bitsToString(result[21:69])+'}')
```
