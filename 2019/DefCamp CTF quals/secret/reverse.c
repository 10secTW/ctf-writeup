void main()
{
  char buf [72];
  
  setvbuf(stdin, 0, 2, 0);
  setvbuf(stdout, 0, 2, 0);
  memset(buf, 0, 64);
  printf("Enter your name?\nName: ");
  read(0, buf, 64);
  printf("Hillo ");
  printf(buf); // fsb
  secret();
  return 0;
}


void secret()
{
  char buf[136];
  
  printf("Enter secret phrase !\nPhrase: ");
  gets(buf); // bof
  printf("Entered secret > %s .\n",buf);
  
  if (!strcmp(buf,"supersecretdctf2019"))
    puts("\nYou entered the same string two times");
  else 
    puts("\nEntered strings are not same!");
}

