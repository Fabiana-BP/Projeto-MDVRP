'''
Arquivo responsável por carregar a aplicação
@author Fabiana Barreto Pereira
'''
from readingDatas import ReadingDatas
from customers import Customers
from depots import Depots
from distances import Distances
from route import Route
from solution import Solution
from initialPopulation import InitialPopulation
from vrp_algorithms import VRP_algorithms as VRP


def main():
    #recebendo instâncias
    r = ReadingDatas("dat/p01")
    r.readFile()
    #adicionando clientes
    Customers.addCustomers(r)
    #for cst in Customers.get_customersList().values():
        #print(cst)

    #adicionando depósitos
    Depots.addDepots(r)
    #print("\n\n\n\")
    #for dpt in Depots.get_depotsList().values():
        #print(dpt)

    #cálculo das distâncias
    Distances.euclidianDistanceAll(Customers.get_customersList(),Depots.get_depotsList())

    '''
    route = Route('52')
    route.addCustomer('8')
    route.addCustomer('9')
    route.addCustomer('10')
    route.calculeCost()
    route.get_totalCost()
    route.printRoute()
    route1 = Route('53')
    route1.addCustomer('11')
    route1.addCustomer('19')
    route1.addCustomer('20')
    route2 = Route('54')
    route2.addCustomer('22')
    route2.addCustomer('23')
    route2.addCustomer('25')

    solution = Solution()
    solution.addRoutes(route)
    solution.addRoutes(route1)
    solution.addRoutes(route2)
    print(solution.get_routes())
    solution.formGiantTour()
    solution.calculateCost()
    '''
    individual = InitialPopulation()
    individual.GilletJohnson()
    print("......")
    print(individual.get_population()[0])
    print("......")
    VRP.mountRoutes(individual.get_population()[0], 'Prins_depotsSeparated')
    print(individual.get_population()[0].calculateCost())




if __name__ == "__main__":
    main()
