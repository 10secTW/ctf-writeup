# Backdoor CTF - 2019

## pwn / 286 - babyheap

> Just another babyheap challenge.
> nc 51.158.118.84 17001

### Solution

By [@kruztw](https://github.com/dreamisadream)

這題和 baby_tcache 一樣有 use after free 的漏洞, 差別在這題用 libc-2.23 沒有 tcache, 而且也沒有 show 的功能, 好在 got 可改 !?
好...其實我沒注意到, 所以修改 stdout 的 file structure, 如果你對 file structure 感到陌生, 可以去看看別人的 writeup , 或是自己嘗試將 atoi 的 got 改成 printf 的 plt ( 話說這題連 PIE 都沒開, 難怪這麼多人解 = = )

回到正題, 有解這題的人都知道, 不管多小的 chunk 都會被放進 unsorted bin, 這是因為程式中有 `mallopt(1,0)`, 它會將 global_max_fast 設成 0x10, 為了要 fastbin dup 我們得修改 global_max_fast 的值, 好在 edit 的功能沒被拔掉, 透過修改 unsorted bin 的 bk, 就能利用 unsorted bin attack 將 global_max_fast 修改成很大的值, 接著我們把 unsorted bin size 的 chunk free 掉, 再部份修改 fd 拿到 _IO_2_1_stdout_ 附近的 chunk, 修改 stdout 的 file structure 就能 leak 出 libc 位址, 接著再用 fastbin dup 拿到 malloc_hook 附近的 chunk, 並修改 malloc_hook 成 one_shot, 觸發 malloc 就能 get shell .

註:
成功機率 1/16

