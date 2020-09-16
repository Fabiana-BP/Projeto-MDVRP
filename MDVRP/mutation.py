from distances import Distances as dist
import copy

class Mutation:

    def mutation(solution):
        return ""

    '''
    Método aplica a regra: Se u for um nó cliente, remova u e insira-o após v
    '''
    def M1(solution):
        solution1 = copy.deepcopy(solution)
        customers = solution1.get_giantTour()
        routes = solution1.get_routes()
        for routeU in solution1.get_routes():
            for i,u in enumerate(routeU.get_tour()):
                for routeV in solution1.get_routes():
                    for j,v in enumerate(routeV.get_tour()):
                        if u is not v: #se eles são diferentes
                            #verificar se há melhora na solução com o procedimento
                            costRouteU = routeU.costWithoutNode(u)
                            costRouteV = routeV.costWithNode(v,j+1)
                            newCost = solution.get_cost() - routeU.get_totalCost() - routeV.get_totalCost() + costRouteU[0] + costRouteV[0]
                            #melhora a solução:
                            if newCost < solution.get_cost():
                                #remove u
                                U = routeU.popCustomer(i)
                                #insere u após v
                                routeV.insertCustomer(U,j+1)
                                #atualizar custos das rotas
                                routeU.set_cost(costRouteU[1],costRouteU[2],costRouteU[3])
                                routeV.set_cost(costRouteV[1],costRouteV[2],costRouteV[3])
                                #atualizar giantTour
                                solution1.formGiantTour()
                                solution1.calculateCost()
                                return solution1

        return solution
