#!/usr/bin/env python3
import sys

BRANCH_DB = {
    '': ('', True),
    'eae': ('# main if ( argc <= 1 )', True),
    '610': ('# printf@plt', False),
    '620': ('# calloc@plt', False),
    '630': ('# malloc@plt', False),
    'e87': ('\n# formula_parse while( *f )', False),
    'be9': ('# formula_parse if ( *f == \',\' )', True),
    'c1c': ('# formula_parse if ( chr <= \'/\' )', False),
    'c22': ('# formula_parse if ( chr > \'9\' )', False),
    'bef': ('# formula_parse ( type == 1 )', True),
    '93e': ('# push if ( s->len > 999u )', False),
    'c58': ('# formula_parse switch case \'+\':', True),
    'caf': ('# formula_parse switch case \'-\':', True),
    'd06': ('# formula_parse switch case \'*\':', True),
    'd5d': ('# formula_parse switch case \'m\':', True),
    'db4': ('# formula_parse switch case \'M\':', True),
    '8dc': ('# pop if ( !a1->len )', True),
    'a81': ('# mul for( ; a2 > i; )', False),
    'a1f': ('# add for( ; op2 % 10 > i; )', False)
}

UNCOND = ['bd6', 'c4f', 'c13', 'ca6', 'cfd', 'd54', 'dab', 'e02', 'e56', 'a5b', 'a0b']


def main():
    with open(sys.argv[1]) as f:
        inp = f.read()

    true = True
    false = False
    trace = eval(inp)

    for inst in trace:
        if inst['event'] != 'branch' and inst['event'] != 'exit':
            continue
        if inst['event'] == 'exit':
            print('# exit')
            return
        
        addr = inst['inst_addr'][-3:]
        if addr in UNCOND:
            print('# Unconditional')
            continue
        taken = inst['branch_taken']
        if addr in BRANCH_DB:
            desc, negate = BRANCH_DB[addr]
            cond = taken
            if negate:
                cond = not cond
            print(desc, cond)


if __name__ == '__main__':
    main()

