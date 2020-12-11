'''
Arquivo responsável por carregar a aplicação
@author Fabiana Barreto Pereira
'''
from readingDatas import ReadingDatas
from customers import Customers
from depots import Depots
from distances import Distances
from geneticAlgorithm import GeneticAlgorithm as GA
from writingSolutions import WritingSolutions as Write
import numpy as np
import time
import math
import config


def main():
    seed = 7890
    nInstance = 0  # número da instância - 1
    instance = config.INSTANCES[nInstance]
    # recebendo instâncias
    r = ReadingDatas(config.DIRECTORY_DATAS+instance)
    r.readFile()
    # adicionando clientes
    Customers.addCustomers(r)
    # for cst in Customers.get_customersList().values():
    # print(cst)

    # adicionando depósitos
    Depots.addDepots(r)
    # print("\n\n\n\")
    # for dpt in Depots.get_depotsList().values():
    # print(dpt)

    # cálculo das distâncias
    Distances.euclidianDistanceAll(
        Customers.get_customersList(), Depots.get_depotsList())

    # for cst in Customers.get_customersList():
    #     print(cst)
    #     print(Customers.get_customersList()[cst].get_depotsDistances())
    # print("\n\n\n")
    # for cst in Customers.get_customersList():
    #     print(cst)
    #     print(Customers.get_customersList()[cst].get_neighborsDistances())
    # exit(1)
    minor = math.inf
    bestSolution = None
    mTime = 0
    mCost = 0

    for i in range(config.N_REPETITIONS):
        write = Write(config.DIRECTORY_RESULT+instance)
        ini = time.time()
        ga = GA()
        best = ga.GA(seed)
        print(best)
        cost = best.get_cost()
        if cost < minor:
            minor = best.get_cost()
            bestSolution = best
        write.writeFile(best)
        end = (time.time() - ini)/60
        mTime += end
        mCost += cost
        print("tempo: "+str(end))
    mTime /= config.N_REPETITIONS
    mCost /= config.N_REPETITIONS

    # calcular gap
    def gap(indexInstance, cost): return (
        100*((cost - config.BST_COST[indexInstance])/config.BST_COST[indexInstance]))

    print("gap médio: "+str(gap(nInstance, mCost))+" \n gap melhor: "+str(gap(nInstance, minor)) +
          " \n custo médio: "+str(mCost)+" \n melhor custo: "+str(minor)+" \n tempo médio: "+str(mTime)+"\n")


if __name__ == "__main__":
    main()
