# SECCON CTF - 2019

## pwn / 264 - one

> Host : one.chal.seccon.jp Port : 18357

### Solution

By [@kruztw](https://github.com/dreamisadream)

題目給了三個函數
* add : 新增大小為 0x40 的 chunk
* show : 印出 chunk 的內容
* delete : free 掉 chunk

而這題的漏洞在於 free 掉 chunk 後沒清成 NULL 導致 use after free, 且這題的 libc 版本為 2.27, 這個版本的 tcache 不會檢查 double free. 因此我們可以透過 tcache_dup 拿到任意位址的 chunk. 但在此之前, 我們要先有 libc 的位址, 由於 chunk 大小被限制在 0x40 (屬於 fastbin), 我們必須偽造一塊屬於 unsorted bin 的 chunk, 並透過 tcache_dup 拿到該 chunk, 再瘋狂 free 直到該 chunk 被放入 unsorted bin , 接著再用 show 來 leak 出 libc 的位址, 有了 libc 位址後我們就能再次透過 tcache_dup 拿到包含 free_hook 位址的 chunk, 並在 free_hook 寫入 one_gadget, 最後觸發 free 拿到 shell.