from collections import defaultdict


class Graph:

    def __init__(self, vertices):
        self.V = vertices
        self.graph = defaultdict(list)
        self.domain = defaultdict(list)
        self.actualGraph = defaultdict(list)



    def addEdge(self, u, v):
        self.graph[u].append(v)
        self.graph[v].append(u)
        self.actualGraph[u].append(v)

    def addDomain(self, v, list):
        self.domain[v]=list

    def getAllDomain(self):
        return self.domain

    def getDomain(self,v):
        return self.domain[v]

    def getNeighbor(self,v):
        return self.graph[v]


    def checkState3(self, s):
        visited = [False for i in range(self.V)]
        stack = []
        stack.append(s)
        while (len(stack)):

            s = stack[-1]
            if self.evidence[s]:
                return False
            stack.pop()

            if (not visited[s]):
                print(s, end=' ')
                visited[s] = True

            for node in self.adj[s]:
                if (not visited[node]):
                    stack.append(node)
        return True

    def sortedWithDegree(self):
        tmp = {k: k for k, v in sorted(self.graph.items(), key=lambda item: len(item[1]))}
        tmp = list(tmp.values())[::-1]
        return tmp



a = input().split(" ")
n = int(a[0])
m = int(a[1])
k = int(a[2])

g = Graph(m)



# first arc consistency
for i in range(n):
    tmp = input().split(" ")
    tmp = map(int, tmp)
    tmp = list(map(int, tmp))
    g.addDomain(i+1,tmp)


for i in range(m):
    tmp = input().split(" ")
    g.addEdge(int(tmp[0]),int(tmp[1]))

assignment = []


def selectUnassignedVariable(assignment):

    return len(assignment)


def AC3(assignment):
    domain = list(g.getAllDomain().values())[:][:]
    for i  in range(1,n+1):
        for j in range(len(assignment)):
            if i==assignment[j][0]:
                domain[i-1]=[assignment[j][1]]
                for k in g.getNeighbor(i):
                    if assignment[j][1] in domain[k-1]:
                        tmp = assignment[j][1]
                        tmp1 = domain[k-1][:]
                        tmp1.remove(tmp)
                        domain[k - 1] = tmp1
                break
        if len(domain[i-1])==0:
            return False
    return True


def consistent(assignment, j,i):
    for k in range(len(assignment)):
        if assignment[k][0] in g.getNeighbor(j):
            if assignment[k][1] == i:
                return False
    return True

orderVariable = g.sortedWithDegree()

def backtracking(assignment):
    if len(assignment) == n:
        return assignment
    j = orderVariable[len(assignment)]
    domain = g.getDomain(j)
    for i in domain:
        if consistent(assignment, j,i):
            assignment.append((j,i))
            inferences = AC3(assignment)
            if inferences != False:
                resualt = backtracking(assignment)
                if resualt != False:
                    return resualt
            assignment.remove((j, i))
    return False

resualt = backtracking([])
if resualt !=False:
    resualt.sort()
    string = ""
    for i in range(len(resualt)):
        if i==len(resualt)-1:
            string = string+str(resualt[i][1])
        else:
            string = string+str(resualt[i][1])+" "
    print(string)
else:
    print("NO")