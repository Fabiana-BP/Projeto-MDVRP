'''
Arquivo responsável por carregar a aplicação
@author Fabiana Barreto Pereira
'''
from readingDatas import ReadingDatas
from customers import Customers
from depots import Depots
from distances import Distances
from geneticAlgorithm import GeneticAlgorithm as GA
import numpy as np
import time


def main():
    seed = 7890
    # recebendo instâncias
    r = ReadingDatas("dat/p01")
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
    for i in range(5):
        ini = time.time()
        ga = GA()
        print(ga.GA(seed))
        end = (time.time() - ini)/60
        print("tempo: "+str(end))


if __name__ == "__main__":
    main()
