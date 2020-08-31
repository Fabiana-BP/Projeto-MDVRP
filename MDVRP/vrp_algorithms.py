
from depots import Depots as dpts
from customers import Customers as csts
from distances import Distances as dist
import math

class VRP_algorithms:
    _infinite = math.inf

    def mountRoutes(solution, typeSplit):
        customers = csts.get_customersList()
        depots = dpts.get_depotsList()

        numberDepots = dpts.get_numberDepots()
        idCsts = solution.get_giantTour()
        idDepots = solution.get_depots()

        paths = [] #cada lista um caminho de um depósito
        #depósitos já vem separados, utilizar heurística de Prins2004 para separar as rotas
        if typeSplit == 'Prins_depotsSeparated':
            #separar conjuntos
            for i in depots:
                depot = depots[i]
                print(depot)
                path=[]
                for j in range(len(idCsts)):
                    if str(depot.get_id()) == str(idDepots[j]):
                        path.append(idCsts[j])
                #paths.append(path)
                #gerar rotas para cada caminho
                print("\ncaminho:\n")
                #print(path)
                pred = VRP_algorithms.splitRoute(path, depot) #método retorna lista de predecessores
                print(pred)



    '''
    Método implementa split definido em Prins2004
    recebe como parâmetro caminho de um depósito
    '''
    def splitRoute(path,depot):
        customers = csts.get_customersList()
        depots = dpts.get_depotsList()
        n = len(path)
        vehicleCapacity = dpts.get_loadVehicle()
        durationRoute = dpts.get_durationRoute()
        v = [] # custo do menor caminho do depósito até o ponto.
        predecessor=[] #predecessores de cada idCsts neste caminho
        v.append(0.0)
        for i in range(n):
            v.append(VRP_algorithms._infinite)
            predecessor.append("")

        for i in range(1,(n+1)):
            load = 0.0
            cost = 0.0
            j = i
            duration = 0
            while (j < n) and (load <= vehicleCapacity):
                customer = customers[str(path[j-1])]
                load += customer.get_demand()
                if i == j:
                    # custo de ida e volta
                    duration += customer.get_duration()
                    cost = 2 * dist.euclidianDistance(customer.get_x_coord(),customer.get_y_coord(),depot.get_x_coord(),depot.get_y_coord()) + customer.get_duration()
                else:
                    duration += customer.get_duration()
                    previewCustomer = customers[str(path[j-2])]
                    cost = cost - dist.euclidianDistance(previewCustomer.get_x_coord(),previewCustomer.get_y_coord(),depot.get_x_coord(),depot.get_y_coord()) + dist.euclidianDistance(previewCustomer.get_x_coord(),previewCustomer.get_y_coord(),customer.get_x_coord(),customer.get_y_coord()) + customer.get_duration() + dist.euclidianDistance(customer.get_x_coord(),customer.get_y_coord(),depot.get_x_coord(),depot.get_y_coord())

                if (load <= vehicleCapacity):
                    if (v[i-1] + cost) < v[j]:
                        v[j] = v[i-1] + cost
                        predecessor[j-1] = i-1 #j-1 pois está associado a lista de clientes 0 a n-1

                    j +=1
        return predecessor


        '''
        Método para extrair a solução VRP do vetor P
        definido em Prins2004
        '''
        def extractVRP(listPredecessors,numberTrips):
            return ''
