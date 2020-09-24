import numpy as np
import random


class team:
    def setValue(self, num, value, name):
        self.value = value
        self.num = num
        self.name = name

    def getValue(self):
        return self.value

    def getNum(self):
        return self.num



n = int(input())
sh = np.zeros(n, dtype=team)
not_sh = np.zeros(n, dtype=team)
for i in range(n):
    tmp = input().split()
    sh[i] = team()
    sh[i].setValue(int(tmp[0]), int(tmp[1]), "sharif")
for i in range(n):
    tmp = input().split()
    not_sh[i] = team()
    not_sh[i].setValue(int(tmp[0]), int(tmp[1]), "not sharif")

np.random.shuffle(sh)
np.random.shuffle(not_sh)
domain = []

# first arc consistency
for i in range(n):
    domain.append([])
    for j in range(n):
        if abs(sh[i].getValue() - not_sh[j].getValue()) < 3:
            domain[i].append(j)
    random.shuffle(domain[i])

assignment = []


def selectUnassignedVariable(assignment):
    return len(assignment)


def AC3(domain, f, j):
    for i in range(f + 1, len(domain)):
        f = 0
        for k in range(len(domain[i])):
            if domain[i][k] != j:
                f = f + 1
        if f == 0:
            return False
    return True


def consistent(assignment, j):
    for i in range(len(assignment)):
        if assignment[i][1].getNum() == not_sh[j].getNum():
            return False
    return True


def backtracking(assignment):
    if len(assignment) == n:
        return assignment
    j = selectUnassignedVariable(assignment)
    for i in domain[j]:
        if consistent(assignment, i):
            assignment.append((sh[j], not_sh[i]))
            inferences = AC3(domain, j, i)
            if inferences != False:
                resualt = backtracking(assignment)
                if resualt != False:
                    return resualt
            assignment.remove((sh[j], not_sh[i]))
    return False


resualt = backtracking([])
if resualt == False:
    print("NO")
else:
    while (True):
        a = input()
        if (a == "end"):
            break
        else:
            a = int(a)
            for i in range(n):
                if resualt[i][0].getNum() == a:
                    print(resualt[i][1].getNum())