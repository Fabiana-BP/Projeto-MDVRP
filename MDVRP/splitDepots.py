from depots import Depots as dpts
from customers import Customers as csts
from solution import Solution
import numpy as np
import math
import copy

class SplitDepots:
    _availableDepots = []
    _individual = None

    '''
    Método para distribuir clientes de forma aleatória aos depósitos.

    def randomDistribution(idum):
        print('Entrou aqui')
        np.random.seed(idum)
        SplitDepots._individual = Solution()
        customersList = copy.deepcopy(csts.get_customersList())#dicionário
        l = list(customersList.keys()) #lista com as chaves dos clientes
        depots = dpts.get_depotsList() #dicionário
        nCustomers = len(l)

        control = {} #(depósito, [total de demanda, duração por depósito]

        for depot in depots:
            control[depot] = [0,0]

        solution = Solution()

        while nCustomers > 0: #enquanto tiver cliente não alocado

        '''




    '''
    Implementação do algoritmo de Gillet e Johnson (1976)
    https://www.marinha.mil.br/spolm/sites/www.marinha.mil.br.spolm/files/102830.pdf
    A  ideia  básica  do  referido  algoritmo  é  selecionar  os  pontos  que  apresentam
    a maior razão entre as distâncias às duas medianas mais próximas para serem designados com  prioridade
    '''
    def GilletJohnson():
        SplitDepots._individual = Solution()
        customersList = copy.deepcopy(csts.get_customersList()) #dicionário

        for dpt in dpts.get_depotsList():
            SplitDepots._availableDepots.append([dpt,dpts.get_depotsList()[dpt].get_loadTotal(),0.0]) #depósito, carga total e demanda total atendida

        unallocatedCustomers = SplitDepots.GilletJohnsonProcedure(customersList,len(SplitDepots._availableDepots))

        #print(Split_algorithms._individual)
        return SplitDepots._individual


    def GilletJohnsonProcedure(customersList,nDepotsAvailable):
        unallocatedCustomers = customersList
        numberDepotsAvailable = nDepotsAvailable
        depots = dpts.get_depotsList()
        auxiliar = []

        for cst in unallocatedCustomers:
            depotsDistances = unallocatedCustomers[cst].get_depotsDistances()
            depotsAvailable = []
            # recuperar apenas depósitos com vagas
            i=0
            for adpts in SplitDepots._availableDepots:
                if str(depotsDistances[i][0]) == str(adpts[0]):
                    depotsAvailable.append(depotsDistances[i])

            if len(depotsAvailable) > 1:
                fstDepot = depotsAvailable[0] #primeiro depósito mais próximo
                sndDepot = depotsAvailable[1] #segundo depósito mais próximo
                fstDistance = fstDepot[1] #distância do primeiro depósito
                sndDistance = sndDepot[1] #distância do segundo depósito
                ratio = fstDistance/float(sndDistance)
                auxiliar.append([unallocatedCustomers[cst],ratio,str(fstDepot[0])])
            elif len(depotsAvailable) == 1:
                fstDepot = depotsAvailable[0] #primeiro depósito mais próximo
                ratio = 1.0
                auxiliar.append([unallocatedCustomers[cst],ratio,str(fstDepot[0])])

            i += 1

        # ordenar lista auxiliar em ordem descrescente
        pts = sorted(auxiliar, key = lambda x: x[1],reverse=True)
        for dpt in SplitDepots._availableDepots:
            for pt in pts:
                if dpt[0] == pt[2]:
                    dpt[2] += pt[0].get_demand()
                    if dpt[1] < dpt[2]: #se carga total < demanda total (considera cheio)
                        if numberDepotsAvailable > 1: #se ainda faltarem clientes para serem alocados e restar apenas 1 depósito, a carga total será desrespeitada
                            dpt[2] -= pt[0].get_demand()
                            print("é menor")
                            dpt[0] = "-1"
                            numberDepotsAvailable -= 1

                        else:
                            #adiciona o cliente no depósito mais próximo
                            SplitDepots._individual.addGiantTour(pt[0],depots[dpt[0]])
                            #remove da lista de unallocatedCustomers
                            unallocatedCustomers.pop(str(pt[0].get_id()),-1)
                    else:
                        #adiciona o cliente no depósito mais próximo
                        SplitDepots._individual.addGiantTour(pt[0],depots[dpt[0]])
                        #remove da lista de unallocatedCustomers
                        unallocatedCustomers.pop(str(pt[0].get_id()),-1)


        #print(":")
        #print(Split_algorithms._availableDepots)
        #print(unallocatedCustomers)
        if len(unallocatedCustomers)>0:
            return SplitDepots.GilletJohnsonProcedure(unallocatedCustomers,numberDepotsAvailable)
        else:
            return unallocatedCustomers
