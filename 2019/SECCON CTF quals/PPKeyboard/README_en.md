# SECCON CTF Quals - 2019

## Rev / 352 - PPKeyboard

> Get a message.
>
>    [PPKeyboard.exe](./PPKeyboard.exe)
>    [packets.pcapng](./packets.pcapng)

### Solution

By [@jaidTw](https://github.com/jaidTw)

We were given a pcap and an executable, which found was a program for handling MIDI after reversing.

In `midiInOpen(&phmi, devID, (DWORD_PTR)midiCallBack, 0i64, CALLBACK_FUNCTION)`, a callback function which will be called on receiving messages was set.

In the callback
```c
void midiCallBack(HMIDIIN hMidiIn, UINT wMsg, DWORD_PTR dwInstance, DWORD_PTR dwParam1, DWORD_PTR dwParam2) {
  if ( wMsg == MIM_DATA && (uint32_t)dwParam1 > 0x7F0000 ) {
    if ( (uint8_t)dwParam1 == 0x97 ) {
      printf("0x%x", ((dwParam1 & 0xFFF) - 0x97) >> 8);
    }
    else if ( (uint8_t)dwParam1 == 0x99 ) {
      printf("%x ", ((dwParam1 & 0xFFF) - 0x99) >> 8);
    }
  }
}
```
According to MSDN，dwParam1 is theMidiMassage itself.

> MIDI message that was received. The message is packed into a doubleword value as follows:
> 
> |Word|Byte|Usage|
> |--|--|--|--|
> |High word | High-order byte | Not used. |
> |          | Low-order byte  | Contains a second byte of MIDI data (when needed).  |
> | Low word | High-order byte | Contains the first byte of MIDI data (when needed). |
> |          |Low-order byte   | Contains the MIDI status. |

callback will print out something based on the message content, thus let's grab all the messages from the packet first.
```
$ tshark packets.pcapng -T fields -e usb.capdata > dump
```
Then, use the script belowed to read data, and simulate program's output.
```py3
#!/usr/bin/env python3
with open('dump', 'r') as f:
    data = f.read()

output = ""

for p in data.split():
    p = p[-2:] + p[-4:-2] + p[-6:-4] + p[-8:-6]
    i = int(p, 16) >> 8
    if i >= 0x7F0000:
        if (i & 0xFF) == 0x97:
            output += "0x%x" % (((i & 0xFFF) - 0x97) >> 8)
        elif (i & 0xFF) == 0x99:
            output += "%x " % (((i & 0xFFF) - 0x99) >> 8)

print("".join([chr(int(c, 16)) for c in output.split()]))
```
Finally, output is a sequence of hex numbers(`"%xx %xx.."`), just convert it to the string then you will get the flag.

```
$ python sol.py
Hey guys! FLAG is SECCON{3n73r3d_fr0m_7h3_p3rf0rm4nc3_p4d_k3yb04rd}
```

### Reference (optional)

* [MSDN midiInOpen](https://docs.microsoft.com/en-us/windows/win32/api/mmeapi/nf-mmeapi-midiinopen)
* [MSDN midiInProc](https://docs.microsoft.com/zh-tw/previous-versions/dd798460(v=vs.85)
* [MSDN MIM_DATA](https://docs.microsoft.com/zh-tw/windows/win32/multimedia/mim-data?redirectedfrom=MSDN)
