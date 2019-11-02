# Backdoor CTF - 2019

## pwn / 201 - babytcache

> At least let me free 7 tcaches.
> nc 51.158.118.84 17002 

### Solution

By [@kruztw](https://github.com/dreamisadream)

很一般的 heap 題, 漏洞也是常見的 use after free, 唯一難點在於只能 malloc 7 次 (因為 free 後沒清成 NULL), 此外題目限制 chunk 大小最多只能到 0x200, 且只能 free 5 次, 因此一般的作法是行不通的。
好在題目有提供 edit, 讓我們能修改 free chunk 的 fd
因此, 整體流程如下
1. free 掉兩塊 chunk
2. 部份修改 fd 指到 tcache_perthread_struct
3. 拿到該 chunk, 修改 tcache_bin 的數量為 7
4. free 掉 chunk , 並用 show 拿到 libc 位址
5. 修改 tcache_perthread_struct 的 tcache bin pointer 指到 __free_hook
6. malloc 拿到 __free_hook chunk 寫入 system
7. 修改某塊 chunk 的內容為 /bin/sh , 並 free 掉它

因為  __free_hook 被寫入 system 所以會執行 system('/bin/sh')

註：
成功機率 1/16