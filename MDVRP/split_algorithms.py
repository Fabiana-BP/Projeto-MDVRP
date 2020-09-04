
from depots import Depots as dpts
from customers import Customers as csts
from distances import Distances as dist
from route import Route
from solution import Solution
import math
import copy

class Split_algorithms:
    _infinite = math.inf


    '''
    Método monta as rotas de cada depósito usando algoritmo proposto por Prins2004
    '''
    def mountRoutes(solution):
        allDepots = dpts.get_depotsList()
        numberDepots = dpts.get_numberDepots()
        customers = solution.get_giantTour()
        depots = solution.get_depots()
        numberVehicles = depots[0].get_numberVehicles()

        #depósitos já vem separados, utilizar heurística de Prins2004 para separar as rotas

        #separar conjuntos
        for i in allDepots:
            depot = allDepots[i]
            path=[]
            for j in range(len(customers)):
                if str(depot.get_id()) == str(depots[j].get_id()):
                    path.append(customers[j])

            #gerar rotas para cada caminho
            pred = Split_algorithms.splitRoute(path, depot) #método retorna lista de predecessores
            allroutes = Split_algorithms.extractVRP(pred,path) #método retorna lista de lista com rotas para um depósito (número máximo de veículos não delimitado)
            #verificar número de rotas formadas

            routes = []
            for l in allroutes:
                if len(l)>0: #há rota
                    routes.append(l)

            #caso tenha mais rotas que veículos
            if len(routes) > numberVehicles:
                routes = sorted(routes,key=lambda x: x[1]) #ordenada em ordem crescente de demanda
                #juntar rotas com menor demanda
                aux = len(routes) - numberVehicles
                while aux>0:
                    r0 = routes[0][0]
                    r1 = routes[1][0]
                    r0 = r0 + r1
                    demand = routes[0][1] + routes[1][1]
                    routes[0]=[r0,demand]
                    del routes[1]
                    routes = sorted(routes,key=lambda x: x[1]) #ordenada em ordem crescente de demanda
                    aux -= 1



            k=-1
            for l in routes:
                route = Route(depot)
                if len(l)>0:
                    for m in l[0]:
                        route.addCustomer(m)
                        k += 1

                    #calcular custo da rota formada
                    route.startValues()
                    route.calculeCost()
                    solution.addRoutes(route)
        solution.formGiantTour()
        solution.calculateCost()
        #print(solution)
        return solution



    '''
    Método implementa split definido em Prins2004
    recebe como parâmetro caminho de um depósito
    '''
    def splitRoute(path,depot):
        n = len(path)
        vehicleCapacity = depot.get_loadVehicle()
        durationRoute = depot.get_durationRoute()
        v = [] # custo do menor caminho do depósito até o ponto.
        predecessor=[] #predecessores de cada idCsts neste caminho
        predecessor.append(-1) #depósito não tem precedente
        v.append(0.0)
        for i in range(n):
            v.append(Split_algorithms._infinite)
            predecessor.append("")

        for i in range(1,n+1):
            load = 0.0
            cost = 0.0
            j = i
            duration = 0
            while (j <= n) and (load <= vehicleCapacity) and (duration <= durationRoute):
                customer = path[j-1]
                load += customer.get_demand()
                if i == j:
                    # custo de ida e volta
                    duration += customer.get_duration()
                    cost = 2 * dist.euclidianDistance(customer.get_x_coord(),customer.get_y_coord(),depot.get_x_coord(),depot.get_y_coord()) + customer.get_duration()
                else:
                    duration += customer.get_duration()
                    previewCustomer = path[j-2]
                    cost = cost - dist.euclidianDistance(previewCustomer.get_x_coord(),previewCustomer.get_y_coord(),depot.get_x_coord(),depot.get_y_coord()) + dist.euclidianDistance(previewCustomer.get_x_coord(),previewCustomer.get_y_coord(),customer.get_x_coord(),customer.get_y_coord()) + customer.get_duration() + dist.euclidianDistance(customer.get_x_coord(),customer.get_y_coord(),depot.get_x_coord(),depot.get_y_coord())

                if (load <= vehicleCapacity) and (duration <= durationRoute):
                    if (v[i-1] + cost) < v[j]:
                        v[j] = v[i-1] + cost
                        predecessor[j] = i-1
                    j += 1
        return predecessor


    '''
    Método para extrair a solução VRP do vetor P
    definido em Prins2004
    retorna uma lista de trips onde cada índice contém uma lista de visitação e a demanda total destes clientes
    '''
    def extractVRP(listPredecessors, listCustomers):
        trip = []
        totalDemand = []
        n = len(listPredecessors) - 1
        for i in range(1,n+1):
            trip.append([])
            totalDemand.append(0)
        t = 0
        j = n
        while i != 0:
            t += 1
            i = listPredecessors[j]
            sumDemand = 0
            trp = []
            for k in range (i+1, j+1):
                trp.append(listCustomers[k-1])
                sumDemand += listCustomers[k-1].get_demand()
            trip[t] = [trp, sumDemand]
            j = i

        return trip
