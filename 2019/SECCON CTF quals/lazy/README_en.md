# SECCON CTF Quals - 2019

## Pwn / 332 - lazy
> ```
> lazy.chal.seccon.jp 33333
> ```
### solution

By [@jaidTw](https://github.com/jaidTw)

Credits to [@HexRabbit](https://blog.hexrabbit.io)

This challenge didn't give us any file. Connect to the challenge first.
```
1: Public contents
2: Login
3: Exit
```
Select option 1
```
Welcome to public directory
You can download contents in this directory
diary_4.txt
diary_3.txt
diary_1.txt
login_source.c
diary_2.txt
```
I can download login_source.c, there were only soure code of functions `login` and `input`.
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
Apparently, there's a out-of-bound read inside `input()`, it won't stop reading until a `'\n'` is encountered. Because `\x00` won't stop the read, in `input(input_password)`, we can overwrite `username`, `input_username`, `password`, `input_password` into same strings to pass the check.

There was a new option after successfully logged in.
```
Logged in!
1: Public contents
2: Login
3: Exit
4: Manage
```
I could download the binary `lazy` using option 4, but `.` is not allowed in the input by the program, so I couldn't download `libc.so.6`.
```
Welcome to private directory
You can download contents in this directory, but you can't download contents with a dot in the name
lazy
libc.so.6
Input file name
```
After used the [script](./get_lazy.py) to get `lazy`, I started to reverse it.

First, in `login()`, here were the username and password, so just use them to login in the following expoits.
```c
strcpy(username, "_H4CK3R_");
strcpy(password, "3XPL01717");
```

* In option 1 `public()`: Switch the directory to `./q/public`, but input use `fgets()`, no overflow here.
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
* In option 4 `filter()`: Switch the directory to `./q/private`. Input used `input()` here, so a stack overflow, followed by a format string vulnerability.
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
Stack canary is on, so we need to leak the canary by format string first, then do the ROP.

Because the `.` check of the path is perform outside of `download()`, so I used ROP to first call `input()`, getting the filename wrote to a buffer, then call `download()` with the buffer to download anyfile. But soon, we found that when trying to download `libc.so.6`, we always got an unexpected EOF and terminated, so the libc was incomplete(~4MB/10MB), I tried many tools such as `objdump`, `nm` and `one_gadget`, but none of them worked with a incomplete libc.

Later, I tried another approach: control the directory using `chdir()`, then call `listing()` to traverse and search for the flag, then use `download()` to get the flag. This looked promising and I successfully read the directory.
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
Unfortunately, the filename of `810a0afb2c69f8864ee65f0bdca999d7_FLAG` exceeded the limit of `download()` (>27), I could only try to use `open()`, `read()`, `puts()` to read the file (There's no a rdx gadget, but you can assign rdx an appropriate value for `read()` by calling `strlen()`).

Now, I could read most of the files, including those under `/proc`, however, I still couldn't read the flag, and I found there was a `cat` in the same directory, so I guessed the flag should be read by the `cat` with setuid. This means the only ways to get the flag were to invoke the shell or use `execve` to run the setuid `cat`, which I thought were impossible without using libc.

When I was almost giving it up, my teammate [@HexRabbit](https://blog.hexrabbit.io) found that IDA Pro can parse the incomplete `libc.so.6`, so we only need to leak `__libc_start_main` from stack, calculate the address of `system`, then use ROP to read `sh` and jump to `system`, and that's it.

Here's the [script](./exp.py)

```
$ ./cat 810a0afb2c69f8864ee65f0bdca999d7_FLAG
SECCON{Keep_Going!_KEEP_GOING!_K33P_G01NG!}
```
