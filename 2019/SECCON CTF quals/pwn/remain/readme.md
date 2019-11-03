# SECCON CTF - 2019

## pwn / 418 - remain

> sum.chal.seccon.jp 10001

### Solution

By [@kruztw](https://github.com/dreamisadream)

分析題目後發現沒有 show, 且 malloc 大小固定為 0x48, 看來又是一道偽造 chunk 修改 file structure 的題目.

而且題目限定只能 malloc 9 次, 但很佛心的在第 10 次幫你 free, 這似乎是在暗示我們要修改 free_hook, 而且出題者可能認為要解這題最少須 malloc 10 次 (最後一次 malloc 伴隨 free(推測用來寫 /bin/sh 用的)), 然而我只花了 8 次就搞定了 (自豪 ><)

這題的漏洞出現在 free 後沒設成 NULL, 導致 use after free 漏洞.

攻擊手法如下
1. 新增兩塊 chunks
2. free 掉這兩塊
3. 利用 tcache_dup 拿到 tcache_perthread_struct 靠近 tcache_bin 指標的 chunk
4. free chunk0
5. 修改 tcache_bin 拿到 tcache_perthread_struct 前面部份的 chunk, 並將屬於 unsorted bin 大小的位置填入 7
6. free chunk0
7. 修改 tcache_bin 拿到 chunk0 前面的 chunk, 利用此 chunk 修改 chunk0 的 header 為 0x91
8. free chunk0 （因為 5. 所以會被放到 unsorted bin)
9. free chunk1
10. 修改 tcache_bin 成 chunk0
11. 修改 chunk0 的 fd 為 _IO_2_1_stdout_
12. 拿到 stdout chunk, 修改 file structure (接著就拿到 libc 位址了)
13. free chunk0
14. 修改 tcache_bin 拿到 free_hook chunk
15. 修改 free_hook 為 system
16. 修改 chunk0 內容為 sh\x00
17. free(chunk0)

中間其實有很多檢查要繞過, 但礙於篇幅過長且難懂, 所以就省略了, 有興趣可以自己 trace 看看.

註:<br>
成功機率 1/256 
* 猜中 tcache_perthread_struct 位址 => 1/16
* 猜中 _IO_2_1_stdout_ 位址 => 1/16


