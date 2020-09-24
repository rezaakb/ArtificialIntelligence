import numpy as np
import random
from numpy.random import default_rng

n = int(input())

m = int(input())

edges = np.zeros((n,n))

for i in range(m):
    tmp = input().split()
    edges[int(tmp[0])-1][int(tmp[1])-1]=1
    edges[int(tmp[1])-1][int(tmp[0])-1]=1


def calculateCost(l, r, edges):
    tmp = edges[l]
    tmp2 = tmp[:,r]
    return np.sum(tmp2)


def swap(l, r,n):
    index1=np.random.randint(n//2)
    index2=np.random.randint(n//2)
    l_new = np.zeros(n//2,dtype=int)
    r_new = np.zeros(n//2,dtype=int)

    l_new[:] = l[:]
    r_new[:] = r[:]

    c=l_new[index1]
    l_new[index1]=r_new[index2]
    r_new[index2]=c
    return l_new,r_new

nodes = np.arange(n)
rng = default_rng()
l = rng.choice(n, size=n//2, replace=False)
r = np.delete(nodes, l)
cost = calculateCost(l,r,edges)
i=0

import time

t_end = time.time() + 60 * 4.9
t=100
i=0
while time.time() < t_end:
    t = t*0.9999
    i=i+1
    if t<0.0005:
        break
    l_new,r_new = swap(l,r,n)
    cost_new = calculateCost(l_new,r_new,edges)
    e = cost_new - cost
    if (e<0):
        l = l_new
        r = r_new
        cost=cost_new
    else:
        tmp =np.exp(-e/t)
        condition  = random.random() < tmp
        if condition:
            l = l_new
            r = r_new
            cost = cost_new


#print resualt
print(int(cost))
l=np.sort(l)+1
r=np.sort(r)+1
for i in range(len(l)):
    if (i==len(l)-1):
        print(l[i])
    else:
        print(l[i], end=" ")

for i in range(len(r)):
    if (i == len(r) - 1):
        print(r[i])
    else:
        print(r[i], end=" ")
