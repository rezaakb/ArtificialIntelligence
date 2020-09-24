
import numpy as np
a = input().split()

n = int(a[0])
m = int(a[1])
s = int(a[2])-1
t = int(a[3])-1

edges = np.zeros((n,n))
for i in range(m):
    a = input().split()
    edges[int(a[0])-1][int(a[1])-1]=int(a[2])

import heapq

count= np.zeros(n)

B=[]
k=2
heapq.heappush(B, (0,s))
while (len(B)>0 and count[t]<k):
    tmp = heapq.heappop(B)
    c= tmp[0]
    u= tmp[1]
    count[u] = count[u] +1
    if u==t:
        p=c
    if count[u]<=k:
        for i in range(n):
            if edges[u][i]>0:
                c_new = c + edges[u][i]
                heapq.heappush(B, (c_new, i))

print(int(p))
