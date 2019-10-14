# HITCON CTF Quals - 2019

## Misc / 207 - EV3 Player

>Do you hear the robot sing~~
>
>https://www.youtube.com/watch?v=J5hUOzusb0E
>
>Author: Jeffxx
>58 Teams solved.

### solution

by [@FI](https://github.com/92b2f2)

又是去年出現過的EV3
從他的youtube link可以大概聽到EV3在說話
經過一陣google後 找到一些可能有用的資料

https://www.ev3dev.org/docs/tutorials/using-ev3-speaker/

https://tiebing.blogspot.com/2019/09/lego-ev3-sound-file-rsf-format.html

不過我們還是先strings一下看看封包裡有沒有可以用的資訊
> strings ev3_player-a093689215ca733316ae447edb364512d54bd13e.pklg | less

可以看到裡面有出現許多.rgf .rsf 檔
我們要的是聲音檔所以要找.rsf檔
搜尋一下發現有兩個很可疑的檔案
>../prjs/SD_Card/project/fl.rsf 
>
>../prjs/SD_Card/project/ag.rsf

有上次的經驗 這次很快就知道想要的資料大概會在哪裡了

wireshark display filter: 
```
btrfcomm
```
然後 Find a packet 
![](https://i.imgur.com/JwAaO9k.png)


在他的下一個從localhost傳的封包的data段裡可以看到
> ...0100xxxx01f40000...
![](https://i.imgur.com/vZucc6i.png)


是.rsf 的header
可以確定接下來一直到長度不同的封包為止 都是在傳輸.rsf 檔
接著把filter 過的封包export 成JSON檔 寫個script 把它們重組拿出來
```python
import json

f = ''
of = 0
jq=json.loads(open("btout.json","r").read())
for i in jq:
    if i["_source"]["layers"]["bthci_acl"]["bthci_acl.dst.name"] != "EV3":
        continue
    try: 
        data = i["_source"]["layers"]["data"]["data.data"].replace(':','')
		datalen = i["_source"]["layers"]["data"]["data.len"]
        if bytes.fromhex(data).find(b'fl.rsf') != -1:
            f = open("fl.rsf","wb")
            of = 1
            continue
        if bytes.fromhex(data).find(b'ag.rsf') != -1:
            f = open("ag.rsf","wb")
            of = 1
            continue
        if of == 1:
            f.write(bytes.fromhex(data[14:]))
            if datalen != "907": 
                of = 0
    except:
        pass
```
得到兩個檔案
> fl.rsf ag.rsf

安裝 https://www.ev3dev.org/downloads/ 用他的sound editor 聽 得到flag

`hitcon{playsoundwithlegomindstormsrobot}`
