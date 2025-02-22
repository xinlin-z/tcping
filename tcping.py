#!/usr/bin/env python3
"""
tcping by connect in Python

Author:   xinlin-z
Github:   https://github.com/xinlin-z/tcping
Blog:     https://CS4096.com
License:  MIT
"""
import sys
import socket
from time import sleep
from time import monotonic as time
from datetime import datetime
import argparse
import math


def cprint(*objects, sep=' ', end='\n', file=sys.stdout,
           flush=False, fg=None, bg=None, style='default'):
    """ colorful print.
    Color and style the text and background, then call the print function,
    Eg: cprint('cs4096.com', fg='red', bg='green', style='blink')
    The other parameters are the same with stand print!
    """
    def _ct(code='0'):
        return '\033[%sm'%code

    # text color
    c = 37
    if fg in ('red','r'): c = 31
    elif fg in ('green','g'): c = 32
    elif fg in ('yellow','y'): c = 33
    elif fg in ('blue','b'): c = 34
    elif fg in ('magenta','m'): c = 35
    elif fg in ('cyan','c'): c = 36
    elif fg in ('white','w'): c = 37
    elif fg in ('black','k'): c = 30
    # background color
    b = 40
    if bg in ('red','r'): b = 41
    elif bg in ('green','g'): b = 42
    elif bg in ('yellow','y'): b = 43
    elif bg in ('blue','b'): b = 44
    elif bg in ('magenta','m'): b = 45
    elif bg in ('cyan','c'): b = 46
    elif bg in ('white','w'): b = 47
    elif bg in ('black','k'): b = 40
    # style
    a = 0
    if style == 'underline': a = 4
    elif style == 'blink': a = 5
    elif style == 'inverse': a = 7

    string = sep.join(map(str, objects))
    color = '%d;%d;%d' % (a,c,b)
    print(_ct(color)+string+_ct(), sep=sep, end=end, file=file, flush=flush)


def mean(lst):
    return 0 if len(lst)==0 else round(sum(lst)/len(lst), 3)


def median(lst):
    if(n:=len(lst)) == 0:
        return 0
    a = lst[:]
    m = n // 2
    a.sort()
    md = a[m] if n%2 else (a[m-1]+a[m])/2
    return round(md, 3)


def std(lst):
    if(n:=len(lst)) <= 1:
        return 0
    m = mean(lst)
    var = sum((i-m)**2 for i in lst) / (n-1)
    return round(math.sqrt(var), 3)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-V', '--version', action='version',
        version='tcping by xinlin-z (https://github.com/xinlin-z/tcping)')
    parser.add_argument('host', help='ip or FQDN')
    parser.add_argument('port', type=int, help='port number')
    parser.add_argument('-n', type=int, default=4,
                        help='tcping count, 0 means infinity')
    parser.add_argument('-i', type=float, default=0.5,
                        help='tcping interval in second')
    parser.add_argument('-t', type=float, default=3.0,
                        help='tcping timeout in second')
    args = parser.parse_args()

    try:
        ips = [t[4][0] for t in socket.getaddrinfo(args.host.strip(),
                                                   None,
                                                   socket.AF_INET,
                                                   socket.SOCK_STREAM)]
    except Exception as e:
        print(repr(e))
        sys.exit(1)

    if args.n < 0:
        args.n = 4
    if args.i < 0:
        args.i = 0.5
    if args.t < 0:
        args.t = 3.0

    print('# tcping by connect')
    print('# ip:', str(ips), ', port:', args.port)
    print('# count:', args.n if args.n else 'infinity')
    print('# interval:', str(args.i)+'s')
    print('# timeout:', str(args.t)+'s')
    for ip in ips:
        print('tcping', ip+':'+str(args.port))
        i = 0
        cts = []
        while True:
            try:
                s = socket.socket()
                s.settimeout(args.t)
                tic = time()
                s.connect((ip,args.port))
                toc = time()
                conntime = (toc-tic)*1000
                s.close()
                cts.append(conntime)
                msg = str(round(conntime,3))+'ms'
            except ConnectionRefusedError:
                msg = 'connection refused'
            except socket.timeout:
                msg = f'timeout(>{args.t*1000}ms)'

            i += 1
            ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
            print(f'\r[{ts} tcping {ip}:{args.port} {i}/{args.n}]',msg)
            cprint(f'> data:{len(cts)}, std:{std(cts)}, '
                   f'mean:{mean(cts)}, median:{median(cts)}  ',
                   end='', flush=True, fg='w', bg='b')

            if i != args.n:
                sleep(args.i)
            else:
                print()
                break

