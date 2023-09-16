## forensics / 277 - Not Just usbpcap

> I recorded one's USB traffic on his computer, can you find the hidden secret?
> [release.pcapng](https://github.com/10secTW/ctf-writeup/blob/master/2023/HITCON%20CTF/release-7ecaf64448a034214d100258675ca969d2232f54.pcapng)
> [color=#33ccff]

### Solution

By [@ScottChen](https://github.com/scott987)
Credits to [@Bandit](https://github.com/rex978956), [@raagi](https://github.com/nashi5566)


先觀察PCAP會發現除了USB裝置外，還包含了藍芽通訊，依照題目名稱，我們首先想到的就是要從藍芽裡面去把通訊的資料拿出來，可以發現藍芽裝置其實是Pixel Buds A-Series耳機，這個裝置從規格文件可以知道其使用的音訊格式只有AAC和SBC兩種。
![remote name](https://hackmd.io/_uploads/rkQKQtf1p.png)

接下來從AVDTP封包可以了解到音訊採用MPEF AAC LC 48000 Hz 2 channels格式：
![AVDTP](https://hackmd.io/_uploads/SJ_nLtz16.png)

後續則有一連串RTP進行音訊傳輸，從資料標頭開頭為47fc，參考RFC 6416確定這些音訊是採用aac latm格式傳輸的AAC資料，只要把這些RTP的data匯出成一音樂檔就可以還原內容
![A2DP RTP](https://hackmd.io/_uploads/BJ-3wFGkT.png)

由於aac latm header不會包含音訊格式資訊，因此需要將latm header重新轉換成adts header，根據前面拿到的資訊，把latm的header "47FC0000B08C800300FFFF91"全換成adts的"FFF94C8052DFFC"，並且合併成一個檔案，從音訊中可以獲得

> welcome back to secret flags unveiled on Hitcon Radio I'm John your host for this intriguing journey into the world of secret flags today we'll explore the secret flag where flag served as vital information for scoring in Ctfs the secret flags are crucial to the success of HITCON CTF and one of them is going to be revealed listen carefully you get only one chance
> flag start
> ***secret flags unveiled with Bluetooth radio***
> flag end
> just simply wrap the text you heard with the flag format if you find some information missing just dig deeper in the packet stay tuned for more secret flags this is John signing off from secret flags unveiled on Hitcon Radio keep those flags flying high.

但空白字元分隔似乎不符合flag格式，因此還需要從其他USB裝置取得資訊，除了藍芽以外還能發現有另外三種裝置:
1. camera(但只有連接，沒有資料)
2. USB Optical Mouse(PixArt)
3. USB-HID Keyboard(HOLTEK)

我們首先測試滑鼠，藉由使用github上的[工具](https://github.com/blluv/mouse-pcap-visualizer)，我們畫出這張圖：
![mouse trace](https://hackmd.io/_uploads/S1YkOcMJT.png)

沒有得到任何有用的訊息，因此改找鍵盤輸入，不過因為鍵盤是利用HID介面，因此利用tshark先把USBHID的data抓出來
```bash!
tshark -r release-7ecaf64448a034214d100258675ca969d2232f54.pcapng -Y 'usbhid.data.key.variable' -T fields -e usbhid.data | sed 's/../:&/g2' > keyboard.data
```
同樣利用[工具](https://github.com/TeamRocketIst/ctf-usb-keyboard-parser)分析，得到鍵盤輸入內容：
> rraaddiioo..cchhaall..hhiittccoonnccttff..ccoomm
> 
> Sssoorrrryy,,  nnoo  ffllaagg  hheerree..  Tttrryy  hhaarrddeerr..
> 
> Buutt  ii  ccaann  tteellll  yyoouu  tthhaatt  tthhee  ffllaagg  ffoorrmmaatt  iiss  hhiittccoonn{lloowweerr--ccaassee--eenngglliisshh--sseeppaarraatteedd--wwiitthh--ddaasshh}
> 
> Aggaaiinn,,  tthhiiss  iiss  nnoott  tthhee  ffllaagg  :(
> 
> C88776633!

因此組合後得到flag: 
`hitcon{secret-flags-unveiled-with-bluetooth-radio}