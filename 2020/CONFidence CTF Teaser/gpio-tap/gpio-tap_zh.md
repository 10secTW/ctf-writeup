# CONFidence CTF Teaser - 2020

## Misc / 53 - GPIO Tap

> We managed to intercept some traffic on the GPIOs, can you find out what was transmitted?

![](https://i.imgur.com/ZXll565.jpg)


### Solution

By [@Raagi](https://github.com/nashi5566)


可以看到圖片中是一個 rpi3 接 16*2 LCD 螢幕，用 rpi3 的 gpio 送 l2c 訊號給 LCD，此外題目有提供一個 `tap.gpio` 的檔案，內容紀錄了每個腳位的訊號是 `HIGH` 還是 `LOW`。

```=
4 -> LOW
25 -> LOW
17 -> HIGH
18 -> LOW
22 -> LOW
23 -> HIGH
24 -> LOW
24 -> HIGH
24 -> LOW
....
```

根據圖片的電路以及訊號的行為判斷，可以得知腳位與訊號的對應關係：
* `GPIO_25` -> `RS`
* `GPIO_24` -> `Enable`
* `GPIO_22` -> `D4`
* `GPIO_18` -> `D5`
* `GPIO_17` -> `D6`
* `GPIO_23` -> `D7`

`HD44780` 這個 controller 處理訊號的邏輯是：每個指令都是一組 2-digit heximal ，而 `[D4:D7]` 訊號每次會先送高四位、再送低四位。 (eg. 1st `[D4:D7]` = 0011, 2nd `[D4:D7]` = 1010, `[b7:b0]` = 00111010)

這邊可以注意到 `RS` 這個訊號，當 `RS` 為 `LOW` 時是指令模式，詳細的指令表可以參照[這裡](https://www.electronicsforu.com/resources/learn-electronics/16x2-lcd-pinout-diagram)，題目中主要使用到的有 `01H`：清空畫面、 `18H` ： 整個畫面右移，以及最重要的兩個指令 `8XH` ：將游標移動到第一行的第 `X` 個位置、 `CXH` ：將游標移動到第二行的第 `X` 個位置。

而 `RS` 為 `HIGH` 時為資料模式， LCD 中有一個 CGRAM ，事先存放了一些常用的字元和符號，在資料模式的情況下 `[D4:D7]` 的訊號會被解讀成 CGRAM 的位址，藉由位址找到對應存放的字元或符號。

知道以上的資訊之後，就可以來 parse `tap.gpio` 的資料和處理如何寫入字元了。

[exploit.py](https://github.com/nashi5566/ctf_writeups/blob/master/gpio-tap/exploit.py)

```
Welcome to p4ctf :) !!
p4{GPIO_t4p_warmup}
```

---
### Referenece

* [How 16×2 LCDs work | Build a basic 16×2 character LCD](https://www.electronicsforu.com/resources/learn-electronics/16x2-lcd-pinout-diagram)
* [HD44780 Custom Character Table](https://circuitdigest.com/sites/default/files/inlineimages/datasheet-of-lcd-controller-IC-HD44780.png)
