from population import Population
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
        # define população inicial
        pop = Population()
        population = pop.definePopulation(config.MI)
        def minor(x, y): return x if x.get_cost() < y.get_cost() else y
        metric = 0
        metricPrev = 0
        cont = 0
        # avalie a população

        # critério de parada
        for i in range(50):
            metricPrev = metric

            #sizePopulation = len(population)
            for j in range(round(config.LAMBDA/2)):
                # selecione os pais

                aux1 = population[np.random.randint(0, len(population))]
                aux2 = population[np.random.randint(0, len(population))]
                
                P1 = minor(aux1, aux2)
                aux1 = population[np.random.randint(0, len(population))]
                aux2 = population[np.random.randint(0, len(population))]
                P2 = minor(aux1, aux2)

                # Crossover

                rand = np.random.random()
                # print(rand)
                # print(P1)
                # print(P2)
                child = []
                if rand > 0.5:
                    child = cross.OBX(P1, P2)
                else:
                    child = cross.PMX(P1, P2)
                # print("child: \n")
                # print(child)
                for a in range(2):
                    for i, c1 in enumerate(child[a]):
                        for j, c2 in enumerate(child[a]):
                            if i != j and c1 == c2:
                                print("Elementos iguais")
                                exit(1)

                cluster = SplitDepots.splitByDepot(child[0])
                # print(cluster)
                individual1 = split.splitLinearBounded(cluster)
                cluster = SplitDepots.splitByDepot(child[1])
                # print(cluster)
                individual2 = split.splitLinearBounded(cluster)

                individual = [individual1, individual2]

                # print("individual: ")
                # print(individual1)
                # print(individual2)
                # for a in range(2):
                #     for i, c1 in enumerate(individual[a].get_giantTour()):
                #         for j, c2 in enumerate(individual[a].get_giantTour()):
                #             if i != j and c1 == c2:
                #                 print("Elementos iguais no split")
                #                 exit(1)

                # Mutação
                if np.random.random() < config.PROB_MUTATION:
                    individual1 = Mutation.mutation(individual1)
                if np.random.random() < config.PROB_MUTATION:
                    individual2 = Mutation.mutation(individual2)
                # print("individual: ")
                # print("indivíduo: "+str(individual))
                # print(individual.get_routes())
                # pop.addIndividual(individual)
                # pop.sortPopulation()

                individual = [individual1, individual2]

                for a in range(2):
                    for i, c1 in enumerate(individual[a].get_giantTour()):
                        for j, c2 in enumerate(individual[a].get_giantTour()):
                            if i != j and c1 == c2:
                                print("Elementos iguais na mutação")
                                exit(1)

                # avalie a população
                for i in range(2):
                    # indivíduo diferente do resto da população
                    if pop.is_different(individual[i]):
                        pop.addIndividual(individual[i])

                pop.sortPopulation()
                population = pop.get_population()

            # defina a população sobrevivente
            metric = pop.defineSurvivors(config.MI)

            # verifica se houve evolução na população
            if round(metricPrev,2) == round(metric,2):
                cont += 1
            if cont>5:
                print("ALERTA POPULAÇÃO PAROU DE EVOLUIR")
                population = pop.get_population()
                print(population)
                exit(1)

            population = pop.get_population()

        # liste os melhores indivíduos
        print(population)
        print(len(population))
