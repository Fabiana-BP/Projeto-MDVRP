from customers import Customers as csts
import numpy as np
import copy

class Crossover:
    '''
    @param lista de clientes (individual1)
    @param lista de clientes (individual2)
    '''
    def OBX(individual1,individual2):
        P1 = individual1.get_giantTour()
        P2 = individual2.get_giantTour()
        # print(P1)
        # print(P2)
        P = [P1,P2]
        child = [[],[]]
        for i in range(2):
            pos1 = Crossover.choosePositions(len(P1)) #lista de posições
            # print("pos1")
            # print(pos1)
            child[i] = copy.deepcopy(P[i])
            pos2 = []
            j = 0
            while j < len(pos1):
                pos2.append(P[i].index(P[(i+1) % 2][pos1[j]]))
                j += 1
            pos2 = sorted(pos2)
            # print("pos2")
            # print(pos2)
            # exit(1)
            j = 0
            while j < len(pos2):
                child[i][pos2[j]] = P[(i+1) % 2][pos1[j]]
                j += 1

        rand = np.random.random()
        # print(child)
        if rand > 0.5:
            return child[0]
        else:
            return child[1]



    '''
    Método escolhe uma lista de posições do indivíduo de forma aleatória
    '''
    def choosePositions(sizeIndividual):
        numPositions = np.random.randint(1,sizeIndividual-1)
        # print("numPositions")
        # print(numPositions)
        positions = []
        i = 0
        while i < numPositions:
            pos = np.random.randint(sizeIndividual)
            if len(positions)<1 or pos not in positions:
                positions.append(pos)
                i += 1

        return positions



    '''
    https://files.cercomp.ufg.br/weby/up/498/o/SamuelWanbergLourencoNery2016.pdf
    @param lista de clientes (individual1)
    @param lista de clientes (individual2)
    '''
    def PMX(individual1,individual2):
        P1 = individual1.get_giantTour()
        P2 = individual2.get_giantTour()
        P = [P1, P2] #pais
        # print(P)
        pos0 = np.random.randint(0,len(P1)-1) #posição inicial a ser copiada de P1
        posF = np.random.randint(pos0+1,len(P1)) #posição final a ser copiada de P1
        # print("pos0: "+str(pos0)+" posF: "+str(posF))
        child1 = []
        child2 = []
        for i in range(len(P1)):
            child1.append(-1) #é um giant_tour sem depósitos associados
            child2.append(-1)

        #copiar a parte selecionada de P1 para child2 e de P2 para child1

        list1 = copy.deepcopy(P2)
        list2 = copy.deepcopy(P1)
        for i in range(pos0,posF+1):
            child1[i] = P2[i]
            list1.remove(child1[i])
            child2[i] = P1[i]
            list2.remove(child2[i])
        #print("list1")
        #print(list1)
        child =[child1,child2]
        listControl = [list1,list2]
        for v in range(2):
            for c in listControl[v]:
                aux = c
                while pos0 <= P[v].index(c) and P[v].index(c) <= posF:
                    c = child[v][P[v].index(c)]
                child[v][P[v].index(c)] = aux
        # print("child")
        # print(str(child))
        rand = np.random.random()
        if rand > 0.5:
            return child[0]
        else:
            return child[1]
