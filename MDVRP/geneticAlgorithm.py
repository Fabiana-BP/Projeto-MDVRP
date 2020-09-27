from initialPopulation import InitialPopulation
from crossover import Crossover as cross
from splitDepots import SplitDepots
from splitAlgorithms import SplitAlgorithms as split
from mutation import Mutation
import numpy as np
import config

class GeneticAlgorithm:

    '''
    Método responsável pelo algoritmo genético
    '''
    def GA(self):
        #define população inicial
        pop = InitialPopulation()
        population = pop.definePopulation(config.SIZE_POPULATION)
        #avalie a população

        #critério de parada
        for i in range(200):
            #selecione os pais

            aux1 = population[np.random.randint(0,len(population))]
            aux2 = population[np.random.randint(0,len(population))]
            minor = lambda x,y:x if x.get_cost()<y.get_cost() else y
            P1 = minor(aux1,aux2)
            aux1 = population[np.random.randint(0,len(population))]
            aux2 = population[np.random.randint(0,len(population))]
            P2 = minor(aux1,aux2)

            #Crossover

            rand = np.random.random()
            # print(rand)
            # print(P1)
            # print(P2)
            child = []
            if rand>0.5:
                child = cross.OBX(P1,P2)
            else:
                child = cross.PMX(P1,P2)
            # print("child: \n")
            # print(child)
            cluster = SplitDepots.splitByDepot(child)
            individual = split.splitLinearBounded(cluster)

            # print("individual: ")
            # print(individual)

            #Mutação

            individual = Mutation.mutation(individual)
            # print("individual: ")
            # print("indivíduo: "+str(individual))
            #print(individual.get_routes())
            # pop.addIndividual(individual)
            # pop.sortPopulation()

            #avalie a população
            ok = pop.is_different(individual)
            if ok: #indivíduo diferente do resto da população
                if len(population)<config.SIZE_POPULATION:
                    pop.addIndividual(individual)
                else:
                    if pop.popIndividual(len(population)-1) != -1:
                        pop.addIndividual(individual)
                    else:
                        print("Indivíduo não foi removido da população")
                        exit(1)
            pop.sortPopulation()
            population = pop.get_population()


            #defina a população sobrevivente

        #liste os melhores indivíduos
        print(population)
        print(len(population))
