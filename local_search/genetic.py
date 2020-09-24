
import numpy as np
import random
from numpy.random import default_rng

import time
t_end = time.time() + 60 * 4.5

n = int(input())
v = input().split(", ")
k = int(input())
x= [None] * k
max=-10
for i in range(k):
    tmp = input()
    size = len(tmp)
    l = np.array([None] * size)
    q= np.array([char for char in tmp])
    for j in range(n):
        a = q==v[j]
        l[a]=j
    x[i]= l
    if len(x[i])>max:
        max=len(x[i])

mc = np.zeros((n+1,n+1),dtype=int)
cc = int(input())
for i in range(n+1):
    tmp = list(map(int, input().split()))
    mc[i,:]=tmp[:]

N=max
rng = default_rng()

def makeRandomGene(x,N):
    x_new = []
    for i in range(k):
        l = rng.choice(N, size=N-len(x[i]), replace=False)
        x_new.append(l)
    return x_new


def calculateFitness(l,x,N):
    sum_fit=0
    range_N=range(N)
    x_new = np.zeros((k,N),dtype=int)
    for i in range(len(x)):
        r = np.delete(range_N, l[i])
        x_new[i,l[i]]=n
        x_new[i,r]=x[i][:]

    for i in range(len(x)):
        if i==len(x)-1:
            break
        for j in range(i+1,len(x)):
            a=mc[x_new[i][:],x_new[j][:]]
            sum_fit=np.sum(a)+sum_fit
    return sum_fit

population = 20

def initialList(N):
    initial_list = [None] * population
    for i in range(population):
        tmp = makeRandomGene(x,N)
        initial_list[i] = (tmp,calculateFitness(tmp,x,N))
    initial_list.sort(key = lambda x: x[1])
    ni = np.zeros(k,dtype=int)
    for i in range(k):
        ni[i]= N-len(x[i])
    conversion_cost = np.sum(ni)*cc
    return initial_list,conversion_cost

minimum=10000000
ress=0
def iteration(initial_list, x, N,minimum,resualt,conversion_cost):

    #selection
    q1 = rng.choice(3, size=10)
    q2 = rng.choice(17,size=10)+3
    q = []
    q.extend(q1)
    q.extend(q2)
    random.shuffle(q)
    selection = [None] *population

    #crossover
    for i in range(0,20,2):
        j = random.randint(-1,2)+k//2
        selection[i]= [None]*k
        selection[i][0:j]=initial_list[q[i]][0][0:j]
        selection[i][j:k]=initial_list[q[i+1]][0][j:k]

        selection[i+1] = [None] * k
        selection[i+1][0:j] = initial_list[q[i+1]][0][0:j]
        selection[i+1][j:k] = initial_list[q[i]][0][j:k]

    #mutation
    q = rng.choice(20, size=4)
    for i in range(4):
        p = random.randint(-1,1)
        one = np.ones_like(selection[q[i]])
        selection[q[i]] = selection[q[i]] +one*p
        selection[q[i]] = selection[q[i]]%N

    #calculate fitness
    initial_list = [None] * population
    for i in range(population):
        tmp = selection[i]
        initial_list[i] = (tmp, calculateFitness(tmp, x,N))
    initial_list.sort(key=lambda x: x[1])

    #save best resualt
    if initial_list[0][1]+conversion_cost<minimum:
        minimum = initial_list[0][1]+conversion_cost
        resualt = initial_list[0][0]
    return initial_list,minimum,resualt

o=0


final =[]
z=0
resualt=None
while time.time() < t_end:
    initial_list,conversion_cost = initialList(N)
    f=0
    o=0
    while o<1000:
        initial_list,minimum,resualt= iteration(initial_list,x,N,minimum,resualt,conversion_cost)
        o=o+1

        #check time
        if o%20==0:
            if time.time() > t_end:
                break
    N=N+1


#show resualt
N= len(x[0])+len(resualt[0])
range_N = range(N)
x_new = np.zeros((k, N), dtype=int)
print(minimum)
v.append("-")
for i in range(len(x)):
    r = np.delete(range_N, resualt[i])
    x_new[i, resualt[i]] = n
    x_new[i, r] = x[i][:]
    string=""
    for j in range(N):
        string=string+v[x_new[i][j]]
    print(string)