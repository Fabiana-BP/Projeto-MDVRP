from initialPopulation import InitialPopulation
from crossover import Crossover as cross
from splitDepots import SplitDepots
from splitAlgorithms import SplitAlgorithms as split
from mutation import Mutation
import numpy as np

class GeneticAlgorithm:

    '''
    Método responsável pelo algoritmo genético
    '''
    def GA(self):
        #define população inicial
        pop = InitialPopulation()
        population = pop.definePopulation(100)
        #avalie a população

        #critério de parada

            #selecione os pais
        aux1 = population[np.random.randint(0,len(population))]
        aux2 = population[np.random.randint(0,len(population))]
        menor = lambda x,y:x if x.get_cost()<y.get_cost() else y
        P1 = menor(aux1,aux2)
        aux1 = population[np.random.randint(0,len(population))]
        aux2 = population[np.random.randint(0,len(population))]
        P2 = menor(aux1,aux2)
            #Crossover
        rand = np.random.random()
        child = []
        if rand>0.5:
            child = cross.OBX(P1,P2)
        else:
            child = cross.PMX(P1,P2)
        cluster = SplitDepots.splitByDepot(child)
        individual = split.splitLinearBounded(cluster)
        print(P1)
        print(P2)
        print(individual)

            #Mutação
        individual = Mutation.M1(individual)
        print(individual)
            #avalie a população

            #defina a população sobrevivente

        #liste os melhores indivíduos
