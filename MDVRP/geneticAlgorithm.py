from population import Population
from crossover import Crossover as cross
from splitDepots import SplitDepots
from splitAlgorithms import SplitAlgorithms as split
from mutation import Mutation
from localSearchBest import LocalSearchBest as lsb
from localSearchFirst import LocalSearch as ls
import numpy as np
import config
import concurrent.futures
import copy
import time
import traceback
import threading as th

mutex = th.Semaphore(1)
newIndividuals = [] # indivíduos obtidos na busca local best improvement

class GeneticAlgorithm:
    '''
    Método responsável pelo algoritmo genético
    '''

    def GA(self,seed):
        global mutex
        global newIndividuals
        np.random.seed(seed)
        # define população inicial
        pop = Population()
        population = pop.definePopulation(config.SIZE_POP)
        def minor(x, y): return x if x.get_cost() < y.get_cost() else y
        best = 0
        bestPrev = 0
        controlPop = True
        controlPopPrev = True
        sumControl = 0
        cont = 0
        timeControl = 0
        # avalie a população

        # critério de parada
        i = 0
        while i < config.GEN and cont <= config.GEN_NO_EVOL and timeControl < config.TIME_TOTAL :
            tAllIni = time.time()
            bestPrev = best
            controlPopPrev = controlPop
            tLS = 0

            #sizePopulation = len(population)
            descendant = []
            for j in range(round(config.SIZE_DESC/2)):
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
                            traceback.print_exc()
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
                    if self.is_different(modIndividuals[a],descendant):
                        #pop.addIndividual(modIndividuals[a])
                        descendant.append(modIndividuals[a])

                # pop.sortPopulation()
                # population = pop.get_population()
            # inserir descendentes à população
            for desc in descendant:
                if pop.is_different(desc):
                    pop.addIndividual(desc)
            
            # inserir indivíduos da lista newIndividuals (se existir) à população

            #início seção crítica
            mutex.acquire()
            # print("verificar lista")
            # print(newIndividuals)
            if newIndividuals:
                # print("novo: "+ str(len(newIndividuals)))
                for ni in newIndividuals:
                    if pop.is_different(ni):
                        # print("achou assíncrona")
                        pop.addIndividual(ni)
                newIndividuals = []
            mutex.release()
            #fim seção crítica
            
            pop.sortPopulation()
            population = pop.get_population()
            # promoção

            p = max(round(config.SIZE_POP * 0.1),1) #10% da população
            LSBetter = ls()
         
            modIndividuals =  []
            individuals = []
            selProbalities = pop.get_selProbabilities() # probabilidade de seleção
            individuals = np.random.choice(population,p,replace=False,p=selProbalities)
            individuals = np.append(individuals, pop.showBestSolution())
            with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
                    future_to_individual = {executor.submit(LSBetter.LS,ind,where='ls'): ind for ind in individuals}
                    for future in concurrent.futures.as_completed(future_to_individual):
                        ind = future_to_individual[future]
                        try:
                            indiv = future.result()
                            modIndividuals.append(indiv)
                        except Exception as exc:
                            print('%s gerou uma exceção na busca local - promoção: %s' % (str(ind), exc))
                            traceback.print_exc()
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
            best = pop.defineSurvivors(config.SIZE_POP)
            population = pop.get_population()
            
            #busca local exaustiva - best improvemment
            # p = 3 # 3 threads
            individuals = []
            # selProbalities = pop.get_selProbabilities() # probabilidade de seleção
            # individuals = np.random.choice(population,(p-1),replace=False,p=selProbalities)
            individuals = np.append(individuals, pop.showBestSolution())
            individuals = np.append(individuals, pop.showSecondBestSolution())
            
            # cria threads 
            for individual in individuals:
                if np.random.random() < config.PROB_LS_BEST:
                    if th.active_count()<3: # máximo 3 threads agindo de forma assíncrona
                        a = MyThread(individual) #inicializa thread
                        a.start()

            
            if i >= config.GEN and cont >= config.GEN_NO_EVOL and timeControl > config.TIME_TOTAL:
                print("th.active_count(): "+str(th.active_count()))
                # não finalizar o programa enquanto tiver thread ativa
                while th.active_count()>0:
                    continue
                if not newIndividuals:
                     for ni in newIndividuals:
                        if pop.is_different(ni):
                            pop.addIndividual(ni)
               
                pop.sortPopulation()
                best = pop.defineSurvivors(config.SIZE_POP)
            
            if round(bestPrev,9) == round(best,9):
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
            pop.sortPopulation()
            population = pop.get_population()
            tAll = (time.time() - tAllIni)/60
            timeControl += tAll

            print("GERAÇÃO: {} - Custo: {} - Tempo LS: {} - Tempo LS Promotion: {} - Tempo Total: {}".format(i,
                                                   pop.showBestSolution().get_cost(),tLS,tTotalP,tAll))

            i += 1

        # liste os melhores indivíduos
        # print(population)
        # print(len(population))
        return pop.showBestSolution()
        
    def is_different(self, solution,descendant):
        for d in descendant:
            if solution.get_cost() == d.get_cost():
                return False
        return True
    
class MyThread(th.Thread):

    def __init__(self, solution):
        th.Thread.__init__(self)
        self._solution = solution

    def run(self):
        global mutex
        global newIndividuals
        LSB = lsb()
        # print("executando thread")
        # print("solution: "+str(self._solution)+"\n")
        individual = LSB.LS(self._solution)
        # print("individual: "+ str(individual)+"\n")
        cont = 0

        #seção crítica
        mutex.acquire()
        for ind in newIndividuals:
            if ind.get_cost() == individual.get_cost():
                cont = 1
                break
        if cont == 0:
            newIndividuals.append(individual)
        mutex.release()
        # print("saiu da thread")
