11    ALLOC(60);
      GPTR[0] = "*************************************\n"
1343  PRSTRI(0)
      GPTR[0] = "*                                   *\n"
2072  PRSTRI(0);
      GPTR[0] = "*             Welcome to            *\n"
3218  PRSTRI(0);
      GPTR[0] = "*        EmojiVM 😀😁🤣🤔🤨😮       *\n"
4019  PRSTRI(0);
      GPTR[0] = "*       The Reverse Challenge       *\n"
4685  PRSTRI(0);
      GPTR[0] = "*                                   *\n"
5351  PRSTRI(0);
      GPTR[0] = "*************************************\n"
5375  PRSTRI(0);
      GPTR[0] = "Please input the secret:"
5953  PRSTRI(0);

5962  ALLOC(30);
5971  ALLOC(30);
5980  ALLOC(30);
5989  ALLOC(30);
GPTR[2] = [24, 5, 29, 16, 66, 9, 74, 36, 0, 91, 8, 23, 64, 0, 114, 48, 9, 108, 86, 64, 9, 91, 5, 26, 0]
GPTR[4] = [142, 99, 205, 18, 75, 88, 21, 23, 81, 34, 217, 4, 81, 44, 25, 21, 134, 44, 209, 76, 132, 46, 32, 6, 0]

6810  RDSTRI(1);
6813  ALLOC(5); # alloc5

@l1:
6818  if(GPTR[GPTR[5, 1], 1] == 0)
6854    GOTO 7052;
6874  if(gptr[1, gptr[5, 1]] == 10)
6910    GOTO @l2;
6930  GPTR[5, 0] += 1;
6939  GPTR[5, 1] += 1;
6981  GOTO @l1;

@l2:
7003  GPTR[GPTR[5, 1], 1] = 0;
7036  GOTO @l3;

@l3:
7056  if(GPTR[5, 0] + 24 != 0);
7095    GOTO @fail;
7117  GPTR[5, 1] = 0;

@l4;
7124  if((GPTR[5, 1] + 1) % 5 == 0)
7161    GOTO 7294;

@l5:
7181  GPTR[5, 1] += 1;
7202  if(GPTR[5, 1] < 24);
7233    GOTO @l4;
7278  GOTO @l7;        # goto 7401

@l6:
7306  if(GPTR[GPTR[5, 1], 1] != 45)
7340    GOTO @fail;
7385  GOTO @l5;

@l7;
7407  GPTR[5, 1] = 0;

@l8
7408  GPTR[5, 2] = GPTR[5, 1] % 4;
7425  if(GPTR[5, 2] == 0)
7458    GOTO @l10;
7474  if(GPTR[5, 2] == 1)
7511    GOTO @l11;
7527  if(GPTR[5, 2] == 2)
7564    GOTO @l12;
7580  if(GPTR[5, 2] == 3)
7617    GOTO @l13;

@l9
7633  GPTR[5, 1] += 1
7658  if(GPTR[5, 1] < 24)
7689    GOTO @l8;
7705  GOTO @l14;

@l10
7774  GPTR[3, GPTR[5, 1]] = GPTR[1, GPTR[5, 1]] + 30;
7804  GOTO @l9;

@l11
7826  GPTR[3, GPTR[5, 1]] = 7 ^ (GPTR[1, GPTR[5, 1]] - 8);
7871  GOTO @l9;

@l12
7920  GPTR[3, GPTR[5, 1]] = (GPTR[1, GPTR[5, 1]] + 44 ^ 68) - 4;
7953  GOTO @l9;

@l13
7973  GPTR[3, GPTR[5, 1]] = (GPTR[1, GPTR[5, 1]] ^ 101) ^ (172 & 20)
8059  GOTO @l9;

@l14
8075  GPTR[5, 1] = 0
8082  GPTR[5, 2] = 0
@l15:
8093  if(GPTR[3, GPTR[5, 1]] == GPTR[4, GPTR[5, 1]])
8135    GOTO @l17;
8160  GPTR[5, 2] -= 1;

@l16:
8179  GPTR[5, 1] += 1;
8192  if(GPTR[5, 1] < 24)
8223    GOTO @l15;
8268  GOTO @l18;

@l17:
8290  GPTR[5, 2] += 1;
8326  GOTO @l16;

@l18;
8346  if(GPTR[5, 2] != 24);
8385    GOTO @fail;
8407  GPTR[5, 1] = 0;

@l19:
8429  GPTR[2, GPTR[5, 1]] = GPTR[1, GPTR[5, 1]] ^ GPTR[2, GPTR[5, 1]];
8437  GPTR[5, 1] += 1;
8458  if(GPTR[5, 1] < 24)
8489    GOTO @l19;
8534  GOTO @correct;

@fail:
      GPTR[0] = "\xf0\x9f\x98\xad\n"
      PRSTRI(0)
8684  GOTO @exit;

@correct:
      GPTR[0] = "\xf0\x9f\x98\x8d\n"
      PRSTRI(0)
8807  PRSTRI(2);
      GPTR[0] = "\n"
8824  PRSTRI(0);
8825  EXIT;   # @exit
