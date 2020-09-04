from depots import Depots as dpts
from customers import Customers as csts
from splitDepots import SplitDepots
from split_algorithms import Split_algorithms as split
from solution import Solution

class InitialPopulation:

    def __init__(self):
        self._population = [] #lista de Solution ordenada em ordem crescente de custo

    '''
    Método define população inicial
    '''
    def definePopulation(self):
        #“cluster first and then route”
        clusters = SplitDepots.GilletJohnson() #divisão por depósitos
        individual = split.mountRoutes(clusters) #criação de rotas por depósitos, individual é um Solution
        self._population.append(individual)
        self._population = sorted(self._population, key = Solution.get_cost)
        #SplitDepots.randomDistribution(5000)
        print(self._population[0])



    def get_population(self):
        return self._population
