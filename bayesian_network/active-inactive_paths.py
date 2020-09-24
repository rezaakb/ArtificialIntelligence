
from collections import defaultdict

class Graph:

    def __init__(self, vertices):
        self.V = vertices
        self.graph = defaultdict(list)
        self.actualGraph = defaultdict(list)
        self.evidence = [False] * (self.V+1)
        self.activePath = []
        self.inActivePath = []


    def addEdge(self, u, v):
        self.graph[u].append(v)
        self.graph[v].append(u)
        self.actualGraph[u].append(v)

    def getActivePath(self):
        return self.activePath

    def getInActivePath(self):
        return self.inActivePath

    def markedEvidence(self,i):
        self.evidence[i]=True

    def checkIndependencyIteration(self, u, d, visited, path):
        visited[u] = True
        path.append(u)
        if u == d:
            if (len(path)>=3):
                if self.checkInAcitvePath(path):
                    self.inActivePath.append(path[:])
                else:
                    self.activePath.append(path[:])
            else:
                self.activePath.append(path[:])
        else:
            for i in self.graph[u]:
                if visited[i] == False:
                    self.checkIndependencyIteration(i, d, visited, path)
        path.pop()
        visited[u] = False

    def checkIndependency(self, s, d):
        visited = [False] * (self.V+1)
        path = []
        self.checkIndependencyIteration(s, d, visited, path)

    def checkInAcitvePath(self, path):
        for i in range(len(path)-2):
            # state 1
            if path[i+1] in self.actualGraph[path[i]] and path[i+2] in self.actualGraph[path[i+1]] and self.evidence[path[i+1]]:
                return True
            # state 2
            if path[i] in self.actualGraph[path[i+1]] and path[i + 2] in self.actualGraph[path[i + 1]] and self.evidence[path[i + 1]]:
                return True
            # state 3
            if path[i+1] in self.actualGraph[path[i]] and path[i + 1] in self.actualGraph[path[i + 2]]:
                if self.checkState3(path[i+1]):
                    return True
        return False

    def checkState3(self, s):
        visited = [False for i in range(self.V+1)]
        stack = []
        stack.append(s)
        while (len(stack)):

            s = stack[-1]
            if self.evidence[s]:
                return False
            stack.pop()

            if (not visited[s]):
                visited[s] = True

            for node in self.actualGraph[s]:
                if (not visited[node]):
                    stack.append(node)
        return True



a = input().split(" ")
n = int(a[0])
m = int(a[1])
z = int(a[2])

g = Graph(n)

for i in range(m):
    a = input().split(" ")
    node1 = int(a[0])
    node2 = int(a[1])
    g.addEdge(node1,node2)

for i in range(z):
    g.markedEvidence(int(input()))

a = input().split(" ")
x = int(a[0])
y = int(a[1])

g.checkIndependency(x,y)

activePath = g.getActivePath()
inActivePath = g.getInActivePath()

if len(activePath)==0:
    print("independent")
else:
    string=""
    for i in range(len(activePath[0])):
        if i ==len(activePath[0])-1:
            string = string +str(activePath[0][i])
        else:
            string = string +str(activePath[0][i])+", "
    print(string)