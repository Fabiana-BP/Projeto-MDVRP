from population import Population
from crossover import Crossover as cross
from splitDepots import SplitDepots
from splitAlgorithms import SplitAlgorithms as split
from mutation import Mutation
#from localSearch import LocalSearch as ls
from localSearchFirst import LocalSearch as ls
import numpy as np
import config
import concurrent.futures
import copy
import time


class GeneticAlgorithm:

    '''
    Método responsável pelo algoritmo genético
    '''

    def GA(self,seed):
        np.random.seed(seed)
        # define população inici
        pop = Population()
        population = pop.definePopulation(config.MI)
        def minor(x, y): return x if x.get_cost() < y.get_cost() else y
        best = 0
        bestPrev = 0
        controlPop = True
        controlPopPrev = True
        sumControl = 0
        cont = 0
        # avalie a população

        # critério de parada
        i = 0
        while i < config.GEN and cont <= config.GEN_NO_EVOL:
            tAllIni = time.time()
            bestPrev = best
            controlPopPrev = controlPop
            tLS = 0

            #sizePopulation = len(population)
            for j in range(round(config.LAMBDA/2)):
                controlPop = True
                selProbalities = pop.get_selProbabilities() # probabilidade de seleção
                # print("pop: "+str(len(population)))
                # print("prob: "+str(len(selProbalities)))
                # selecione os pais
                aux = np.random.choice(population,2,replace=False,p=selProbalities)

                # aux1 = population[np.random.randint(len(population))]
                # aux2 = population[np.random.randint(len(population))]

                P1 = minor(aux[0], aux[1])

                aux = np.random.choice(population,2,replace=False,p=selProbalities)
                # aux1 = population[np.random.randint(len(population))]
                # aux2 = population[np.random.randint(len(population))]
                P2 = minor(aux[0], aux[1])

                # Crossover

                rand = np.random.random()
                # print(rand)
                # print(P1)
                # print(P2)
                children = []
                if rand > 0.5:
                    children = cross.OBX(copy.deepcopy(P1), copy.deepcopy(P2))
                else:
                    children = cross.PMX(copy.deepcopy(P1), copy.deepcopy(P2))
                # print("child: \n")
                # print(child)
                # for a in range(2):
                #     for e1, c1 in enumerate(children[a]):
                #         for e2, c2 in enumerate(children[a]):
                #             if e1 != e2 and c1 == c2:
                #                 print("Elementos iguais")
                #                 exit(1)

                # Mutação

                # duas threads
                modChildren =  []
                with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
                    future_to_child = {executor.submit(Mutation.mutation,child): child for child in children}
                    for future in concurrent.futures.as_completed(future_to_child):
                        child = future_to_child[future]
                        try:
                            indiv = future.result()
                            modChildren.append(indiv)
                        except Exception as exc:
                            print('%s gerou uma exceção na busca local: %s' % (str(child), exc))

                # split
                cluster = SplitDepots.splitByDepot(modChildren[0])
                # print(cluster)
                individual1 = split.splitLinear(cluster)
                cluster = SplitDepots.splitByDepot(modChildren[1])
                # print(cluster)
                individual2 = split.splitLinear(cluster)

                individuals = [individual1, individual2]

                # print("individual: ")
                # print(individual1)
                # print(individual2)
                for a in range(2):
                    for ii, c1 in enumerate(individuals[a].get_giantTour()):
                        for jj, c2 in enumerate(individuals[a].get_giantTour()):
                            if ii != jj and c1 == c2:
                                print("Elementos iguais na mutação")
                                exit(1)

                # Busca Local
                
                # duas threads
                ini = time.time()
                modIndividuals =  []
                LS = ls()
                # modIndividuals.append(LS.LS(individuals[0]))
                # modIndividuals.append(LS.LS(individuals[1]))
                with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
                    future_to_individual = {executor.submit(LS.LS,ind,nMovimentations='random' ,where='ls'): ind for ind in individuals}
                    for future in concurrent.futures.as_completed(future_to_individual):
                        ind = future_to_individual[future]
                        try:
                            indiv = future.result()
                            modIndividuals.append(indiv)
                        except Exception as exc:
                            print('%s gerou uma exceção na busca local: %s' % (str(ind), exc))
                # print(future_to_individual)
                # print(individuals[0])
                # print(modIndividuals)
                # exit(1)
                tTotal = (time.time() - ini)/60
                tLS += tTotal
                for a in range(2):
                    for e1, c1 in enumerate(modIndividuals[a].get_giantTour()):
                        for e2, c2 in enumerate(modIndividuals[a].get_giantTour()):
                            if e1 != e2 and c1 == c2:
                                print("Elementos iguais na busca local")
                                exit(1)
                # exit(1)
                # avalie a população
                for a in range(2):
                    # indivíduo diferente do resto da população
                    if pop.is_different(modIndividuals[a]):
                        pop.addIndividual(modIndividuals[a])

                pop.sortPopulation()
                population = pop.get_population()
                
            # promoção

            p = max(round(config.LAMBDA * 0.1),1) #10% da população
            ini = time.time()
            LSBest = ls()
            # if np.random.random() < config.PROB_LS:
            #     bestIndividual = LSBest.LS(population[0])
            #     if pop.is_different(bestIndividual):
            #         pop.addIndividual(bestIndividual)
            #         population = pop.get_population()
            modIndividuals =  []
            individuals = []
            selProbalities = pop.get_selProbabilities() # probabilidade de seleção
            individuals = np.random.choice(population,p,replace=False,p=selProbalities)
            individuals = np.append(individuals, pop.showBestSoution())
            with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
                    future_to_individual = {executor.submit(LSBest.LS,ind,where='ls'): ind for ind in individuals}
                    for future in concurrent.futures.as_completed(future_to_individual):
                        ind = future_to_individual[future]
                        try:
                            indiv = future.result()
                            modIndividuals.append(indiv)
                        except Exception as exc:
                            print('%s gerou uma exceção na busca local - promoção: %s' % (str(ind), exc))

            #exit(1)
            # avalie a população
            for a in modIndividuals:

                for e1, c1 in enumerate(a.get_giantTour()):
                        for e2, c2 in enumerate(a.get_giantTour()):
                            if e1 != e2 and c1 == c2:
                                print("Elementos iguais na busca local - promoção")
                                exit(1)

                # indivíduo diferente do resto da população
                if pop.is_different(a):
                    pop.addIndividual(a)

            tTotalP = (time.time() - ini)/60

            pop.sortPopulation()

            # defina a população sobrevivente
            best = pop.defineSurvivors(config.MI)

            # verifica se houve evolução na população
            # print("pop.verifyDiversity(): "+ str(pop.verifyDiversity()))
            # if not pop.verifyDiversity():
            #     # print("Baixa diversidade")
            #     controlPop = False # perdeu diversidade
            #     if controlPop == controlPopPrev:
            #         # print("contando")
            #         sumControl += 1
            #         # print("controlPop "+str(controlPop))
            #         # print("controlPopPrev "+str(controlPopPrev))
            # else:
            #     # print("Entrou aqui")
            #     sumControl = 0
                
            
            if bestPrev == best:
                cont += 1
            else:
                cont = 0
            # if sumControl > config.CONT_METRIC:
            #     # idum = i * seed
            #     population = pop.changePopulation()
            #     sumControl = 0
            if cont > config.GEN_NO_EVOL:
                # population = pop.changePopulation()
                # cont = 0
                print("ALERTA POPULAÇÃO PAROU DE EVOLUIR")

            population = pop.get_population()
            tAll = (time.time() - tAllIni)/60

            print("GERAÇÃO: {} - Custo: {} - Tempo LS: {} - Tempo LS Promotion: {} - Tempo Total: {}".format(i,
                                                   pop.showBestSoution().get_cost(),tLS,tTotalP,tAll))

            i += 1

        # liste os melhores indivíduos
        # print(population)
        # print(len(population))
        return pop.showBestSoution()
        
