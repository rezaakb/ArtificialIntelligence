import numpy as np
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


class query:
    def setValue(self, name, evidence, value_evidence):
        self.evidence = evidence
        self.value_evidence = value_evidence
        self.name = name

    def getValueEvidence(self):
        return self.value_evidence

    def getName(self):
        return self.name

    def getEvidence(self):
        return self.evidence


a = input()
list_nodes =[]
while (a!="."):
    b = a.split(', [')
    n = node()
    name = [b[0][1:len(b[0])]]
    list_of_fathers = []
    cpt=[]
    if (b[1]!=']'):
        list_of_fathers = (b[1][0:-1]).split(', ')
    cpt = list(map(float, b[2][0:-2].split(', ')))
    n.setValue(name, list_of_fathers, cpt)
    list_nodes.append(n)
    a = input()

a=input()
list_query = []
while (a!="."):
    b = a.split(', [')
    n = query()
    variables = b[0][2:-1].split(', ')
    list_of_evidence = []
    value_evidence = []
    if (b[1]!=']'):
        list_of_evidence = b[1][0:-1].split(', ')
        value_evidence  = list(map(float, b[2][0:-2].split(', ')))
    n.setValue(variables, list_of_evidence, value_evidence)
    list_query.append(n)
    a = input()

passed = []

def findRelatedFactors(v,list):
    related = []
    for i in range (len(list)):
        tmp = list[i].getFather()
        if v in tmp:
            related.append(list[i])
    return related


def sumOut(final_cpt, v,names,fathers):
    variables_num = len(names) + len(fathers)
    string_binary = '{0:0' + str(variables_num) + 'b}'

    sum_out_cpt = [None] * (len(final_cpt)//2)

    new_names = names[:]
    new_fathers = fathers[:]
    main_name = v.getName()
    for i in range(len(main_name)):
        new_names.remove(main_name[i])
    for k in range(len(main_name)):
        t=0
        for i in range(len(final_cpt)):
            binary =string_binary.format(i)
            dict={}
            for j in range(len(names)):
                dict[names[j]]=binary[j]
            for j in range(len(fathers)):
                dict[fathers[j]]=binary[j+len(names)]

            if dict[main_name[k]]=='1':
                continue

            index = 0

            if (len(new_names) > 1):
                for w in range(1, len(new_names)):
                    tmp1 = int(dict[new_names[w]])
                    tmp2 = 2 ** (len(new_names) + len(new_fathers) - w - 1)
                    tmp = tmp1 * (tmp2)
                    index = index + tmp

            for w in range(len(new_fathers)):
                tmp1 = int(dict[new_fathers[w]])
                tmp2 = 2 ** (len(new_fathers) - w - 1)
                tmp = tmp1 * (tmp2)
                index = index + tmp

            index2=0
            dict[main_name[k]] = 1
            if (len(names) > 1):
                for w in range(1, len(names)):
                    tmp1 = int(dict[names[w]])
                    tmp2 = 2 ** (len(names) + len(fathers) - w- 1)
                    tmp = tmp1 * (tmp2)
                    index2 = index2 + tmp

            for w in range(len(fathers)):
                tmp1 = int(dict[fathers[w]])
                tmp2 = 2 ** (len(fathers) - w - 1)
                tmp = tmp1 * (tmp2)
                index2 = index2 + tmp

            tmp1 = final_cpt[i]
            if dict[names[0]] == '1':
                tmp1 = 1 - tmp1

            tmp2 = final_cpt[index2]
            if dict[names[0]] == '1':
                tmp2 = 1 - tmp2
            t=t+1
            sum_out_cpt[index]=tmp1+tmp2
            if t==len(final_cpt)//2:
                break
    return new_names,sum_out_cpt


def joinRelatedFactors(v,factors):

    new_node = node()

    #tedad name haye khoroji
    new_node_names = []

    #tedad father haye khoroji
    new_node_father = []

    main_name = v.getName()
    main_cpt = v.getCpt()
    main_father = v.getFather()

    for i in range(len(factors)):
        tmp = factors[i].getName()
        for j in range(len(tmp)):
            if tmp[j] not in new_node_names:
                new_node_names.append(tmp[j])
        tmp = factors[i].getFather()
        for j in range(len(tmp)):
            if tmp[j] not in new_node_father:
                new_node_father.append(tmp[j])

    for j in range(len(main_name)):
        if main_name[j] not in new_node_names:
            new_node_names.append(main_name[j])
        if main_name[j] in new_node_father:
            new_node_father.remove(main_name[j])
    for j in range(len(main_father)):
        if main_father[j] not in new_node_father:
            new_node_father.append(main_father[j])
    variables_num = len(new_node_names)+len(new_node_father)
    cpt_num = 2**(variables_num-1)

    #cpt khoroji
    final_cpt =[None] * cpt_num
    string_binary = '{0:0'+str(variables_num)+'b}'

    for i in range(cpt_num):
        binary =string_binary.format(i)
        dict={}
        for j in range(len(new_node_names)):
            dict[new_node_names[j]]=binary[j]
        for j in range(len(new_node_father)):
            dict[new_node_father[j]]=binary[j+len(new_node_names)]
        resualt = 1

        for j in range(len(factors)):
            father_of_factor = factors[j].getFather()
            name_factor = factors[j].getName()
            index = 0

            if (len(name_factor)>1):
                for k in range(1,len(name_factor)):
                    tmp1 = int(dict[name_factor[k]])
                    tmp2 = 2 ** (len(name_factor) +len(father_of_factor) - k - 1)
                    tmp = tmp1 * (tmp2)
                    index = index + tmp

            for k in range(len(father_of_factor)):
                tmp1 = int(dict[father_of_factor[k]])
                tmp2 = 2 ** (len(father_of_factor) - k - 1)
                tmp = tmp1 * (tmp2)
                index = index + tmp

            n1 = factors[j].getCpt()[index]
            if dict[name_factor[0]]=='1':
               n1 = 1-n1
            resualt = resualt * n1
        index=0
        if (len(main_name) > 1):
            for k in range(1, len(main_name)):
                tmp1 = int(dict[main_name[k]])
                tmp2 = 2 ** (len(main_name) + len(main_father) - k - 1)
                tmp = tmp1 * (tmp2)
                index = index + tmp

        for k in range(len(main_father)):
            tmp1 = int(dict[main_father[k]])
            tmp2 = 2 ** (len(main_father) - k - 1)
            tmp = tmp1 * (tmp2)
            index = index + tmp

        n1 = main_cpt[index]
        if dict[main_name[0]]=='1':
           n1 = 1-n1
        resualt = resualt * n1

        final_cpt[i]=resualt
    new_node_names, new_node_cpt = sumOut(final_cpt, v, new_node_names, new_node_father)
    new_node.setValue(new_node_names, new_node_father, new_node_cpt)
    return new_node


def joinRelatedFactorsWithoutSumOut(v,factors):

    new_node = node()

    #tedad name haye khoroji
    new_node_names = []

    #tedad father haye khoroji
    new_node_father = []

    main_name = v.getName()
    main_cpt = v.getCpt()
    main_father = v.getFather()

    for i in range(len(factors)):
        tmp = factors[i].getName()
        for j in range(len(tmp)):
            if tmp[j] not in new_node_names:
                new_node_names.append(tmp[j])
        tmp = factors[i].getFather()
        for j in range(len(tmp)):
            if tmp[j] not in new_node_father:
                new_node_father.append(tmp[j])

    for j in range(len(main_name)):
        if main_name[j] not in new_node_names:
            new_node_names.append(main_name[j])
        if main_name[j] in new_node_father:
            new_node_father.remove(main_name[j])
    for j in range(len(main_father)):
        if main_father[j] not in new_node_father:
            new_node_father.append(main_father[j])
    variables_num = len(new_node_names)+len(new_node_father)
    cpt_num = 2**(variables_num-1)

    #cpt khoroji
    final_cpt =[None] * cpt_num
    string_binary = '{0:0'+str(variables_num)+'b}'

    for i in range(cpt_num):
        binary =string_binary.format(i)
        dict={}
        for j in range(len(new_node_names)):
            dict[new_node_names[j]]=binary[j]
        for j in range(len(new_node_father)):
            dict[new_node_father[j]]=binary[j+len(new_node_names)]
        resualt = 1

        for j in range(len(factors)):
            father_of_factor = factors[j].getFather()
            name_factor = factors[j].getName()
            index = 0

            if (len(name_factor)>1):
                for k in range(1,len(name_factor)):
                    tmp1 = int(dict[name_factor[k]])
                    tmp2 = 2 ** (len(name_factor) +len(father_of_factor) - k - 1)
                    tmp = tmp1 * (tmp2)
                    index = index + tmp

            for k in range(len(father_of_factor)):
                tmp1 = int(dict[father_of_factor[k]])
                tmp2 = 2 ** (len(father_of_factor) - k - 1)
                tmp = tmp1 * (tmp2)
                index = index + tmp

            n1 = factors[j].getCpt()[index]
            if dict[name_factor[0]]=='1':
               n1 = 1-n1
            resualt = resualt * n1
        index=0
        if (len(main_name) > 1):
            for k in range(1, len(main_name)):
                tmp1 = int(dict[main_name[k]])
                tmp2 = 2 ** (len(main_name) + len(main_father) - k - 1)
                tmp = tmp1 * (tmp2)
                index = index + tmp

        for k in range(len(main_father)):
            tmp1 = int(dict[main_father[k]])
            tmp2 = 2 ** (len(main_father) - k - 1)
            tmp = tmp1 * (tmp2)
            index = index + tmp

        n1 = main_cpt[index]
        if dict[main_name[0]]=='1':
           n1 = 1-n1
        resualt = resualt * n1

        final_cpt[i]=resualt
    new_node.setValue(new_node_names, new_node_father, final_cpt)
    return new_node

def printNode(n):
    for i in n:
        print('P(',i.getName(),'|',i.getFather(),')')




list_nodes_first = list_nodes[:]
final_joins =[]


def findFactor(v, list_nodes):
    for i in range(len(list_nodes)):
        tmp = list_nodes[i].getName()
        if v in tmp:
            return list_nodes[i]
    return None


for j in range(len(list_query)):

    query_name = list_query[j].getName()
    query_evidence = list_query[j].getEvidence()
    query_evidence_value = list_query[j].getValueEvidence()

    unselected_variables = query_name + query_evidence
    selected_variables = []
    for j in list_nodes:
        if j.getName()[0] not in selected_variables and j.getName()[0] not in unselected_variables:
            selected_variables.append(j.getName()[0])
    ii=0
    jj=0

    while 0<len(selected_variables):
        related = findRelatedFactors(selected_variables[ii],list_nodes)
        if ii<len(selected_variables)-1:
            ii=ii+1
            continue
        variable = findFactor(selected_variables[ii],list_nodes)
        if (len(related)>0):
            new_node = joinRelatedFactors(variable,related)
            list_nodes.remove(variable)
            selected_variables.remove(selected_variables[ii])
            for w in range(len(related)):
                list_nodes.remove(related[w])

            list_nodes.append(new_node)
            ii=0
        else:
            if variable in list_nodes:
                list_nodes.remove(variable)
            selected_variables.remove(selected_variables[ii])
            ii=ii-1
    if (len(list_nodes)>1):
        querys = []
        unquerys = []
        for w in range(len(query_name)):
            for p in range(len(list_nodes)):
                if query_name[w] == list_nodes[p].getName()[0]:
                    querys.append(list_nodes[p])
                    break

        for p in range(len(list_nodes)):
            if list_nodes[p] not in querys:
                unquerys.append(list_nodes[p])

        for p in range(len(querys)):
            new_node = joinRelatedFactorsWithoutSumOut(querys[len(querys)-1-p],unquerys)
            unquerys = [new_node]
    else:
        new_node = list_nodes[0]

    resualt_name = new_node.getName()
    resualt_father = new_node.getFather()
    resualt_csp = new_node.getCpt()

    #find probability
    dict = {}
    for j in range(len(query_evidence)):
        dict[query_evidence[j]] = (int(query_evidence_value[j])+1)%2

    final_num = len(query_name)
    final_table_num = 2**(final_num)
    final_table = [None] * final_table_num

    string_binary = '{0:0'+str(final_num)+'b}'
    for j in range(final_table_num):
        binary =string_binary.format(j)
        for w in range(len(query_name)):
            dict[query_name[w]] = binary[w]
        index=0
        if (len(resualt_name) > 1):
            for w in range(1, len(resualt_name)):
                tmp1 = int(dict[resualt_name[w]])
                tmp2 = 2 ** (len(resualt_name) + len(resualt_father) - w - 1)
                tmp = tmp1 * (tmp2)
                index = index + tmp

        for w in range(len(resualt_father)):
            tmp1 = int(dict[resualt_father[w]])
            tmp2 = 2 ** (len(resualt_father) - w - 1)
            tmp = tmp1 * (tmp2)
            index = index + tmp

        tmp_resualt = resualt_csp[index]
        if dict[resualt_name[0]] == '1':
            tmp_resualt = 1 - tmp_resualt

        final_table[j]=tmp_resualt

    list_nodes = list_nodes_first[:]
    for w in range(0,len(final_table),2):
        tmp = final_table[w]+final_table[w+1]
        print("%.2f" % (final_table[w] / tmp))
        print("%.2f" % (final_table[w + 1] / tmp))

