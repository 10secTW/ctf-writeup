# HITCON CTF Quals - 2019

## Pwn / 234 - Trick or Treat

> Trick or Treat !!
>
> Author: Angelboy
> 
> 40 Teams solved.

### Solution

By [@kruztw](https://github.com/dreamisadream)

```clike=
void main()
{
    size = 0;
    Offsett = 0;
    value = 0;
    heap_addr = NULL;
    setvbuf(stdin, 0, 2, 0);
    setvbuf(stdout, 0, 2, 0);
    write(1, "Size:", 5);
    scanf("%lu", &size);
    heap_addr = malloc(size);
    if (heap_addr) {
        printf("Magic:%p\n",heap_addr);
        for(int i = 0; i<2; i++){
            write(1,"Offset & Value:",0x10);
            scanf("%lx %lx", &offset, &value);
            heap_addr[offset] = value;
        }
    }
    _exit(0);
}
```

程式流程很簡單, 使用者首先可以 malloc 任意大小的 chunk, 如果 malloc 成功就回傳 chunk 的位址, 接著, 使用者可以任意修改兩個位址的值, 但這位址是相對於 chunk 的位址。

一般來說, malloc 都是從 heap 切, 只有當 malloc 過大 (例如超過 top chunk size) 的 chunk 才會另外 mmap 一塊空間 (如圖所示)

![](https://i.imgur.com/wjZAHUp.png)

透過這個位址, 我們就能計算出 libc_base, 進而修改 free_hook 或 malloc_hook。
但程式看過去似乎沒有 free 和 malloc (如果不算一開始的 malloc 的話), 這樣修改 hook 有什麼用呢？
事實上, printf 和 scanf 在輸入字串過大時會觸發 malloc 來存字串
```clike=
 if (width >= sizeof (work_buffer) / sizeof (work_buffer[0]) - 32)
   {
     /* We have to use a special buffer.  The "32" is just a safe
        bet for all the output which is not counted in the width.  */
     size_t needed = ((size_t) width + 32) * sizeof (CHAR_T);
     if (__libc_use_alloca (needed))
       workend = (CHAR_T *) alloca (needed) + width + 32;
     else
       {
         workstart = (CHAR_T *) malloc (needed);
            ...
       }
```

因此如果我們將 malloc_hook 寫入 one_gadget 就有機會拿到 shell, 但不幸的是, 不論 malloc_hook 或 free_hook 都沒辦法滿足 constraints, 因此改朝 system 發展。
由於 malloc 多半會伴隨 free, 而且這裡的 free 是 free 掉剛剛 malloc 存放字串的 chunk, 如果我們將字串寫入 /bin/sh 並調用 free (此時 free_hook 已寫入 system 的位址), 則會執行 system("/bin/sh"), 然而這樣做是不行的, 因為 %lx 只吃 0-9 a-f 的字元。
好啦, 看來這題已從 pwn 轉為 misc 了 , 剩下的就是想辦法用 0-9 a-f 構成的指令拿到 shell。
經過隊友大大們的幫助, 發現可用 ed, 在 ed 輸入 !ls 能執行 shell 命令(ls), 因此輸入 !sh 就能成功拿到 shell。