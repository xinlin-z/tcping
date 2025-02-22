#!/usr/bin/env python3
"""
tcping by connect in Python

Author:   xinlin-z
Github:   https://github.com/xinlin-z/tcping
Blog:     https://CS4096.com
License:  MIT
"""
import socket
from time import sleep
from time import monotonic as time
from datetime import datetime
import argparse
import math


def mean(lst):
    assert len(lst) >= 1
    return round(sum(lst)/len(lst), 3)


def median(lst):
    assert len(lst) >= 1
    a = lst[:]
    n = len(a)
    m = n // 2
    a.sort()
    md = a[m] if n%2 else (a[m-1]+a[m])/2
    return round(md, 3)


def std(lst):
    assert len(lst) >= 1
    if (n:=len(lst)) == 1:
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

    ips = [t[4][0] for t in socket.getaddrinfo(args.host.strip(),
                                               None,
                                               socket.AF_INET,
                                               socket.SOCK_STREAM)]
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
        while True:
            try:
                s = socket.socket()
                s.settimeout(args.t)
                tic = time()
                s.connect((ip,args.port))
                toc = time()
                conntime = toc - tic
                s.close()
                msg = str(round(conntime*1000,3))+'ms'
            except ConnectionRefusedError:
                msg = 'connection refused'
            except socket.timeout:
                msg = f'timeout(>{args.t*1000}ms)'

            i += 1
            ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
            print(f'[{ts} tcping {ip}:{args.port} {i}/{args.n}]',msg)

            if i != args.n:
                sleep(args.i)
            else:
                break

