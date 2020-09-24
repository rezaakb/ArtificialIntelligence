import numpy as np

a = input().split(" ")
m = int(a[0])
n = int(a[1])
board = np.zeros((m,n))
k=0
packman = []
for i in range(m):
    a=input().split(" ")
    for j in range(n):
        if int(a[j])==1:
            board[i,j] = True
        if int(a[j])==2:
            board[i,j] = False
        if int(a[j])==3:
            board[i, j] = True
            packman.append([i,j])
            k=k+1

first_state = np.array(packman)

from collections import defaultdict

class Graph:

    def __init__(self):
        self.graph = defaultdict(list)

    def findEdges(self,board):
        m = len(board)
        n = len(board[0])
        for i in range(m):
            for j in range(n):
                if board[i,j]==False:
                    continue
                if board[(i+1)%m,j] and i+1<m:
                    self.graph[(i,j)].append((i+1,j))
                    self.graph[(i+1,j)].append((i,j))
                if board[(i-1)%m,j] and i-1>-1:
                    self.graph[(i,j)].append((i-1,j))
                    self.graph[(i-1,j)].append((i,j))
                if board[i , (j+ 1) % n] and j + 1 < n:
                    self.graph[(i,j+1)].append((i,j))
                    self.graph[(i,j)].append((i,j+1))
                if board[i, (j - 1) % n] and j-1 > -1:
                    self.graph[(i, j - 1)].append((i, j))
                    self.graph[(i, j)].append((i, j - 1))


    def BFS(self, i2,j2):
        visited = np.zeros_like(board)
        level = np.ones_like(board)*112341234
        queue = []
        queue.append((i2,j2))
        level[i2,j2]= 0
        visited[i2,j2] = True
        w = 0
        while queue:
            i1,j1 = queue.pop(0)
            w = w+1
            for i,j in self.graph[i1,j1]:
                if visited[i,j] == False:
                    queue.append((i,j))
                    visited[i,j] = True
                    level[i,j] = level[i1,j1]+1
        return level


g = Graph()
g.findEdges(board)
max_iter = np.zeros_like(board)
for i in range(len(packman)):
    d = g.BFS(packman[i][0],packman[i][1])
    max_iter[d>max_iter]=d[d>max_iter]

print(int(np.min(max_iter[board==True])))