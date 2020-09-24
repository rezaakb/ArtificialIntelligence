import random

class node:
    def setValue(self, name, father, cpt):
        self.father = father
        self.cpt = cpt
        self.name = name

    def getFather(self):
        return self.father

    def getName(self):
        return self.name

    def getCpt(self):
        return self.cpt

n = int(input())

variables = [None]*n
a = input().split(" ")

for i in range(n):
    variables[i] = a[i]

m = int(input())
list_nodes =[]
a = input().split(" ")
i=0
while i<m:
    c = 2**(len(a)-2)
    name = a[len(a)-2]
    fathers = []
    cpt = [0]*c
    for j in range(len(a)-2):
        fathers.append(a[j][1:len(a[j])])
    i=i+c
    for j in range(c):
        cpt[j]=float(a[len(a)-1])
        a = input().split(" ")
    tmp = node()
    tmp.setValue(name, fathers, cpt)
    list_nodes.append(tmp)

query_name = a[0]
query_evidence =[]
query_evidence_value =[]
for i in range(1,len(a)):
    if a[i][0] =='+':
        query_evidence_value.append(1)
    else:
        query_evidence_value.append(0)
    query_evidence.append(a[i][1:len(a[i])])


def findNode(nodes,query):
    for i in range(len(nodes)):
        if nodes[i].name == query:
            return nodes[i]
    pass

def findNodeChildren(nodes,query):
    list_children = []
    for i in range(len(nodes)):
        if query in nodes[i].father:
            list_children.append(nodes[i])

    return list_children

def findNodeIndex(nodes,query):
    for i in range(len(nodes)):
        if nodes[i].name == query:
            return i
    pass


from operator import itemgetter

def findOrdering(nodes, query, evidence):
    query_evidence_all = [query] + evidence
    ordering_variable = []
    for i in range(len(query_evidence_all)):
        d = findNodeIndex(nodes,query_evidence_all[i])
        ordering_variable.append([])
        visited = [False] * (len(nodes))
        queue = []
        queue.append(d)
        visited[d] = True

        while queue:
            tmp =queue.pop(0)
            d = nodes[tmp]
            ordering_variable[i].append((len(d.father),d.name))
            for k in d.father:
                j = findNodeIndex(nodes,k)
                if visited[j] == False:
                    queue.append(j)
                    visited[j] = True
        ordering_variable[i] = sorted(ordering_variable[i], key=itemgetter(0))
        for j in range(len(ordering_variable[i])):
            ordering_variable[i][j]=ordering_variable[i][j][1]
    return ordering_variable


def randomChoice(nodes,name,dict):
    d=findNode(nodes,name)
    fathers = d.father
    index = 0
    num_fathers =len(fathers)
    for i in range(num_fathers-1,-1,-1):
        index = (1-dict[fathers[i]])*(2**(num_fathers-i-1))+index
    p = d.cpt[index]
    r = random.random()
    if r < p:
        return 1
    else:
        return 0



def randomChoiceGibbs(nodes,name,dict):
    cpts = []
    p1 = randomChoiceLiklihood(nodes,name,dict)
    cpts.append([p1,1-p1])
    list_children = findNodeChildren(nodes,name)
    tmp = dict[name]
    for i in range(len(list_children)):
        dict[name]=1
        p1 = randomChoiceLiklihoodWithNode(list_children[i],dict)

        dict[name] = 0
        p2 = randomChoiceLiklihoodWithNode(list_children[i], dict)
        cpts.append([p1,p2])
    dict[name] = tmp
    p1 = 1
    p2 = 1
    for i in range(len(cpts)):
        p1 = p1 * cpts[i][0]
        p2 = p2 * cpts[i][1]

    p = p1/(p1+p2)
    r = random.random()
    if r < p:
        return 1
    else:
        return 0


def randomChoiceLiklihood(nodes,name,dict):
    d=findNode(nodes,name)
    fathers = d.father
    index = 0
    num_fathers =len(fathers)
    for i in range(num_fathers):
        index = (1-dict[fathers[i]])*(2**(num_fathers-i-1))+index
    return d.cpt[index]


def randomChoiceLiklihoodWithNode(d,dict):
    fathers = d.father
    index = 0
    num_fathers =len(fathers)
    for i in range(num_fathers):
        index = (1-dict[fathers[i]])*(2**(num_fathers-i-1))+index
    return d.cpt[index]



def rejectionSampling(nodes, query, evidence,evidence_value):
    query_evidence_all = [query] + evidence
    dicti = {}
    order = findOrdering(nodes, query, evidence)
    counter_p = 0
    counter_n = 0
    for i in range(len(order)):
        for j in range(len(order[i])):
            dicti[order[i][j]] = 2
    for k in range(10000):

        # initial value
        dicti = dict.fromkeys(dicti, 2)
        for i in range(len(query_evidence_all)-1,-1,-1):
            for j in range(len(order[i])):
                if dicti[order[i][j]]==2:
                    dicti[order[i][j]]= randomChoice(nodes,order[i][j],dicti)
            if i!=0:
                if dicti[evidence[i-1]]!=evidence_value[i-1]:
                    break
            else:
                if dicti[query_evidence_all[0]]==0:
                    counter_n = counter_n+1
                elif dicti[query_evidence_all[0]]==1:
                    counter_p = counter_p+1
    return counter_p/(counter_p+counter_n)


def likelihoodSampling(nodes, query, evidence,evidence_value):
    query_evidence_all = [query] + evidence
    dicti = {}
    order = findOrdering(nodes, query, evidence)
    order_all = []
    counter_p = 0
    counter_n = 0
    for i in range(len(order)):
        order_all = order_all + order[i]
    variables = list(set(order_all))
    keys = [2]*len(variables)
    for i in range(len(evidence)):
        if evidence[i] in variables:
            keys[variables.index(evidence[i])] = evidence_value[i]

    for k in range(100000):

        # initial value
        for i in range(len(variables)):
            dicti[variables[i]]= keys[i]

        f = 0
        w = 1
        for i in range(len(query_evidence_all)-1,-1,-1):
            for j in range(len(order[i])):
                if dicti[order[i][j]]==2:
                    dicti[order[i][j]] = randomChoice(nodes,order[i][j],dicti)
                elif order[i][j] in evidence and j == len(order[i])-1:
                    w = w * randomChoiceLiklihood(nodes,order[i][j],dicti)

        if dicti[query_evidence_all[0]]==0:
            counter_n = counter_n+w
        elif dicti[query_evidence_all[0]]==1:
            counter_p = counter_p+w

    return counter_p/(counter_p+counter_n)






def gibbsSampling(nodes, query, evidence,evidence_value):
    dicti = {}
    order = findOrdering(nodes, query, evidence)
    order_all=[]
    for i in range(len(order)):
        order_all = order_all + order[i]
    variables = list(set(order_all))
    for i in range(len(evidence)):
        variables.remove(evidence[i])
    counter_p = 0
    counter_n = 0
    for i in range(len(variables)):
        dicti[variables[i]] = random.randint(0, 1)
    for i in range(len(evidence)):
        dicti[evidence[i]] = evidence_value[i]

    for k in range(100000):

        for j in range(len(variables)):
            dicti[variables[j]]= randomChoiceGibbs(nodes,variables[j],dicti)

        if dicti[query]==0:
            counter_n = counter_n+1
        elif dicti[query]==1:
            counter_p = counter_p+1

    return counter_p/(counter_p+counter_n)

print('Rejection ',rejectionSampling(list_nodes,query_name,query_evidence,query_evidence_value))
print('Likelihood ',likelihoodSampling(list_nodes,query_name,query_evidence,query_evidence_value))
print('Gibbs ',gibbsSampling(list_nodes,query_name,query_evidence,query_evidence_value))