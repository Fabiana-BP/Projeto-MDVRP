from depots import Depots as dpts
from customers import Customers as csts
from splitDepots import SplitDepots
from splitAlgorithms import SplitAlgorithms as split
from solution import Solution
from auxiliary_heuristics import NearestNeighbor
from mutation import Mutation as mt
from localSearchFirst import LocalSearch as ls
#from localSearch import LocalSearch as ls
import config
import numpy as np


class Population:

    def __init__(self):
        self._population = []  # lista de Solution ordenada em ordem crescente de custo
        self._selProbabilities = []  # lista de probabilidade de seleção de cada indivíduo

    '''
    Método define população inicial
    '''

    def definePopulation(self, size):
        LS = ls()
        # Heurística do vizinho mais próximo
        customers = list(csts.get_customersList().values())
        cst0 = customers[np.random.randint(len(customers)-1)]
        tour = NearestNeighbor.nearestNeighbor(cst0)
        cluster = SplitDepots.splitByDepot(tour)
        # criação de rotas por depósitos, individual é um Solution
        individual = split.splitLinear(cluster)
        # print(individual)
        # print(individual.get_routes())
        rand = np.random.random()
        if rand < config.PROB_LS_POP:
            individual = LS.LS(individual)
        self.addIndividual(individual)
        # print(individual)
        # exit(1)
        # print(individual.get_routes())
        # exit(1)

        # “cluster first and then route”
        cluster = SplitDepots.GilletJohnson()  # divisão por depósitos

        # criação de rotas por depósitos, individual é um Solution
        individual = split.splitLinear(cluster)
        # print(individual)
        # print(individual.get_routes())
        rand = np.random.random()
        if rand < config.PROB_LS_POP:
            individual = LS.LS(individual)
        # print(individual)
        # print(individual.get_routes())

        if individual is not None and self.is_different(individual):
            self.addIndividual(individual)
        # for i in self._population:
        #     print(i)
        #     self.verifyNodes(i)
        # exit(1)

        # formação de rotas aleatórias
        self.formRandomPopulation(size)

        self.sortPopulation()

        
        print(len(self._population))

        return self._population

    def formRandomPopulation(self,size):
        LS = ls()
        for i in range(2 * size):
            if len(self._population) >= size:
                break
            #seed = i + int(seed * np.random.random())
            cluster = SplitDepots.randomDistribution()
            # criação de rotas por depósitos, individual é um Solution
            individual = split.splitLinear(cluster)
            # print(individual)
            # print(individual.get_routes())
            rand = np.random.random()
            if rand < config.PROB_LS_POP:
                individual = LS.LS(individual)
            if individual is not None and self.is_different(individual):
                self.addIndividual(individual)
            # print(individual)
            # print(individual.get_routes())
            # exit(1)

    def verifyNodes(self, solution):
        tour = solution.get_giantTour()
        for i, c1 in enumerate(tour):
            for j, c2 in enumerate(tour):
                if i != j and c1 == c2:
                    print("Elementos iguais")
                    exit(1)

    '''
    Método define as soluções sobreviventes (as de menor custo)
    @return melhor custo da população
    '''

    def defineSurvivors(self, size):
        del self._population[0:(len(self._population)-size)]
        self.sortPopulation()
        return self.showBestSoution().get_cost()
    
    def changePopulation(self):
        print('mudou população')
        # print(self._population)
        lenght = len(self._population)
        sizeSurvivors = max(1,round(lenght*0.1))
        del self._population[0:(len(self._population)-sizeSurvivors)]
        self.definePopulation(config.MI)
        # self.sortPopulation()
        # print('depois')
        # print(self._population)
        return self._population

    '''
    Método calcula o rank linear do indivíduo
    http://www.geatbx.com/docu/algindex-02.html#P244_16021
    '''

    def linearRanking(self, individual, pos):
        return 2 - config.SP + 2 * (config.SP - 1) * (pos/(len(self._population) - 1))

    '''
    Método adiciona indivíduo a população
    '''

    def addIndividual(self, solution):
        self._population.append(solution)

    '''
    Método remove o indivíduo de determinado índice da população
    @param índice do indivíduo a ser removido
    @return indivíduo removido ou -1
    '''

    def popIndividual(self, index):
        if index < len(self._population):
            individual = self._population.pop(index)
            return individual
        else:
            return -1

    '''
    Método ordena a população em linear ranking
    '''

    def sortPopulation(self):
        self.sortPopulationDesc()
        self._selProbabilities = []
        for i, individual in enumerate(self._population):
            ranking = self.linearRanking(individual, i)
            individual.set_ranking(ranking)
            self._selProbabilities.append(ranking/len(self._population))

        self._population = sorted(self._population, key=Solution.get_ranking)

    '''
    Método ordena a população em ordem decrescente de custo
    '''

    def sortPopulationDesc(self):
        self._population = sorted(
            self._population, key=Solution.get_cost, reverse=True)

    '''
    Método verifica a diversidade da população
    @return False caso métrica de diversidade for maior que config.METRIC
    '''

    def verifyDiversity(self):
        lenght = len(self._population)
        p = max(3,round(lenght * 0.15))
        # escolher p indivíduos aleatórios
        indexes = np.random.choice(lenght, p, replace=False)
        metric = 0
        for i in indexes:
            m = 0
            if i > 0 and i < lenght - 1:
                m = abs(self._population[i].get_cost() - self._population[i-1].get_cost(
                )) + abs(self._population[i].get_cost() - self._population[i+1].get_cost())
            elif i == 0:
                m = abs(self._population[i].get_cost() - self._population[lenght-1].get_cost(
                )) + abs(self._population[i].get_cost() - self._population[i+1].get_cost())
            else:
                m = abs(self._population[i].get_cost() - self._population[i-1].get_cost(
                )) + abs(self._population[i].get_cost() - self._population[0].get_cost())
        metric += m
        print(metric)
        # perdeu diversidade
        if metric <= config.METRIC:
            return False
        
        return True

    def get_population(self):
        return self._population

    def get_selProbabilities(self):
        return self._selProbabilities

    def changeIndividual(self, individual, index):
        self._population[index] = individual
        self.sortPopulation()

    '''
    Método verifica se há outro indivíduo com mesmo custo
    '''

    def is_different(self, solution):
        for p in self._population:
            if solution.get_cost() == p.get_cost():
                return False
        return True

    def showBestSoution(self):
        return self._population[len(self._population)-1]
