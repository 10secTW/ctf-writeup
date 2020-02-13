# nullcon HackIM 2020

## re / 176 - year3000

### Solution

By [@jaidTw](https://github.com/jaidTw)

We got 3000 executables after unzipped the challenge. Some were 32-bit x86 ELF, while others were 64-bit. I Randomly opened some binaries and found that they were almost same. These executables read a input then perform a check.

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
Here's the checking function from one binary. The format of the valid input is: a character repeats N times, followed by some trailing bytes, which would be compared to a buffer in memoery. Different binaries have different character, repetition times and trailing bytes, but the offset of these value are fixed inside the binary, so we can easily parse them.

Try to connect to the challenge, we got a filename and ask for some base64 input. So what we have to do is automate the parsing process, then generate the solution encoded by base64.

[sol.py](./sol.py)
