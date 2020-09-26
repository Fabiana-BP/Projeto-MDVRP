from depots import Depots as dpts
from customers import Customers as csts
from splitDepots import SplitDepots
from splitAlgorithms import SplitAlgorithms as split
from solution import Solution
from auxiliary_heuristics import NearestNeighbor
from mutation import Mutation as mt
import numpy as np

class InitialPopulation:

    def __init__(self):
        self._population = [] #lista de Solution ordenada em ordem crescente de custo

    '''
    Método define população inicial
    '''
    def definePopulation(self,size):
        #Heurística do vizinho mais próximo
        for cst in  csts.get_customersList():
            tour = NearestNeighbor.nearestNeighbor(csts.get_customersList()[cst])
            break
        cluster = SplitDepots.splitByDepot(tour)
        individual = split.splitLinearBounded(cluster) #criação de rotas por depósitos, individual é um Solution
        # rand = np.random.random()
        # if rand < 0.05:
        #     individual = mt.mutation(individual)
        self._population.append(individual)

        #“cluster first and then route”
        cluster = SplitDepots.GilletJohnson() #divisão por depósitos
        #individual = split.mountRoutes(cluster) #criação de rotas por depósitos, individual é um Solution
        individual = split.splitLinearBounded(cluster) #criação de rotas por depósitos, individual é um Solution
        # rand = np.random.random()
        # if rand < 0.05:
        #     individual = mt.mutation(individual)
        if individual is not None and self.is_different(individual):
            self._population.append(individual)

        #formação de rotas aleatórias
        for i in range(2*size):
            if len(self._population)>=size:
                break
            seed = int(5000 * np.random.random())
            sd = SplitDepots()
            sp = split()
            cluster = SplitDepots.randomDistribution(seed)
            individual = split.splitLinearBounded(cluster) #criação de rotas por depósitos, individual é um Solution
            # rand = np.random.random()
            # if rand < 0.05:
            #     individual = mt.mutation(individual)
            if individual is not None and self.is_different(individual):
                self.addIndividual(individual)

        self.sortPopulation()

        for i in self._population:
            print(i)

        print(len(self._population))
        return self._population


    '''
    Método adiciona indivíduo a população
    '''
    def addIndividual(self,solution):
        self._population.append(solution)


    '''
    Método remove o indivíduo de determinado índice da população
    @param índice do indivíduo a ser removido
    @return indivíduo removido ou -1
    '''
    def popIndividual(self,index):
        if index < len(self._population):
            return self._population.pop(index)
        else:
            return -1


    '''
    Método ordena a população em ordem crescente de custo
    '''
    def sortPopulation(self):
        self._population = sorted(self._population, key = Solution.get_cost)



    def get_population(self):
        return self._population


    '''
    Método verifica se há outro indivíduo com mesmo custo
    '''
    def is_different(self,solution):
        for p in self._population:
            if solution.get_cost() == p.get_cost():
                return False
        return True
