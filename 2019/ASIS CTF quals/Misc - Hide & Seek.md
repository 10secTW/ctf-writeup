# ASIS CTF Quals - 2019
###### Contributed by <`FI`>


## Hide & Seek - Points 227 / Misc

Description:
Chaos is a ladder for those who can put its steps in the right order and climb it to see the whole picture!
![](https://i.imgur.com/tWp35vP.png)

### Solution
First I use zsteg to check if there where some hidden stuff.
```
$ zsteg flag.png
```
It replies
```
[?] 36245 bytes of extra data after zlib stream
extradata:0         .. file: zlib compressed data
    00000000: 78 01 ec d3 03 73 a4 41  00 84 e1 8e 93 45 c7 b6  |x....s.A.....E..|
    00000010: 6d db b6 6d db b6 9d b3  6d fc ca fb 36 ce 9e ad  |m..m....m...6...|
...
```
It's a bit strange that it report zlib data as extradata since it's usually part of the PNG.
I extract it and decompress it.
```
$ zsteg flag.png -e extradata:0 | zlib-flate -uncompress
```
But sadly there's nothing, and it looks like the normal zlib data in a PNG file.

Then I started to check where these zlib data where in the original file and found out that these where the IDAT chunks except the first IDAT chunk.
So I cut off the IDAT chunks from the original file except the first chunk to see if the picture breaks.
```=bash
$ dd count=6217 if=flag.png of=f0.png bs=1
```
And it doesn't, it looks just like the original file.
Next, I cut off the head of the PNG and append with the rest of IDAT chunks
```=bash
$ dd count=1081 if=flag.png of=f1.png bs=1    
$ dd skip=6217 if=flag.png of=f1.png bs=1 oflag=append conv=notrunc
```
and voila
![](https://i.imgur.com/RSKKpr8.png)
part of the flag pops out

It's clear now that the rest of the IDAT chunks include the rest of the flag, so I wrote a script.
```=python3
#!/usr/bin/env python3
import binascii

f = open('flag.png', 'rb')

PNG = f.read()
IEND = PNG[-12:]    # PNG's IEND
PNG = PNG[:-12]     # cut it off
IDAT = PNG.split(b'IDAT')    # use IDAT to split IDAT block

for i in range(len(IDAT)-1):
    IDAT[i+1] = IDAT[i][-4:] + b'IDAT' + IDAT[i+1]    # restore IDAT's length info
    IDAT[i] = IDAT[i][:-4]                            # cut off the length info from the previous part

head = IDAT[0]    # PNG's head
IDAT = IDAT[1:]   # cut it off

for chunk in IDAT:
    out = head + chunk + IEND                 # reconstruct the PNG 
    fname = binascii.hexlify(chunk[11:14])    # make file name
    f = open(fname+'.png', 'wb')              # write out
    f.write(out)
```
Here's the result.
![](https://i.imgur.com/9vZ2aZQ.png)
![](https://i.imgur.com/n9FowA5.png)
![](https://i.imgur.com/YwkpyIq.png)
![](https://i.imgur.com/MTxq2Kc.png)
![](https://i.imgur.com/6t1gljr.png)
![](https://i.imgur.com/jgPMTL1.png)
![](https://i.imgur.com/6XpTSqy.png)
#### flag
`ASIS{f1Nd_fl49_bY__53aRcH1n9__ID47_By_N0}`

