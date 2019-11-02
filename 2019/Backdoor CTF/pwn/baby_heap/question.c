// g_note 0x602120
// g_size 0x6020e0
// g_quata 0x602088 // 8

void main()
{ 
    alarm(0x3c);
    mallopt(1,0);
    setvbuf(stdout,(char *)0x0,2,0);
    setvbuf(stdin,(char *)0x0,2,0);
    setvbuf(stderr,(char *)0x0,2,0);
    puts("----------DATA BANK----------");
    
    while( true ) {
        op = menu();
        switch(op){
            case 1:
                add();
                break;

            case 2:
                edit();
                break;

            case 3:
                remove();

            case 4:
                exit(0);

            default:
                puts("Invalid");
                break;
        }
    }
}


void menu()
{
    puts("1) Add data\n2) Edit data\n3) Remove data\n4) Exit");
    printf(">> ");
    read();
}


void read()
{
    char local_38 [40];
    __read(local_38,0x20);
    atoi(local_38);
}


ulong __read(void *param_1,int param_2)
{ 
    sVar2 = read(0,param_1,(long)param_2);
    op = (int)sVar2;
    if (op == -1)
        exit(0);

    if (*(char *)((long)param_1 + (long)op + -1) == '\n')
        *(undefined *)((long)param_1 + (long)op + -1) = 0;
  
    return (ulong)(op - 1);
}


void edit()
{
    puts("Enter the index:");
    idx = _read();
    if (-1 < idx && idx < 12) {
        if (!g_note[idx])
            puts("The index is empty\n");
        else {
            puts("Please update the data:");
            result = __read(g_note[idx], g_size[idx]);

            if (result == 0) 
                puts("update unsuccessful");  
            else 
                puts("update successful\n");
        }
    }
}


void add()
{
    puts("Enter the index:");
    op = _read();
    while( true ) {
        if (op < 0 ||op > 11)
          return;
        
        if (!g_note[idx]) {
            puts("The idx is occupied\n");
            return;
        }

        puts("Enter the size:");
        g_size[idx] = _read();

        if ( -1 < g_size[idx] && g_size[idx] < 0x401) break;
            puts("Invalid size");
        
        g_note[idx] = malloc(g_size[idx]);
        if (!g_note[idx])
            puts("malloc_error");
        else {
            puts("Enter data:");
            __read(g_note[idx], g_size[idx]);
        }
    }
}


void remove()
{ 
    puts("Enter the index:");
    idx = _read();
    while( true ) {
        if (op < 0 || op > 11) return;
        
        if (!g_note[idx]) {
            puts("The index is empty");
            return;
        }
        
        if (g_quata != 0) break;
        g_quata --;
        puts("Sorry no more removal\n"); // wtf ?? not exit
    }
    
    g_quata = g_quata + -1;
    free(g_note[idx]); // uaf
    puts("done");
}