# SECCON CTF Quals - 2019

## Misc / 279 - Sandstorm 

> I've received a letter... Uh, Mr. Smith?
> ![](./imgs/sandstorm.png)

### Solution

By [@afcidk](https://github.com/afcidk)

From the provided image, we can guess that this challenge is related to Adam7, which is an interlacing scheme for PNG images. Adam7 has seven passes, so I decide to generate those seven subimages first, and see if there is any clues.

I wrote a simple script to transform the original [sandstorm.png](./imgs/sandstorm.png) to seven images using Adam7 algorithm.

Level 1:
![](./imgs/level1.png)

Level 2:
![](./imgs/level2.png)

Level 3:
![](./imgs/level3.png)

Level 4:
![](./imgs/level4.png)

Level 5:
![](./imgs/level5.png)

Level 6:
![](./imgs/level6.png)

Level 7:
![](./imgs/level7.png)

The flag is encoded to QR code in Level-1 subimage, `SECCON{p0nlMpzlCQ5AHol6}`.

### Reference

* [Adam7 algorithm](https://en.wikipedia.org/wiki/Adam7_algorithm)
