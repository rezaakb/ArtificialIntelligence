import random

m = int(input())
b = int(input())
c = int(input())

bids = []
list_revenue = []
f=124124124
for i in range(b):
    a = input().split(" ")
    if int(a[0])!=f:
        bids.append([])
        list_revenue.append([])
        f=int(a[0])
    list_revenue[f].append(float(a[1]))
    tmp = map(int, a[2:len(a)-1])
    tmp = list(map(int, tmp))
    bids[f].append(tmp)

each_revenue = [0]*len(list_revenue)
for i in range(len(list_revenue)):
    q=0
    for j in range(len(list_revenue[i])):
        q=q+list_revenue[i][j]
    each_revenue[i]=q

for i in range(len(list_revenue)-1,-1,-1):
    if len(list_revenue[i])==0:
        list_revenue.remove(list_revenue[i])
        bids.remove(bids[i])
    else:
        break



k=0

import time


def initial(bids):
    revenue =0
    list_selected = []
    list_bids = [0] * len(bids)
    for i in range(len(bids)):
        tmp  = random.randint(0,(len(bids[i])-1))
        p = random.random()
        if p > min(list_revenue[i][tmp]*len(list_revenue[i])/each_revenue[i],0.8):
            list_bids[i] = 9009000
            continue
        if len(set(list_selected).intersection(set(bids[i][tmp]))) ==0:
            list_selected = list_selected + bids[i][tmp]
            revenue = revenue + list_revenue[i][tmp]
            list_bids[i] = tmp
        else:
            list_bids[i] = 9009000

    return  list_bids,list_selected,revenue



def randomlySelectSuccessorWithRevenue(list_selected,list_region,bids,q):
    list_selected_region = list_region[:]
    list_selected_bids = list_selected[:]
    revenue =0
    for i in range(len(bids)):
        tmp  = random.randint(0,(len(bids[i])-1))
        p = random.random()
        if p < q:
            if list_selected_bids[i] != 9009000:
                revenue = revenue + list_revenue[i][list_selected_bids[i]]
            continue
        if tmp == list_selected_bids[i]:
            tmp = (tmp +1)%(len(bids[i]))
        if list_selected_bids[i] !=9009000:
            for j in range(len(bids[i][list_selected_bids[i]])):
                list_selected_region.remove(bids[i][list_selected_bids[i]][j])

        if len(set(list_selected_region).intersection(set(bids[i][tmp]))) ==0:
            list_selected_region = list_selected_region + bids[i][tmp]
            revenue = revenue + list_revenue[i][tmp]
            list_selected_bids[i] = tmp
        else:
            list_selected_bids[i] = 9009000

    return  list_selected_bids,list_selected_region,revenue


revenue = 0
w = 0
bests = []
#list_selected_bids,list_selected_region, new_revenue = initial(bids)
list_selected = []
list_region = []
for i in range(3):
    revenue= 0
    end_time = time.perf_counter() + 1.4
    while time.perf_counter() < end_time:
        list_selected_bids, list_selected_region, new_revenue = initial(bids)
        e = new_revenue - revenue
        if (e>0):
            list_selected = list_selected_bids[:]
            list_region = list_selected_region[:]
            revenue=new_revenue
    q=0.3
    end_time = time.perf_counter() + 1.4
    while time.perf_counter() < end_time:
        list_selected_bids,list_selected_region, new_revenue = randomlySelectSuccessorWithRevenue(list_selected,list_region,bids,q)
        e = new_revenue - revenue
        q = q * (1.001)
        if (e>0):
            list_selected = list_selected_bids[:]
            list_region = list_selected_region[:]
            revenue=new_revenue
    bests.append([revenue, list_selected.copy()])
    #print(i,q)
#print(revenue)
#print(q)
#print(w)
#print(bests[0][0],bests[1][0],bests[2][0])
#print(bests[0][1])
#print(bests[1][1])#,bests[2][0],bests[3][0])
#print(bests[2][1])#,bests[2][0],bests[3][0])
#print(bests[3][1])#,bests[2][0],bests[3][0])

maxi = -10000
for i in range(3):
    if bests[i][0]>maxi:
        ii=i
        maxi = bests[i][0]

list_selected = bests[ii][1]
string = ""
f=0
for i in range(len(list_selected)):
    if list_selected[i]!=9009000:
        string = string + str(list_selected[i]+f) + " "
    f = f + len(bids[i])
string = string + '#'
print(string)
