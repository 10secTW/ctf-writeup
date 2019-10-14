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
6818  if(GPTR[1, i] == 0)
6854    GOTO @l3;
6874  if(GPTR[1, i] == 10)
6910    GOTO @l2;
6930  GPTR[5, 0] += 1;
6939  i += 1;
6981  GOTO @l1;

@l2:
7003  GPTR[1, i] = 0;
7036  GOTO @l3;

@l3:
7056  if(GPTR[5, 0] == 24)
7095    GOTO @fail;
7117  i = 0;
      do {
7118    if( (i + 1) % 5 == 0 && GPTR[1, i] != 45 )
7340      GOTO @fail;
7181    i += 1;
7202  } while(i < 24);
7407  i = 0;
      do {
7408    off = i % 4;
7425    if(off == 0)
          GPTR[3, i] = GPTR[1, i] + 30;
7474    else if(off == 1)
          GPTR[3, i] = 7 ^ (GPTR[1, i] - 8);
7527    else if(off == 2)
          GPTR[3, i] = ((GPTR[1, i] + 44) ^ 68) - 4;
7580    else if(off == 3)
          GPTR[3, i] = (GPTR[1, i] ^ 101) ^ (172 & 20)
7633    i += 1
7658  } while(i < 24)
8075  i = 0
8084  off = 0
      do {
8093    if(GPTR[3, i] == GPTR[4, i]) {
8135      off += 1;
        } else {
8160      off -= 1;
        }
8179    i += 1;
8192  } while(i < 24)
8346  if(off != 24);
8385    GOTO @fail;
8407  i = 0;
      do {
8429    GPTR[2, i] = GPTR[1, i] ^ GPTR[2, i];
8437    i += 1;
8458  while(i < 24);
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
