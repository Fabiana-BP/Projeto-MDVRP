from population import Population
from crossover import Crossover as cross
from splitDepots import SplitDepots
from splitAlgorithms import SplitAlgorithms as split
from mutation import Mutation
from localSearch import LocalSearch as ls
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
        best = 0
        bestPrev = 0
        cont = 0
        # avalie a população

        # critério de parada
        i = 0
        while i < config.GEN and cont <= config.GEN_NO_EVOL:
            bestPrev = best

            #sizePopulation = len(population)
            for j in range(round(config.LAMBDA/2)):
                # selecione os pais

                aux1 = population[np.random.randint(len(population))]
                aux2 = population[np.random.randint(len(population))]

                P1 = minor(aux1, aux2)
                aux1 = population[np.random.randint(len(population))]
                aux2 = population[np.random.randint(len(population))]
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
                    for e1, c1 in enumerate(child[a]):
                        for e2, c2 in enumerate(child[a]):
                            if e1 != e2 and c1 == c2:
                                print("Elementos iguais")
                                exit(1)
                # Mutação
                if np.random.random() < config.PROB_MUTATION:
                    child[0] = Mutation.mutation(child[0])
                if np.random.random() < config.PROB_MUTATION:
                    child[1] = Mutation.mutation(child[1])

                # split
                cluster = SplitDepots.splitByDepot(child[0])
                # print(cluster)
                individual1 = split.splitLinear(cluster)
                cluster = SplitDepots.splitByDepot(child[1])
                # print(cluster)
                individual2 = split.splitLinear(cluster)

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

                # Busca Local
                if np.random.random() < config.PROB_LS:
                    individual1 = ls.LS(individual1)
                if np.random.random() < config.PROB_LS:
                    individual2 = ls.LS(individual2)
                # print("individual: ")
                # print("indivíduo: "+str(individual))
                # print(individual.get_routes())
                # pop.addIndividual(individual)
                # pop.sortPopulation()

                individual = [individual1, individual2]

                for a in range(2):
                    for e1, c1 in enumerate(individual[a].get_giantTour()):
                        for e2, c2 in enumerate(individual[a].get_giantTour()):
                            if e1 != e2 and c1 == c2:
                                print("Elementos iguais na mutação")
                                exit(1)

                # avalie a população
                for a in range(2):
                    # indivíduo diferente do resto da população
                    if pop.is_different(individual[a]):
                        pop.addIndividual(individual[a])

                pop.sortPopulation()
                population = pop.get_population()

            # defina a população sobrevivente
            best = pop.defineSurvivors(config.MI)

            # verifica se houve evolução na população
            if bestPrev == best:
                cont += 1
            else:
                cont = 0
            if cont > config.GEN_NO_EVOL:
                print("ALERTA POPULAÇÃO PAROU DE EVOLUIR")

            population = pop.get_population()

            print("GERAÇÃO: {} - Custo: {}".format(i,
                                                   pop.showBestSoution().get_cost()))

            i += 1

        # liste os melhores indivíduos
        print(population)
        print(len(population))
