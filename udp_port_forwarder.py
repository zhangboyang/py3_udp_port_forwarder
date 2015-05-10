#!/usr/bin/python3
#  UDP port forwarder by ZBY 20150509
#  user1   Lport           Rport   user2
#  addrC <=======> addrL <=======> addrR
#               sockL sockR

L = ('::', '10800')
R = ('127.0.0.1', '10800')
TIMEINTERVAL = 1
BUFSIZE = 65536

from socket import SOCK_DGRAM, socket, getaddrinfo
from select import select
from time import time

# query address
afL, stL, pL, cL, addrL = getaddrinfo(L[0], L[1], type = SOCK_DGRAM)[0]
afR, stR, pR, cR, addrR = getaddrinfo(R[0], R[1], type = SOCK_DGRAM)[0]

# print query result
maxiplen = max(len(addrL[0]), len(addrR[0]))
print('L: ip=%-*s port=%s'%(maxiplen, addrL[0], addrL[1]))
print('R: ip=%-*s port=%s'%(maxiplen, addrR[0], addrR[1]))
print()

# setup socket
sockL, sockR = socket(afL, stL), socket(afR, stR)
fdL, fdR = sockL.fileno(), sockR.fileno()

# bind socket
sockL.bind(addrL)

# server loop
ddl = time() + TIMEINTERVAL
cntL, cntR, lenL, lenR = 0, 0, 0, 0
while True:
    for fd in select([fdL, fdR], [], [], max(0, ddl - time()))[0]:
        if fd == fdL:
            data, addrC = sockL.recvfrom(BUFSIZE)
            sockR.sendto(data, addrR)
            lenL += len(data)
            cntL += 1
        elif fd == fdR:
            data = sockR.recv(BUFSIZE)
            sockL.sendto(data, addrC)
            lenR += len(data)
            cntR += 1
    if time() >= ddl:
        print('[%.3f]'%time(), end=' ')
        print('cntL=%d, cntR=%d'%(cntL, cntR), end=', ')
        print('lenL=%d, lenR=%d'%(lenL, lenR))
        cntL, cntR, lenL, lenR = 0, 0, 0, 0
        ddl += TIMEINTERVAL

