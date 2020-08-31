from depots import Depots as dpts
from customers import Customers as csts
from solution import Solution
import copy

class InitialPopulation:

    def __init__(self):
        self._population = []
        self._individual = Solution()
        self._availableDepots = []


    '''
    Implementação do algoritmo de Gillet e Johnson (1976)
    https://www.marinha.mil.br/spolm/sites/www.marinha.mil.br.spolm/files/102830.pdf
    A  ideia  básica  do  referido  algoritmo  é  selecionar  os  pontos  que  apresentam
    a maior razão entre as distâncias às duas medianas mais próximas para serem designados com  prioridade
    '''
    def GilletJohnson(self):
        customersList = copy.deepcopy(csts.get_customersList()) #dicionário

        for dpt in dpts.get_depotsList():
            self._availableDepots.append([dpt,dpts.get_depotsList()[dpt].get_loadTotal(),0.0]) #depósito, carga total e demanda total atendida

        unallocatedCustomers = self.GilletJohnsonProcedure(customersList,len(self._availableDepots))
        self._population.append(self._individual)
        print("vai imprimir individual")
        print(self._individual)
        self._individual = Solution()


    def GilletJohnsonProcedure(self,customersList,nDepotsAvailable):
        unallocatedCustomers = customersList
        numberDepotsAvailable = nDepotsAvailable
        auxiliar = []

        for cst in unallocatedCustomers:
            depotsDistances = unallocatedCustomers[cst].get_depotsDistances()
            depotsAvailable = []
            # recuperar apenas depósitos com vagas
            i=0
            for adpts in self._availableDepots:
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
        for dpt in self._availableDepots:
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
                            self._individual.addGiantTour(str(pt[0].get_id()),dpt[0])
                            #remove da lista de unallocatedCustomers
                            unallocatedCustomers.pop(str(pt[0].get_id()),-1)
                    else:
                        #adiciona o cliente no depósito mais próximo
                        self._individual.addGiantTour(str(pt[0].get_id()),dpt[0])
                        #remove da lista de unallocatedCustomers
                        unallocatedCustomers.pop(str(pt[0].get_id()),-1)


        print(":")
        print(self._availableDepots)
        print(unallocatedCustomers)
        if len(unallocatedCustomers)>0:
            return self.GilletJohnsonProcedure(unallocatedCustomers,numberDepotsAvailable)
        else:
            return unallocatedCustomers

    def get_population(self):
        return self._population
