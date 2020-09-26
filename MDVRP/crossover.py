from customers import Customers as csts
import numpy as np

class Crossover:
    '''
    @param lista de clientes (individual1)
    @param lista de clientes (individual2)
    '''
    def OBX(individual1,individual2):
        P1 = individual1.get_giantTour()
        P2 = individual2.get_giantTour()
        pos0 = np.random.randint(0,len(P1)-1) #posição inicial a ser copiada de P1
        posF = np.random.randint(pos0+1,len(P1)) #posição final a ser copiada de P1
        #print("pos0: "+str(pos0)+" posF: "+str(posF))

        child =[-1 for x in range(len(P1))] #é um giant_tour sem depósitos associados

        #copiar a parte selecionada de P1 para child
        aux = [] #controle para saber quais foram copiados
        for i in range(pos0,posF+1):
            child[i] = P1[i]
            aux.append(P1[i].get_id())

        i = 0

        #completar com os clientes de P2 que não estão em child respeitando a ordem
        for cst in P2:
            if cst.get_id() not in aux:
                while child[i] is not -1:
                    i += 1
                child[i] = cst

        return child

    '''
    @param lista de clientes (individual1)
    @param lista de clientes (individual2)
    '''
    def PMX(individual1,individual2):
        P1 = individual1.get_giantTour()
        P2 = individual2.get_giantTour()
        pos0 = np.random.randint(0,len(P1)-1) #posição inicial a ser copiada de P1
        posF = np.random.randint(pos0+1,len(P1)) #posição final a ser copiada de P1
        #print("pos0: "+str(pos0)+" posF: "+str(posF))

        child =[-1 for x in range(len(P1))] #é um giant_tour sem depósitos associados
        #copiar a parte selecionada de P1 para child
        aux = [] #controle para saber quais foram copiados
        auxImage = [] #corresponde a quais foram substituídos
        for i in range(pos0,posF+1):
            child[i] = P1[i]
            aux.append(P1[i].get_id())
            auxImage.append(P2[i].get_id())

        #completar com os clientes de P2 que não estão em child, caso esteja troca pela imagem de P1
        for i in range(len(P2)):
            if child[i] == -1:
                if P2[i].get_id() in aux:
                    #recupera índice de aux
                    id = aux.index(P2[i].get_id())
                    child[i] = csts.get_customersList()[str(auxImage[id])]
                else:
                    child[i] = P2[i]


        return child
