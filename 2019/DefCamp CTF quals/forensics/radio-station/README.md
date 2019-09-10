# D-CTF - 2019
###### Contributed by afcidk

## Radio Station - 316 / Forensics

We managed to intercept all the traffic within a pirate radio station. Could you help us what is it going on? I think you should be an artist to understand them... 
Flag format: DCTF + 19 alphanumeric characters + DCTF

### Solution
We took a look at the provided [traffic](./traffic.7z) file first, and found that this pcap file captures many GET requests for pictures.

We can find that they are all covers of albums, the downloaded pictures can be found [here](./pictures.7z)

We first tried [stegdetect](https://linux.die.net/man/1/stegdetect) to analyze all the pictures, and got the following results.

```
0843f93df10815bde14176ba1f8459e8b32f38b6 : negative
118247f5437b8a527487f5f99ce576b8fbdc98fc : negative
1a3f165b0e7a0ea003c9f3a447e05cc2dfa4288a : negative
20d5ccc04cba362c613f0d8521077ec8bcb1e857 : negative
26a3e45a68317a8e21a08b02bb136335b8963ae1 : negative
336471918174b6c76124f2dcef8956c8016178f5 : negative
41d223339d4a7b6002665c4196cb055019f3e7aa : negative
43b85702779d9cdf91430cbe7f8c9327c1a2fe45 : negative
45881f936e2aadb16355052fdf68cf54ed4cacba : negative
474115d5ea751cbc949052427538e9c745db077e : jphide(***)
5955b33bd14a312f331bb3c2dc3ac527fc21d6df : negative
606336f26cd23dc672ba3b1ad986f0284e089d7d : negative
62c225bdbe30485332b18cf9cbfbaeb010b33b21 : negative
70b0c1d8ae1d88e5a4ced559b97bc06ab048ee56 : negative
77eb7c17cafe550265ac9656051fe4e651a00d70 : negative
77eb7c17cafe55026b823b02df0c4513a863e106 : skipped (false positive likely)
7a670279f866362cdc04d76450c351b83dba53cd : negative
7e79bbb6f3c7e32da90e643ab40ba40533c53bac : negative
7f3fd84167f5f990f570aedd338f8ed31541d085 : negative
8b96f771abe2f3d8d998f589d7b40748f6f4463d : negative
96b35b373991e847a94926e21f1fddc4a82ec784 : negative
9f8bd0efcc5566b42db44064b6a1e0356c5dbdd4 : negative
a392f0f7a7dbc6424f769f6f7f7824e40c42a734 : negative
ba9f2138015f926ed8fffe8a4c285f330216f572 : jphide(***)
c588ccad32d0d482301c5ab42e71a359464ff830 : negative
d3b33d8067e34f2e7555205471a2b7d4693612f6 : negative
e08b756820a7c5a05220b733942575d06c744ec4 : negative
```

It seems that some message has been hidden in the pictures. However, we cannot get any results using the rockyou and [stegbreak](https://linux.die.net/man/1/stegbreak) to crack the password.
> Stegbreak cannot accept the word list that contains words more than 127 characters. For more information, please see [Stegbreak Segmentation Fault Fix](http://digital-forensics-student.blogspot.com/2015/02/stegbreak-segmentation-fault-fix.html).

After some other tries, we finally realize that the flag format is `DCTF + 19 alphanumeric characters + DCTF`. It is 27 characters long, which is equal to the total amount of the downloaded pictures.

By googling the albums, we found that the flag is composed of the first character of the artists' name (this can be verified by checking the first and last four images, which is known to be both "DCTF").

The information of the albums is as follows, and the flag lies in the first character of the album information
```
20d5ccc04cba362c613f0d8521077ec8bcb1e857 Disturbed - Disturbed
0843f93df10815bde14176ba1f8459e8b32f38b6 Christian Nodal - Me Dejé Llevar
43b85702779d9cdf91430cbe7f8c9327c1a2fe45 Three Days Grace - Never Too Late
41d223339d4a7b6002665c4196cb055019f3e7aa Five Finger Death Punch Pharaohs - Blue on Black 
7e79bbb6f3c7e32da90e643ab40ba40533c53bac Slipknot - Vol. 3: The Subliminal Verses
c588ccad32d0d482301c5ab42e71a359464ff830 Korn - See You on the Other Side
d3b33d8067e34f2e7555205471a2b7d4693612f6 Seether - Finding Beauty in Negative Spaces
336471918174b6c76124f2dcef8956c8016178f5 Breaking Benjamin - I Will Not Bow
e08b756820a7c5a05220b733942575d06c744ec4 Dual Core - All the Things 
474115d5ea751cbc949052427538e9c745db077e Jedi Mind Tricks - Uncommon Valor: A Vietnam Story
77eb7c17cafe55026b823b02df0c4513a863e106 Eminem - The Eminem Show
8b96f771abe2f3d8d998f589d7b40748f6f4463d Non Phixion - Black Helicopters 
ba9f2138015f926ed8fffe8a4c285f330216f572 Crazy Town - The Gift of Game
7a670279f866362cdc04d76450c351b83dba53cd Quarashi- Mess it up
62c225bdbe30485332b18cf9cbfbaeb010b33b21 Army of the 
118247f5437b8a527487f5f99ce576b8fbdc98fc Vinnie Paz - God of the Serengeti
606336f26cd23dc672ba3b1ad986f0284e089d7d 7L & Esoteric - This Is War (feat. Army Of The Pharaohs)
9f8bd0efcc5566b42db44064b6a1e0356c5dbdd4 Kenny Dorham
26a3e45a68317a8e21a08b02bb136335b8963ae1 Art Tatum - The Complete Capitol Recordings
7f3fd84167f5f990f570aedd338f8ed31541d085 Chick Corea
70b0c1d8ae1d88e5a4ced559b97bc06ab048ee56 Volbeat - Guitar Gangsters & Cadillac Blood
1a3f165b0e7a0ea003c9f3a447e05cc2dfa4288a Metallica - Master of Puppets 
5955b33bd14a312f331bb3c2dc3ac527fc21d6df Trapt
96b35b373991e847a94926e21f1fddc4a82ec784 Drake - Care Package
77eb7c17cafe550265ac9656051fe4e651a00d70 Coldplay - Live in Buenos Aires
a392f0f7a7dbc6424f769f6f7f7824e40c42a734 Three Days Grace - Transit Of Venus
45881f936e2aadb16355052fdf68cf54ed4cacba Fall Out Boy - Save Rock and Roll
```

`DCTFSKSBDJENCQAV7KACVMTDCTF`.
