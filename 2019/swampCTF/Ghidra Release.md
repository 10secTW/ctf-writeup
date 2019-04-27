# SwampCTF - 2019
###### Contributed by ScottChen

## Ghidra Release - 310 / Misc

:::info
[Meanwhile at the NSA on a Friday afternoon]

Manager: Hey, we're going to be releasing our internal video training for Ghidra and we need you to watch it all to flag any content that needs to be redacted before release.

Manager: The release is next Monday. Hope you didn't have any weekend plans!

You: Uhhh, sure bu-

Manager: Great! Thanks. Make sure nothing gets out.

You: ... [looks at clock. It reads 3:45PM]

You: [Mutters to self] No way am I watching all of this: https://static.swampctf.com/ghidra_nsa_training.mp4
[ghidra_nsa_training.mp4](https://drive.google.com/file/d/1xJQrAhgIN4XvpqhfNzQVFrTaqYn812cl/view?usp=sharing)
:::

### Solution
I think the flag may be hidden in some view of video, so I use ffmpeg to get frames for each 10min:
```shell=
ffmpeg -i ghidra_nsa_training.mp4 -vf fps=1/600 image%d.png
```
But there isn't any flag, neither each 5min or 1min.

After game, I found my fault with the [writeup](https://ctftime.org/writeup/14500) from other teams, the flag only display just ***a few seconds***(about 5 seconds).
So may use ffmpeg to get frames for each five seconds:
```shell=
	ffmpeg -i ghidra_nsa_training.mp4 -vf fps=1/5 image%d.png
```
flag like this:
![flag section](https://i.imgur.com/trP7V0K.png)
Then may use OCR to find four flag section.