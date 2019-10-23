# SECCON CTF Quals - 2019

## Pwn / 332 - lazy
> ```
> lazy.chal.seccon.jp 33333
> ```
### solution

這題並沒有給binary，首先連上題目
```
1: Public contents
2: Login
3: Exit
```
接著使用功能1
```
Welcome to public directory
You can download contents in this directory
diary_4.txt
diary_3.txt
diary_1.txt
login_source.c
diary_2.txt
```
發現可以下載login_source.c，裡面只有兩個function的`login`和`input`的source code
```c
#define BUFFER_LENGTH 32
#define PASSWORD "XXXXXXXXXX"
#define USERNAME "XXXXXXXX"

int login(void){
        char username[BUFFER_LENGTH];
        char password[BUFFER_LENGTH];
        char input_username[BUFFER_LENGTH];
        char input_password[BUFFER_LENGTH];

        memset(username,0x0,BUFFER_LENGTH);
        memset(password,0x0,BUFFER_LENGTH);
        memset(input_username,0x0,BUFFER_LENGTH);
        memset(input_password,0x0,BUFFER_LENGTH);

        strcpy(username,USERNAME);
        strcpy(password,PASSWORD);

        printf("username : ");
        input(input_username);
        printf("Welcome, %s\n",input_username);

        printf("password : ");
        input(input_password);


        if(strncmp(username,input_username,strlen(USERNAME)) != 0){
                puts("Invalid username");
                return 0;
        }

        if(strncmp(password,input_password,strlen(PASSWORD)) != 0){
                puts("Invalid password");
                return 0;
        }

        return 1;
}


void input(char *buf){
        int recv;
        int i = 0;
        while(1){
                recv = (int)read(STDIN_FILENO,&buf[i],1);
                if(recv == -1){
                        puts("ERROR!");
                        exit(-1);
                }
                if(buf[i] == '\n'){
                        return;
                }
                i++;
        }
}
```
`input()`有很明顯的out-of-bound read，只要不輸入換行字元便能不斷讀取。因為`\x00`並不會導致中斷讀取，因此可以在`input(input_password)`時利用overflow將`username`、`input_username`、`password`、`input_password`全部寫成一樣的字串來通過判斷。

成功登入後發現多了一個選項
```
Logged in!
1: Public contents
2: Login
3: Exit
4: Manage
```
利用Manage功能，就可以下載`lazy`的執行檔，但程式禁止輸入的字串中包含`.`，所以無法直接下載`libc.so.6`。
```
Welcome to private directory
You can download contents in this directory, but you can't download contents with a dot in the name
lazy
libc.so.6
Input file name
```
拿到`lazy`後就能開始進行逆向。

首先可以直接在`login()`裡看到帳號密碼，之後就可以直接用來登入
```c
strcpy(username, "_H4CK3R_");
strcpy(password, "3XPL01717");
```

* 在功能1: `public()`中發現會將目錄切換到`./q/public`，但此處輸入使用`fgets()`，沒有overflow。
```c
unsigned __int64 public() {
  char *HOME; // rax
  char s[24]; // [rsp+0h] [rbp-20h]
  if ( chdir("./q/public") == -1 ) {
    ...
  }
  puts("Welcome to public directory");
  puts("You can download contents in this directory");
  listing();
  fgets(s, 20, stdin);
  download(s);
  HOME = getenv("HOME");
  if ( chdir(HOME) == -1 ) {
    ...
  }
}
```
* 在功能4: `filter()`中則會將目錄切換到`./q/private`，不過此處輸入`input()`，因此可以overflow，而且緊接著有一個format string可以利用。
```c
void __fastcall filter()
{
  char *HOME; // rax
  char s[24]; // [rsp+0h] [rbp-20h]
  
  ...
  if ( chdir("./q/private") == -1 ) {
    ...
  }
  puts("Welcome to private directory");
  puts("You can download contents in this directory, but you can't download contents with a dot in the name");
  listing();
  puts("Input file name");
  input(s);
  if ( strchr(s, '.') ) {
     exit(-1);
  }
  printf("Filename : ");
  printf(s);
  puts("OK! Downloading...");
  download(s);
  HOME = getenv("HOME");
  if ( chdir(HOME) == -1 ) {
    exit(-1);
  }
}
```

本題因為有stack canary保護，所以需要利用format string來洩漏canary，之後就能進行ROP了。

由於對於路徑包含`.`的檢查是在download外進行，因此可以ROP呼叫`input()`輸入檔名後再呼叫`download()`來下載任意檔案。但我們發現無論如何，libc總是在下載約4MB/10MB左右時就遇到EOF意外中止，得到的片段部分無論是`objdump、nm`還是`one_gadget`等工具都無法讀取。

接著嘗試了另一種思路，控制`chdir()`的參數接著呼叫`listing()`達到path traversal找到flag，再使用`download()`下載flag，前部分很順利，可以看到目錄底下有
```
run.sh
lazy
ld.so
cat
.profile
libc.so.6
810a0afb2c69f8864ee65f0bdca999d7_FLAG
.bashrc
q
.bash_logout
```
不巧，`810a0afb2c69f8864ee65f0bdca999d7_FLAG`檔名長度超過了`download()`的限制(>27)，只能試著用`open()`, `read()`, `puts()`來進行讀檔(沒有rdx的gadget，但可以通過呼叫一次`strlen()`來讓`rdx`變為能作為`read` size的適當大小)，然而卻發現沒辦法成功讀到flag，而且同目錄下有一個`cat`。因此推測程式沒有讀取flag的權限，可能需要用有setuid的`cat`來進行讀取，這就代表一定需要libc來拿到`shell`或執行`execve`。

正當我苦無對策時，隊友@HexRabbit發現用IDA Pro可以解析出不完整的`libc`，所以只要leak出stack上return的`__libc_start_main`，接著算出`system`再用ROP讀取`sh`跳過去就結束了。

```
$ ./cat 810a0afb2c69f8864ee65f0bdca999d7_FLAG
SECCON{Keep_Going!_KEEP_GOING!_K33P_G01NG!}
```
