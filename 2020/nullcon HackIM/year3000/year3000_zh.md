# nullcon HackIM 2020

## re / 176 - year3000

### Solution

By [@jaidTw](https://github.com/jaidTw)

題目解壓縮後共有3000個執行檔，一部分是32-bit ELF，另一部份是64-bit的，隨便看幾個後會發現每個binary幾乎都長得一樣，讀取輸入進行一段簡單的檢查。

```c
int check(char *buf) {
  int passed = 1;
  for ( int i = 0; i < 83; ++i ) {
    if ( buf[i] != 'N' ) {
      passed = 0;
      break;
    }
  }
  if ( memcmp(buf + 83, &unk_201010, 8uLL) )
    passed = 0;
  return passed;
}
```
檢查格式固定是某字元重複N次再加上一串結尾，不同執行檔的差別只在於檢查的function中，所檢查的字元和長度及結尾會不同，而這些值及結尾的offset在binary中是固定的，可以簡單地被讀取出來。

試著連上題目，會給予檔案的名稱，並要求輸入，且輸入必須以base64編碼，因此推測應該是要根據檔案給出能夠pass的輸入。只要把流程自動化即可。

[sol.py](./sol.py)
