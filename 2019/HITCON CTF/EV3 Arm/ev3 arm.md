# HITCON CTF Quals - 2019

## Misc / 221 - EV3 Arm

> ![snapshot](https://imgur.com/BxyS1Qk.png)
>
> https://youtu.be/6Hb4KEqtboI
>
> [ev3_arm-17958868466f3801c4926675e13863b838e8e7cc.rbf](http://hitcon-2019-quals.s3-website-ap-northeast-1.amazonaws.com/ev3_arm-17958868466f3801c4926675e13863b838e8e7cc.rbf)
>
> Author: Jeffxx
>
> 48 Teams solved.

### Solution

By [@chuanchan](https://github.com/chuanchan1116)

The file provided is a binary that runs on Lego Mindstorms EV3. Using [this website](http://ev3treevis.azurewebsites.net/) to get a list of readable instructions. The Lego Mindstorms EV3 has 4 ports to connect to the motor. If you watch the video closely and compare to the picture provided in the description, you'll see that ports B connects to motor lifting or striking the pen, port A connects to motor for vertical stroke, and port C connects to motor for horizontal movements.

Comparing the instructions with the video, it's easy to speculate that `port_motor: B | rotations: 35 | speed: -15` strikes the pen, `port_motor: A | rotations: 720 | speed: -75` creates a stroke about height of `h`, `port_motor: C | rotations: 2 | speed: 70` create a stroke about width of `h`. Everytime a character is written, the pen will reset to the left top corner for the next letter. Trying to manipulate the instructions manually, and you will get the flag.

`flag:hitcon{why_not_just_use_the_printer}`

Instructions decoded are as follow

```
ev3_arm
 ├─ MediumMotor.Degrees brake: 0 | port_motor: B | rotations: 35 | speed: -15
 ├─ MediumMotor.Degrees brake: 0 | port_motor: A | rotations: 720 | speed: -75
 ├─ MediumMotor.Degrees brake: 0 | port_motor: B | rotations: 35 | speed: 15
 ├─ MediumMotor.Degrees brake: 0 | port_motor: A | rotations: 360 | speed: 75
 ├─ MediumMotor.Degrees brake: 0 | port_motor: B | rotations: 35 | speed: -15
 ├─ Motor.Rotations brake: 1 | port_motor: C | rotations: 2 | speed: 70
 ├─ MediumMotor.Degrees brake: 0 | port_motor: A | rotations: 360 | speed: -75
 ├─ MediumMotor.Degrees brake: 0 | port_motor: B | rotations: 35 | speed: 15
 //h
 ├─ MediumMotor.Degrees brake: 0 | port_motor: A | rotations: 720 | speed: 75
 ├─ Motor.Rotations brake: 1 | port_motor: C | rotations: 1.5 | speed: 70
 ├─ MediumMotor.Degrees brake: 0 | port_motor: B | rotations: 35 | speed: -15
 ├─ MediumMotor.Degrees brake: 0 | port_motor: A | rotations: 180 | speed: -75
 ├─ MediumMotor.Degrees brake: 0 | port_motor: B | rotations: 35 | speed: 15
 ├─ MediumMotor.Degrees brake: 0 | port_motor: A | rotations: 180 | speed: -75
 ├─ MediumMotor.Degrees brake: 0 | port_motor: B | rotations: 35 | speed: -15
 ├─ MediumMotor.Degrees brake: 0 | port_motor: A | rotations: 360 | speed: -75
 ├─ MediumMotor.Degrees brake: 0 | port_motor: B | rotations: 35 | speed: 15
 //i
 ├─ MediumMotor.Degrees brake: 0 | port_motor: A | rotations: 720 | speed: 75
 ├─ Motor.Rotations brake: 1 | port_motor: C | rotations: 1.5 | speed: 70
 ├─ MediumMotor.Degrees brake: 0 | port_motor: A | rotations: 360 | speed: -75
 ├─ MediumMotor.Degrees brake: 0 | port_motor: B | rotations: 35 | speed: -15
 ├─ Motor.Rotations brake: 1 | port_motor: C | rotations: 1.5 | speed: 70
 ├─ MediumMotor.Degrees brake: 0 | port_motor: B | rotations: 35 | speed: 15
 ├─ Motor.Rotations brake: 1 | port_motor: C | rotations: 1 | speed: -70
 ├─ MediumMotor.Degrees brake: 0 | port_motor: A | rotations: 90 | speed: 75
 ├─ MediumMotor.Degrees brake: 0 | port_motor: B | rotations: 35 | speed: -15
 ├─ MediumMotor.Degrees brake: 0 | port_motor: A | rotations: 450 | speed: -75
 ├─ MediumMotor.Degrees brake: 0 | port_motor: B | rotations: 35 | speed: 15
 //t
 ├─ MediumMotor.Degrees brake: 0 | port_motor: A | rotations: 720 | speed: 75
 ├─ Motor.Rotations brake: 1 | port_motor: C | rotations: 4 | speed: 70
 ├─ MediumMotor.Degrees brake: 0 | port_motor: A | rotations: 360 | speed: -75
 ├─ MediumMotor.Degrees brake: 0 | port_motor: B | rotations: 35 | speed: -15
 ├─ Motor.Rotations brake: 1 | port_motor: C | rotations: 2 | speed: -70
 ├─ MediumMotor.Degrees brake: 0 | port_motor: A | rotations: 360 | speed: -75
 ├─ Motor.Rotations brake: 1 | port_motor: C | rotations: 2 | speed: 70
 ├─ MediumMotor.Degrees brake: 0 | port_motor: B | rotations: 35 | speed: 15
 //c
 ├─ MediumMotor.Degrees brake: 0 | port_motor: A | rotations: 720 | speed: 75
 ├─ Motor.Rotations brake: 1 | port_motor: C | rotations: 3.5 | speed: 70
 ├─ MediumMotor.Degrees brake: 0 | port_motor: A | rotations: 360 | speed: -75
 ├─ MediumMotor.Degrees brake: 0 | port_motor: B | rotations: 35 | speed: -15
 ├─ Motor.Rotations brake: 1 | port_motor: C | rotations: 2 | speed: -70
 ├─ MediumMotor.Degrees brake: 0 | port_motor: A | rotations: 360 | speed: -75
 ├─ Motor.Rotations brake: 1 | port_motor: C | rotations: 2 | speed: 70
 ├─ MediumMotor.Degrees brake: 0 | port_motor: A | rotations: 420 | speed: 75
 ├─ MediumMotor.Degrees brake: 0 | port_motor: B | rotations: 35 | speed: 15
 //o
 ├─ MediumMotor.Degrees brake: 0 | port_motor: A | rotations: 300 | speed: 75
 ├─ Motor.Rotations brake: 1 | port_motor: C | rotations: 1.5 | speed: 70
 ├─ MediumMotor.Degrees brake: 0 | port_motor: A | rotations: 320 | speed: -75
 ├─ MediumMotor.Degrees brake: 0 | port_motor: B | rotations: 35 | speed: -15
 ├─ MediumMotor.Degrees brake: 0 | port_motor: A | rotations: 400 | speed: -75
 ├─ MediumMotor.Degrees brake: 0 | port_motor: A | rotations: 420 | speed: 75
 ├─ FORK objectid: 3
 │  └─ Motor.Rotations brake: 1 | port_motor: C | rotations: 2 | speed: 60
 ├─ MediumMotor.Degrees brake: 0 | port_motor: A | rotations: 120 | speed: 15
 ├─ MediumMotor.Degrees brake: 0 | port_motor: A | rotations: 480 | speed: -75
 ├─ MediumMotor.Degrees brake: 0 | port_motor: B | rotations: 35 | speed: 15
 //n
 ├─ MediumMotor.Degrees brake: 0 | port_motor: A | rotations: 660 | speed: 75
 ├─ CommentBlock
 ├─ Motor.Rotations brake: 1 | port_motor: C | rotations: 2 | speed: 70
 ├─ MediumMotor.Degrees brake: 0 | port_motor: B | rotations: 35 | speed: -15
 ├─ Motor.Rotations brake: 1 | port_motor: C | rotations: 0.5 | speed: -70
 ├─ MediumMotor.Degrees brake: 0 | port_motor: A | rotations: 300 | speed: -75
 ├─ FORK objectid: 5
 │  ├─ Motor.Rotations brake: 1 | port_motor: C | rotations: 0.3 | speed: -90
 │  └─ Motor.Rotations brake: 1 | port_motor: C | rotations: 0.3 | speed: 90
 ├─ MediumMotor.Degrees brake: 0 | port_motor: A | rotations: 120 | speed: -75
 ├─ MediumMotor.Degrees brake: 0 | port_motor: A | rotations: 300 | speed: -75
 ├─ Motor.Rotations brake: 1 | port_motor: C | rotations: 0.5 | speed: 70
 ├─ MediumMotor.Degrees brake: 0 | port_motor: B | rotations: 35 | speed: 15
 //{
 ├─ MediumMotor.Degrees brake: 0 | port_motor: A | rotations: 720 | speed: 75
 ├─ Motor.Rotations brake: 1 | port_motor: C | rotations: 1.5 | speed: 70
 ├─ MediumMotor.Degrees brake: 0 | port_motor: A | rotations: 360 | speed: -75
 ├─ MediumMotor.Degrees brake: 0 | port_motor: B | rotations: 35 | speed: -15
 ├─ FORK objectid: 7
 │  └─ Motor.Rotations brake: 1 | port_motor: C | rotations: 2.2 | speed: 35
 ├─ MediumMotor.Degrees brake: 0 | port_motor: A | rotations: 360 | speed: -75
 ├─ MediumMotor.Degrees brake: 0 | port_motor: A | rotations: 360 | speed: 75
 ├─ MediumMotor.Degrees brake: 0 | port_motor: A | rotations: 360 | speed: -75
 ├─ MediumMotor.Degrees brake: 0 | port_motor: A | rotations: 420 | speed: 75
 ├─ MediumMotor.Degrees brake: 0 | port_motor: B | rotations: 35 | speed: 15
 //w
 ├─ MediumMotor.Degrees brake: 0 | port_motor: A | rotations: 300 | speed: 75
 ├─ Motor.Rotations brake: 1 | port_motor: C | rotations: 1.5 | speed: 70
 ├─ MediumMotor.Degrees brake: 0 | port_motor: B | rotations: 35 | speed: -15
 ├─ MediumMotor.Degrees brake: 0 | port_motor: A | rotations: 720 | speed: -75
 ├─ MediumMotor.Degrees brake: 0 | port_motor: B | rotations: 35 | speed: 15
 ├─ MediumMotor.Degrees brake: 0 | port_motor: A | rotations: 360 | speed: 75
 ├─ MediumMotor.Degrees brake: 0 | port_motor: B | rotations: 35 | speed: -15
 ├─ Motor.Rotations brake: 1 | port_motor: C | rotations: 2 | speed: 70
 ├─ MediumMotor.Degrees brake: 0 | port_motor: A | rotations: 360 | speed: -75
 ├─ MediumMotor.Degrees brake: 0 | port_motor: B | rotations: 35 | speed: 15
 //h
 ├─ MediumMotor.Degrees brake: 0 | port_motor: A | rotations: 720 | speed: 75
 ├─ Motor.Rotations brake: 1 | port_motor: C | rotations: 1 | speed: 70
 ├─ MediumMotor.Degrees brake: 0 | port_motor: A | rotations: 360 | speed: -75
 ├─ MediumMotor.Degrees brake: 0 | port_motor: B | rotations: 35 | speed: -15
 ├─ FORK objectid: 9
 │  └─ Motor.Rotations brake: 1 | port_motor: C | rotations: 2.2 | speed: 70
 ├─ MediumMotor.Degrees brake: 0 | port_motor: A | rotations: 360 | speed: -75
 ├─ MediumMotor.Degrees brake: 0 | port_motor: A | rotations: 420 | speed: 75
 ├─ MediumMotor.Degrees brake: 0 | port_motor: A | rotations: 600 | speed: -75
 ├─ Motor.Rotations brake: 1 | port_motor: C | rotations: 0.75 | speed: -70
 ├─ MediumMotor.Degrees brake: 0 | port_motor: B | rotations: 35 | speed: 15
 //y
 ├─ Motor.Rotations brake: 1 | port_motor: C | rotations: 0.75 | speed: 70
 ├─ MediumMotor.Degrees brake: 0 | port_motor: A | rotations: 900 | speed: 75
 ├─ Motor.Rotations brake: 1 | port_motor: C | rotations: 1.5 | speed: 70
 ├─ MediumMotor.Degrees brake: 0 | port_motor: A | rotations: 720 | speed: -75
 ├─ MediumMotor.Degrees brake: 0 | port_motor: B | rotations: 35 | speed: -15
 ├─ Motor.Rotations brake: 1 | port_motor: C | rotations: 2 | speed: 70
 ├─ MediumMotor.Degrees brake: 0 | port_motor: B | rotations: 35 | speed: 15
 //_
 ├─ MediumMotor.Degrees brake: 0 | port_motor: A | rotations: 720 | speed: 75
 ├─ Motor.Rotations brake: 1 | port_motor: C | rotations: 1.5 | speed: 70
 ├─ MediumMotor.Degrees brake: 0 | port_motor: A | rotations: 360 | speed: -75
 ├─ MediumMotor.Degrees brake: 0 | port_motor: B | rotations: 35 | speed: -15
 ├─ MediumMotor.Degrees brake: 0 | port_motor: A | rotations: 400 | speed: -75
 ├─ MediumMotor.Degrees brake: 0 | port_motor: A | rotations: 420 | speed: 75
 ├─ FORK objectid: 10
 │  └─ Motor.Rotations brake: 1 | port_motor: C | rotations: 2 | speed: 60
 ├─ MediumMotor.Degrees brake: 0 | port_motor: A | rotations: 120 | speed: 15
 ├─ MediumMotor.Degrees brake: 0 | port_motor: A | rotations: 480 | speed: -75
 ├─ MediumMotor.Degrees brake: 0 | port_motor: B | rotations: 35 | speed: 15
 ├─ MediumMotor.Degrees brake: 0 | port_motor: A | rotations: 700 | speed: 75
 //n
 ├─ Motor.Rotations brake: 1 | port_motor: C | rotations: 3.5 | speed: 70
 ├─ MediumMotor.Degrees brake: 0 | port_motor: A | rotations: 360 | speed: -75
 ├─ MediumMotor.Degrees brake: 0 | port_motor: B | rotations: 35 | speed: -15
 ├─ Motor.Rotations brake: 1 | port_motor: C | rotations: 2 | speed: -70
 ├─ MediumMotor.Degrees brake: 0 | port_motor: A | rotations: 360 | speed: -75
 ├─ Motor.Rotations brake: 1 | port_motor: C | rotations: 2 | speed: 70
 ├─ MediumMotor.Degrees brake: 0 | port_motor: A | rotations: 420 | speed: 75
 ├─ MediumMotor.Degrees brake: 0 | port_motor: B | rotations: 35 | speed: 15
 ├─ MediumMotor.Degrees brake: 0 | port_motor: A | rotations: 300 | speed: 75
 //o
 ├─ Motor.Rotations brake: 1 | port_motor: C | rotations: 1.5 | speed: 70
 ├─ MediumMotor.Degrees brake: 0 | port_motor: A | rotations: 360 | speed: -75
 ├─ MediumMotor.Degrees brake: 0 | port_motor: B | rotations: 35 | speed: -15
 ├─ Motor.Rotations brake: 1 | port_motor: C | rotations: 1.5 | speed: 70
 ├─ MediumMotor.Degrees brake: 0 | port_motor: B | rotations: 35 | speed: 15
 ├─ Motor.Rotations brake: 1 | port_motor: C | rotations: 1 | speed: -70
 ├─ MediumMotor.Degrees brake: 0 | port_motor: A | rotations: 90 | speed: 75
 ├─ MediumMotor.Degrees brake: 0 | port_motor: B | rotations: 35 | speed: -15
 ├─ MediumMotor.Degrees brake: 0 | port_motor: A | rotations: 450 | speed: -75
 ├─ MediumMotor.Degrees brake: 0 | port_motor: B | rotations: 35 | speed: 15
 ├─ MediumMotor.Degrees brake: 0 | port_motor: A | rotations: 720 | speed: 75
 //t
 ├─ Motor.Rotations brake: 1 | port_motor: C | rotations: 2 | speed: 70
 ├─ MediumMotor.Degrees brake: 0 | port_motor: A | rotations: 720 | speed: -75
 ├─ MediumMotor.Degrees brake: 0 | port_motor: B | rotations: 35 | speed: -15
 ├─ Motor.Rotations brake: 1 | port_motor: C | rotations: 2 | speed: 70
 ├─ MediumMotor.Degrees brake: 0 | port_motor: B | rotations: 35 | speed: 15
 ├─ MediumMotor.Degrees brake: 0 | port_motor: A | rotations: 720 | speed: 75
 //_
 ├─ Motor.Rotations brake: 1 | port_motor: C | rotations: 1.5 | speed: 70
 ├─ MediumMotor.Degrees brake: 0 | port_motor: B | rotations: 35 | speed: -15
 ├─ MediumMotor.Degrees brake: 0 | port_motor: A | rotations: 180 | speed: -75
 ├─ MediumMotor.Degrees brake: 0 | port_motor: B | rotations: 35 | speed: 15
 ├─ MediumMotor.Degrees brake: 0 | port_motor: A | rotations: 180 | speed: -75
 ├─ MediumMotor.Degrees brake: 0 | port_motor: B | rotations: 35 | speed: -15
 ├─ MediumMotor.Degrees brake: 0 | port_motor: A | rotations: 720 | speed: -75
 ├─ FORK objectid: 12
 │  └─ Motor.Rotations brake: 1 | port_motor: C | rotations: 1 | speed: -70
 ├─ MediumMotor.Degrees brake: 0 | port_motor: A | rotations: 180 | speed: 25
 ├─ MediumMotor.Degrees brake: 0 | port_motor: B | rotations: 35 | speed: 15
 ├─ MediumMotor.Degrees brake: 0 | port_motor: A | rotations: 900 | speed: 75
 //j
 ├─ Motor.Rotations brake: 1 | port_motor: C | rotations: 2.5 | speed: 70
 ├─ MediumMotor.Degrees brake: 0 | port_motor: A | rotations: 360 | speed: -75
 ├─ MediumMotor.Degrees brake: 0 | port_motor: B | rotations: 35 | speed: -15
 ├─ MediumMotor.Degrees brake: 0 | port_motor: A | rotations: 400 | speed: -75
 ├─ MediumMotor.Degrees brake: 0 | port_motor: A | rotations: 120 | speed: 75
 ├─ FORK objectid: 15
 │  └─ Motor.Rotations brake: 1 | port_motor: C | rotations: 2 | speed: 60
 ├─ MediumMotor.Degrees brake: 0 | port_motor: A | rotations: 120 | speed: -15
 ├─ MediumMotor.Degrees brake: 0 | port_motor: A | rotations: 480 | speed: 75
 ├─ MediumMotor.Degrees brake: 0 | port_motor: B | rotations: 35 | speed: 15
 ├─ MediumMotor.Degrees brake: 0 | port_motor: A | rotations: 280 | speed: 75
 //u
 ├─ Motor.Rotations brake: 1 | port_motor: C | rotations: 3.5 | speed: 70
 ├─ MediumMotor.Degrees brake: 0 | port_motor: A | rotations: 360 | speed: -75
 ├─ MediumMotor.Degrees brake: 0 | port_motor: B | rotations: 35 | speed: -15
 ├─ FORK objectid: 17
 │  └─ MediumMotor.Degrees brake: 0 | port_motor: A | rotations: 360 | speed: -15
 ├─ Motor.Rotations brake: 1 | port_motor: C | rotations: 2 | speed: -60
 ├─ Motor.Rotations brake: 1 | port_motor: C | rotations: 2 | speed: 80
 ├─ Motor.Rotations brake: 1 | port_motor: C | rotations: 2 | speed: -60
 ├─ MediumMotor.Degrees brake: 0 | port_motor: B | rotations: 35 | speed: 15
 ├─ Motor.Rotations brake: 1 | port_motor: C | rotations: 2 | speed: 70
 ├─ MediumMotor.Degrees brake: 0 | port_motor: A | rotations: 720 | speed: 75
 //s
 ├─ Motor.Rotations brake: 1 | port_motor: C | rotations: 1.5 | speed: 70
 ├─ MediumMotor.Degrees brake: 0 | port_motor: A | rotations: 360 | speed: -75
 ├─ MediumMotor.Degrees brake: 0 | port_motor: B | rotations: 35 | speed: -15
 ├─ Motor.Rotations brake: 1 | port_motor: C | rotations: 1.5 | speed: 70
 ├─ MediumMotor.Degrees brake: 0 | port_motor: B | rotations: 35 | speed: 15
 ├─ Motor.Rotations brake: 1 | port_motor: C | rotations: 1 | speed: -70
 ├─ MediumMotor.Degrees brake: 0 | port_motor: A | rotations: 90 | speed: 75
 ├─ MediumMotor.Degrees brake: 0 | port_motor: B | rotations: 35 | speed: -15
 ├─ MediumMotor.Degrees brake: 0 | port_motor: A | rotations: 450 | speed: -75
 ├─ MediumMotor.Degrees brake: 0 | port_motor: B | rotations: 35 | speed: 15
 ├─ MediumMotor.Degrees brake: 0 | port_motor: A | rotations: 720 | speed: 75
 //t
 ├─ Motor.Rotations brake: 1 | port_motor: C | rotations: 2 | speed: 70
 ├─ MediumMotor.Degrees brake: 0 | port_motor: A | rotations: 720 | speed: -75
 ├─ MediumMotor.Degrees brake: 0 | port_motor: B | rotations: 35 | speed: -15
 ├─ Motor.Rotations brake: 1 | port_motor: C | rotations: 2 | speed: 70
 ├─ MediumMotor.Degrees brake: 0 | port_motor: B | rotations: 35 | speed: 15
 ├─ MediumMotor.Degrees brake: 0 | port_motor: A | rotations: 720 | speed: 75
 //_
 ├─ Motor.Rotations brake: 1 | port_motor: C | rotations: 1.5 | speed: 70
 ├─ MediumMotor.Degrees brake: 0 | port_motor: A | rotations: 360 | speed: -75
 ├─ MediumMotor.Degrees brake: 0 | port_motor: B | rotations: 35 | speed: -15
 ├─ MediumMotor.Degrees brake: 0 | port_motor: A | rotations: 400 | speed: -75
 ├─ MediumMotor.Degrees brake: 0 | port_motor: A | rotations: 120 | speed: 75
 ├─ FORK objectid: 19
 │  └─ Motor.Rotations brake: 1 | port_motor: C | rotations: 2 | speed: 60
 ├─ MediumMotor.Degrees brake: 0 | port_motor: A | rotations: 120 | speed: -15
 ├─ MediumMotor.Degrees brake: 0 | port_motor: A | rotations: 480 | speed: 75
 ├─ MediumMotor.Degrees brake: 0 | port_motor: B | rotations: 35 | speed: 15
 ├─ MediumMotor.Degrees brake: 0 | port_motor: A | rotations: 280 | speed: 75
 ├─ Motor.Rotations brake: 1 | port_motor: C | rotations: 3.5 | speed: 70
 //u
 ├─ MediumMotor.Degrees brake: 0 | port_motor: A | rotations: 360 | speed: -75
 ├─ MediumMotor.Degrees brake: 0 | port_motor: B | rotations: 35 | speed: -15
 ├─ FORK objectid: 21
 │  └─ MediumMotor.Degrees brake: 0 | port_motor: A | rotations: 360 | speed: -15
 ├─ Motor.Rotations brake: 1 | port_motor: C | rotations: 2 | speed: -60
 ├─ Motor.Rotations brake: 1 | port_motor: C | rotations: 2 | speed: 80
 ├─ Motor.Rotations brake: 1 | port_motor: C | rotations: 2 | speed: -60
 ├─ MediumMotor.Degrees brake: 0 | port_motor: B | rotations: 35 | speed: 15
 ├─ Motor.Rotations brake: 1 | port_motor: C | rotations: 2 | speed: 70
 ├─ MediumMotor.Degrees brake: 0 | port_motor: A | rotations: 720 | speed: 75
 //s
 ├─ Motor.Rotations brake: 1 | port_motor: C | rotations: 1.5 | speed: 70
 ├─ MediumMotor.Degrees brake: 0 | port_motor: A | rotations: 540 | speed: -75
 ├─ MediumMotor.Degrees brake: 0 | port_motor: B | rotations: 35 | speed: -15
 ├─ Motor.Rotations brake: 1 | port_motor: C | rotations: 2 | speed: 70
 ├─ MediumMotor.Degrees brake: 0 | port_motor: A | rotations: 240 | speed: 75
 ├─ Motor.Rotations brake: 1 | port_motor: C | rotations: 2 | speed: -70
 ├─ MediumMotor.Degrees brake: 0 | port_motor: A | rotations: 480 | speed: -75
 ├─ Motor.Rotations brake: 1 | port_motor: C | rotations: 2 | speed: 70
 ├─ MediumMotor.Degrees brake: 0 | port_motor: B | rotations: 35 | speed: 15
 ├─ MediumMotor.Degrees brake: 0 | port_motor: A | rotations: 780 | speed: 75
 //e
 ├─ Motor.Rotations brake: 1 | port_motor: C | rotations: 2 | speed: 70
 ├─ MediumMotor.Degrees brake: 0 | port_motor: A | rotations: 720 | speed: -75
 ├─ MediumMotor.Degrees brake: 0 | port_motor: B | rotations: 35 | speed: -15
 ├─ Motor.Rotations brake: 1 | port_motor: C | rotations: 2 | speed: 70
 ├─ MediumMotor.Degrees brake: 0 | port_motor: B | rotations: 35 | speed: 15
 ├─ MediumMotor.Degrees brake: 0 | port_motor: A | rotations: 720 | speed: 75
 //_
 ├─ Motor.Rotations brake: 1 | port_motor: C | rotations: 1.5 | speed: 70
 ├─ MediumMotor.Degrees brake: 0 | port_motor: A | rotations: 360 | speed: -75
 ├─ MediumMotor.Degrees brake: 0 | port_motor: B | rotations: 35 | speed: -15
 ├─ Motor.Rotations brake: 1 | port_motor: C | rotations: 1.5 | speed: 70
 ├─ MediumMotor.Degrees brake: 0 | port_motor: B | rotations: 35 | speed: 15
 ├─ Motor.Rotations brake: 1 | port_motor: C | rotations: 1 | speed: -70
 ├─ MediumMotor.Degrees brake: 0 | port_motor: A | rotations: 90 | speed: 75
 ├─ MediumMotor.Degrees brake: 0 | port_motor: B | rotations: 35 | speed: -15
 ├─ MediumMotor.Degrees brake: 0 | port_motor: A | rotations: 450 | speed: -75
 ├─ MediumMotor.Degrees brake: 0 | port_motor: B | rotations: 35 | speed: 15
 ├─ MediumMotor.Degrees brake: 0 | port_motor: A | rotations: 720 | speed: 75
 //t
 ├─ Motor.Rotations brake: 1 | port_motor: C | rotations: 2.5 | speed: 70
 ├─ MediumMotor.Degrees brake: 0 | port_motor: B | rotations: 35 | speed: -15
 ├─ MediumMotor.Degrees brake: 0 | port_motor: A | rotations: 720 | speed: -75
 ├─ MediumMotor.Degrees brake: 0 | port_motor: B | rotations: 35 | speed: 15
 ├─ MediumMotor.Degrees brake: 0 | port_motor: A | rotations: 360 | speed: 75
 ├─ MediumMotor.Degrees brake: 0 | port_motor: B | rotations: 35 | speed: -15
 ├─ Motor.Rotations brake: 1 | port_motor: C | rotations: 2 | speed: 70
 ├─ MediumMotor.Degrees brake: 0 | port_motor: A | rotations: 360 | speed: -75
 ├─ MediumMotor.Degrees brake: 0 | port_motor: B | rotations: 35 | speed: 15
 ├─ MediumMotor.Degrees brake: 0 | port_motor: A | rotations: 720 | speed: 75
 //h
 ├─ Motor.Rotations brake: 1 | port_motor: C | rotations: 1.5 | speed: 70
 ├─ MediumMotor.Degrees brake: 0 | port_motor: A | rotations: 540 | speed: -75
 ├─ MediumMotor.Degrees brake: 0 | port_motor: B | rotations: 35 | speed: -15
 ├─ Motor.Rotations brake: 1 | port_motor: C | rotations: 2 | speed: 70
 ├─ MediumMotor.Degrees brake: 0 | port_motor: A | rotations: 240 | speed: 75
 ├─ Motor.Rotations brake: 1 | port_motor: C | rotations: 2 | speed: -70
 ├─ MediumMotor.Degrees brake: 0 | port_motor: A | rotations: 480 | speed: -75
 ├─ Motor.Rotations brake: 1 | port_motor: C | rotations: 2 | speed: 70
 ├─ MediumMotor.Degrees brake: 0 | port_motor: B | rotations: 35 | speed: 15
 ├─ MediumMotor.Degrees brake: 0 | port_motor: A | rotations: 780 | speed: 75
 //e
 ├─ Motor.Rotations brake: 1 | port_motor: C | rotations: 1.5 | speed: 70
 ├─ MediumMotor.Degrees brake: 0 | port_motor: A | rotations: 720 | speed: -75
 ├─ MediumMotor.Degrees brake: 0 | port_motor: B | rotations: 35 | speed: -15
 ├─ Motor.Rotations brake: 1 | port_motor: C | rotations: 2 | speed: 70
 ├─ MediumMotor.Degrees brake: 0 | port_motor: B | rotations: 35 | speed: 15
 ├─ MediumMotor.Degrees brake: 0 | port_motor: A | rotations: 720 | speed: 75
 //_
 ├─ Motor.Rotations brake: 1 | port_motor: C | rotations: 1.5 | speed: 70
 ├─ MediumMotor.Degrees brake: 0 | port_motor: A | rotations: 720 | speed: -75
 ├─ MediumMotor.Degrees brake: 0 | port_motor: B | rotations: 35 | speed: -15
 ├─ Motor.Rotations brake: 1 | port_motor: C | rotations: 2 | speed: 70
 ├─ MediumMotor.Degrees brake: 0 | port_motor: A | rotations: 420 | speed: 75
 ├─ Motor.Rotations brake: 1 | port_motor: C | rotations: 2 | speed: -70
 ├─ MediumMotor.Degrees brake: 0 | port_motor: A | rotations: 800 | speed: -75
 ├─ MediumMotor.Degrees brake: 0 | port_motor: B | rotations: 35 | speed: 15
 ├─ Motor.Rotations brake: 1 | port_motor: C | rotations: 2 | speed: 70
 ├─ MediumMotor.Degrees brake: 0 | port_motor: A | rotations: 1100 | speed: 75
 //p
 ├─ Motor.Rotations brake: 1 | port_motor: C | rotations: 1.5 | speed: 70
 ├─ MediumMotor.Degrees brake: 0 | port_motor: A | rotations: 360 | speed: -75
 ├─ MediumMotor.Degrees brake: 0 | port_motor: B | rotations: 35 | speed: -15
 ├─ MediumMotor.Degrees brake: 0 | port_motor: A | rotations: 400 | speed: -75
 ├─ MediumMotor.Degrees brake: 0 | port_motor: A | rotations: 420 | speed: 75
 ├─ FORK objectid: 22
 │  └─ Motor.Rotations brake: 1 | port_motor: C | rotations: 1.5 | speed: 60
 ├─ MediumMotor.Degrees brake: 0 | port_motor: A | rotations: 120 | speed: 15
 ├─ MediumMotor.Degrees brake: 0 | port_motor: A | rotations: 60 | speed: -75
 ├─ MediumMotor.Degrees brake: 0 | port_motor: B | rotations: 35 | speed: 15
 ├─ MediumMotor.Degrees brake: 0 | port_motor: A | rotations: 280 | speed: 75
 //r
 ├─ Motor.Rotations brake: 1 | port_motor: C | rotations: 1.5 | speed: 70
 ├─ MediumMotor.Degrees brake: 0 | port_motor: B | rotations: 35 | speed: -15
 ├─ MediumMotor.Degrees brake: 0 | port_motor: A | rotations: 180 | speed: -75
 ├─ MediumMotor.Degrees brake: 0 | port_motor: B | rotations: 35 | speed: 15
 ├─ MediumMotor.Degrees brake: 0 | port_motor: A | rotations: 180 | speed: -75
 ├─ MediumMotor.Degrees brake: 0 | port_motor: B | rotations: 35 | speed: -15
 ├─ MediumMotor.Degrees brake: 0 | port_motor: A | rotations: 360 | speed: -75
 ├─ MediumMotor.Degrees brake: 0 | port_motor: B | rotations: 35 | speed: 15
 ├─ MediumMotor.Degrees brake: 0 | port_motor: A | rotations: 720 | speed: 75
 //i
 ├─ Motor.Rotations brake: 1 | port_motor: C | rotations: 1.5 | speed: 70
 ├─ MediumMotor.Degrees brake: 0 | port_motor: A | rotations: 360 | speed: -75
 ├─ MediumMotor.Degrees brake: 0 | port_motor: B | rotations: 35 | speed: -15
 ├─ MediumMotor.Degrees brake: 0 | port_motor: A | rotations: 400 | speed: -75
 ├─ MediumMotor.Degrees brake: 0 | port_motor: A | rotations: 420 | speed: 75
 ├─ FORK objectid: 24
 │  └─ Motor.Rotations brake: 1 | port_motor: C | rotations: 2 | speed: 60
 ├─ MediumMotor.Degrees brake: 0 | port_motor: A | rotations: 120 | speed: 15
 ├─ MediumMotor.Degrees brake: 0 | port_motor: A | rotations: 480 | speed: -75
 ├─ MediumMotor.Degrees brake: 0 | port_motor: B | rotations: 35 | speed: 15
 ├─ MediumMotor.Degrees brake: 0 | port_motor: A | rotations: 700 | speed: 75
 //n
 ├─ Motor.Rotations brake: 1 | port_motor: C | rotations: 1.5 | speed: 70
 ├─ MediumMotor.Degrees brake: 0 | port_motor: A | rotations: 360 | speed: -75
 ├─ MediumMotor.Degrees brake: 0 | port_motor: B | rotations: 35 | speed: -15
 ├─ Motor.Rotations brake: 1 | port_motor: C | rotations: 1.5 | speed: 70
 ├─ MediumMotor.Degrees brake: 0 | port_motor: B | rotations: 35 | speed: 15
 ├─ Motor.Rotations brake: 1 | port_motor: C | rotations: 1 | speed: -70
 ├─ MediumMotor.Degrees brake: 0 | port_motor: A | rotations: 90 | speed: 75
 ├─ MediumMotor.Degrees brake: 0 | port_motor: B | rotations: 35 | speed: -15
 ├─ MediumMotor.Degrees brake: 0 | port_motor: A | rotations: 450 | speed: -75
 ├─ MediumMotor.Degrees brake: 0 | port_motor: B | rotations: 35 | speed: 15
 ├─ MediumMotor.Degrees brake: 0 | port_motor: A | rotations: 720 | speed: 75
 //t
 ├─ Motor.Rotations brake: 1 | port_motor: C | rotations: 2.5 | speed: 70
 ├─ MediumMotor.Degrees brake: 0 | port_motor: A | rotations: 540 | speed: -75
 ├─ MediumMotor.Degrees brake: 0 | port_motor: B | rotations: 35 | speed: -15
 ├─ Motor.Rotations brake: 1 | port_motor: C | rotations: 2 | speed: 70
 ├─ MediumMotor.Degrees brake: 0 | port_motor: A | rotations: 240 | speed: 75
 ├─ Motor.Rotations brake: 1 | port_motor: C | rotations: 2 | speed: -70
 ├─ MediumMotor.Degrees brake: 0 | port_motor: A | rotations: 480 | speed: -75
 ├─ Motor.Rotations brake: 1 | port_motor: C | rotations: 2 | speed: 70
 ├─ MediumMotor.Degrees brake: 0 | port_motor: B | rotations: 35 | speed: 15
 ├─ MediumMotor.Degrees brake: 0 | port_motor: A | rotations: 780 | speed: 75
 //e
 ├─ Motor.Rotations brake: 1 | port_motor: C | rotations: 1.5 | speed: 70
 ├─ MediumMotor.Degrees brake: 0 | port_motor: A | rotations: 360 | speed: -75
 ├─ MediumMotor.Degrees brake: 0 | port_motor: B | rotations: 35 | speed: -15
 ├─ MediumMotor.Degrees brake: 0 | port_motor: A | rotations: 400 | speed: -75
 ├─ MediumMotor.Degrees brake: 0 | port_motor: A | rotations: 420 | speed: 75
 ├─ FORK objectid: 27
 │  └─ Motor.Rotations brake: 1 | port_motor: C | rotations: 1.5 | speed: 60
 ├─ MediumMotor.Degrees brake: 0 | port_motor: A | rotations: 120 | speed: 15
 ├─ MediumMotor.Degrees brake: 0 | port_motor: A | rotations: 60 | speed: -75
 ├─ MediumMotor.Degrees brake: 0 | port_motor: B | rotations: 35 | speed: 15
 ├─ MediumMotor.Degrees brake: 0 | port_motor: A | rotations: 280 | speed: 75
 //r
 ├─ Motor.Rotations brake: 1 | port_motor: C | rotations: 2 | speed: 70
 ├─ MediumMotor.Degrees brake: 0 | port_motor: B | rotations: 35 | speed: -15
 ├─ Motor.Rotations brake: 1 | port_motor: C | rotations: 0.5 | speed: 70
 ├─ MediumMotor.Degrees brake: 0 | port_motor: A | rotations: 300 | speed: -75
 ├─ FORK objectid: 29
 │  ├─ Motor.Rotations brake: 1 | port_motor: C | rotations: 0.3 | speed: 90
 │  └─ Motor.Rotations brake: 1 | port_motor: C | rotations: 0.3 | speed: -90
 ├─ MediumMotor.Degrees brake: 0 | port_motor: A | rotations: 120 | speed: -75
 ├─ MediumMotor.Degrees brake: 0 | port_motor: A | rotations: 300 | speed: -75
 ├─ Motor.Rotations brake: 1 | port_motor: C | rotations: 0.5 | speed: -70
 ├─ MediumMotor.Degrees brake: 0 | port_motor: B | rotations: 35 | speed: 15
 └─ MediumMotor.Degrees brake: 0 | port_motor: A | rotations: 720 | speed: 75
 //}
```

