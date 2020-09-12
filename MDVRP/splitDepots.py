from depots import Depots as dpts
from customers import Customers as csts
from solution import Solution
from distances import Distances as dist
import numpy as np
import math
import copy

class SplitDepots:
    _availableDepots = []
    _individual = None

    '''
    Método para distribuir clientes de forma aleatória aos depósitos.
    '''
    def randomDistribution(idum):
        #print('Entrou aqui')
        np.random.seed(idum)
        SplitDepots._individual = Solution()
        customersList = copy.deepcopy(csts.get_customersList())#dicionário
        keysCst = list(customersList.keys()) #lista com as chaves dos clientes
        depots = dpts.get_depotsList() #dicionário
        nCustomers = len(keysCst)
        solution = {}

        control = {} #(depósito, [total de demanda, duração por depósito]

        for depot in depots:
            control[depot] = [0,0]
        while nCustomers > 0: #enquanto tiver cliente não alocado
            #cliente aleatório
            idCst = np.random.randint(0,len(keysCst))
            customer = customersList[keysCst[idCst]]
            #depósito mais próximo
            i=0
            dpt = customer.get_depotsDistances()[i]
            cont = len(customer.get_depotsDistances())
            aux = 0
            while ((control[str(dpt[0])][0] > depots[str(dpt[0])].get_loadTotal()+ 0.0001) or control[str(dpt[0])][1] > depots[str(dpt[0])].get_durationTotal()) and cont>0:
                if cont == 1:
                    aux = 1 #indica que todos os depósitos anteriores estão lotados
                i += 1
                dpt = customer.get_depotsDistances()[i]
                cont -= 1

            depot = depots[str(dpt[0])]
            control[str(dpt[0])][0] = control[str(dpt[0])][0] + customer.get_demand()
            control[str(dpt[0])][1] = control[str(dpt[0])][1] + customer.get_duration()

            #adicionar cliente ao depósito
            SplitDepots._individual.addGiantTour(customer,depot)
            del keysCst[idCst] #atualizar lista
            nCustomers -= 1
            #escolher três clientes aleatórios
            if len(keysCst)>0:
                idcst1 = np.random.randint(0,len(keysCst))
                neighbor1 = customersList[keysCst[idcst1]]
                dist1 = dist.euclidianDistance(customer.get_x_coord(),customer.get_y_coord(),neighbor1.get_x_coord(),neighbor1.get_y_coord())
                idcst2 = np.random.randint(0,len(keysCst))
                neighbor2 = customersList[keysCst[idcst2]]
                dist2 = dist.euclidianDistance(customer.get_x_coord(),customer.get_y_coord(),neighbor2.get_x_coord(),neighbor2.get_y_coord())
                idcst3 = np.random.randint(0,len(keysCst))
                neighbor3 = customersList[keysCst[idcst3]]
                dist3 = dist1 = dist.euclidianDistance(customer.get_x_coord(),customer.get_y_coord(),neighbor3.get_x_coord(),neighbor3.get_y_coord())
                #ver o mais próximo ao cliente
                if dist1 <= dist2 and dist1 <= dist3:
                    close = neighbor1
                    id = idcst1
                elif dist2 <= dist1 and dist2 <= dist3:
                    close = neighbor2
                    id = idcst2
                else:
                    close = neighbor3
                    id = idcst3

                control[str(dpt[0])][0] = control[str(dpt[0])][0] + close.get_demand()
                control[str(dpt[0])][1] = control[str(dpt[0])][1] + close.get_duration()

                if (control[str(dpt[0])][0] <= depot.get_loadTotal() + 0.0001 and control[str(dpt[0])][1] <= (depot.get_durationTotal())) or aux ==1:
                    #adicionar vizinho mais próximo a solução
                    SplitDepots._individual.addGiantTour(close,depot)
                    del keysCst[id] #atualizar lista
                    nCustomers -= 1
                else:
                    control[str(dpt[0])][0] = control[str(dpt[0])][0] - close.get_demand()
                    control[str(dpt[0])][1] = control[str(dpt[0])][1] - close.get_duration()



        #print(self._individual.get_giantTour())
        #print(SplitDepots._individual.get_depots())
        return SplitDepots._individual





    '''
    Implementação do algoritmo de Gillet e Johnson (1976)
    https://www.marinha.mil.br/spolm/sites/www.marinha.mil.br.spolm/files/102830.pdf
    A  ideia  básica  do  referido  algoritmo  é  selecionar  os  pontos  que  apresentam
    a maior razão entre as distâncias às duas medianas mais próximas para serem designados com  prioridade
    '''
    def GilletJohnson():
        SplitDepots._individual = Solution()
        SplitDepots._availableDepots = []
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
