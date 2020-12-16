from distances import Distances as dist
from depots import Depots as dpts
import copy
import config
import numpy as np
import random
import math

'''
Pesquisa local de Prins2004
'''


class LocalSearch:
    '''
    Cada iteração varre todos os pares possíveis de nós distintos (u,v). Esses nós podem pertencer à mesma viagem ou a viagens diferentes
    e um deles pode ser o depósito. x e y são os sucessores de u e v em suas respectivas viagens.
    @param Where opcional, para indicar onde o método é chamado, opções: None default ou 'ls'
    @param nMovimentations, para indicar se serão utilizados todos os movimentos ou apenas alguns. Opções: 'all' default ou 'random'
    '''

    def LS(self, solution, nMovimentations='all', where=None):

        movimentation = [self.M1, self.M2, self.M3, self.M4, self.M5,
                         self.M6, self.M7, self.M8, self.M9, self.M10]
        lenght = len(movimentation)
        prob = 0#config.PROB_LS
        # embaralhar os movimentos
        if nMovimentations == 'random':
            n = max(2,round(0.8*lenght))
            p = np.random.randint(1, n+1)
            movimentation = np.random.choice(movimentation, p, replace=False)
        else:
            # p = np.random.randint(1,lenght)
            prob = config.PROB_LS_BEST
            movimentation = np.random.choice(
                movimentation, lenght, replace=False)

        bestSolution = None
        bestSolution = copy.deepcopy(solution)

        if (where == 'ls' and np.random.random() < prob) or where == None:
            # print("vai mudar")
            # print(bestSolution)
            # print(bestSolution.get_routes())
            for i, m in enumerate(movimentation):
                # print(m)
                # print(solution)
                # print(solution.get_routes())
                # print("vai passar .................")
                solution1 = None
                solution1 = m(bestSolution)
                # tour = solution1.get_giantTour()
                # for i, c1 in enumerate(tour):
                #     for j, c2 in enumerate(tour):
                #         if i != j and c1 == c2:
                #             print("Elementos iguais na LS first")
                #             exit(1)
                # print(m)
                # print(solution1)
                # print(solution1.get_routes())
                # for r in solution1.get_routes():
                #     demand = 0
                #     for c in r.get_tour():
                #         demand += c.get_demand()
                #     if demand != r.get_totalDemand():
                #         print("demandas diferentes")
                #         print(r)
                #         print(c)
                #         print("demand: "+ str(demand))
                #         print("totalDemand: "+str(r.get_totalDemand()))
                #         exit(1)

                if solution1.get_cost() < bestSolution.get_cost():
                    bestSolution = copy.deepcopy(solution1)
                    # print("achou melhor")
                else:
                    # excluir rotas vazias
                    bestSolution.removeRoutesEmpty()
                    # print("bestSolution")
                    # print(bestSolution)
                    return bestSolution

            # excluir rotas vazias
            bestSolution.removeRoutesEmpty()
            # print("não achou melhor")
        return bestSolution

    '''
    Método aplica a regra: Se u for um nó cliente, remova u e insira-o após v
    '''

    def M1(self, solution):
        solution1 = None
        solution1 = copy.deepcopy(solution)
        # print(solution1.get_routes())
        for routeU in solution1.get_routes():
            for i, u in enumerate(routeU.get_tour()):
                costRouteU = routeU.costWithoutNode(i)
                for routeV in solution1.get_routes():
                    for j, v in enumerate(routeV.get_tour()):
                        if u != v:  # se eles são diferentes
                            newCost = math.inf
                            indJ = j
                            # print(u)
                            # print(v)
                            if u in routeV.get_tour() and v in routeU.get_tour():  # pertencem a mesma rota
                                # print("mesma rota")
                                auxRouteU = copy.deepcopy(routeU)
                                auxRouteU.popCustomer(i)
                                auxRouteU.set_cost(
                                    costRouteU[1], costRouteU[2], costRouteU[3])
                                if j > i:
                                    indJ = j - 1
                                costRouteV = auxRouteU.costWithNode(u, indJ+1)
                                newCost = solution.get_cost() - routeU.get_totalCost() + \
                                    costRouteV[0]
                            else:
                                # print("rotas diferentes")
                                costRouteV = routeV.costWithNode(u, indJ+1)
                                newCost = solution.get_cost() - routeU.get_totalCost() - \
                                    routeV.get_totalCost() + \
                                    costRouteU[0] + costRouteV[0]

                            # melhora a solução:
                            if newCost < solution.get_cost():
                                # remove u
                                U = routeU.popCustomer(i)
                                # insere u após v
                                routeV.insertCustomer(U, indJ+1)
                                # atualizar custos das rotas
                                routeU.set_cost(
                                    costRouteU[1], costRouteU[2], costRouteU[3])
                                routeV.set_cost(
                                    costRouteV[1], costRouteV[2], costRouteV[3])
                                # atualizar giantTour
                                solution1.formGiantTour()
                                solution1.calculateCost()
                                # print("rotas")

                                return solution1

                    # caso v seja o depósito
                    newCost = math.inf
                    if u in routeV.get_tour():  # pertencem a mesma rota
                        auxRoute = None
                        auxRouteU = copy.deepcopy(routeU)
                        auxRouteU.popCustomer(i)
                        auxRouteU.set_cost(
                            costRouteU[1], costRouteU[2], costRouteU[3])
                        costRouteV = auxRouteU.costWithNode(u, 0)
                        newCost = solution.get_cost() - routeU.get_totalCost() + \
                            costRouteV[0]
                    else:
                        costRouteV = routeV.costWithNode(u, 0)
                        newCost = solution.get_cost() - routeU.get_totalCost() - \
                            routeV.get_totalCost() + \
                            costRouteU[0] + costRouteV[0]
                    # melhora a solução:
                    if newCost < solution.get_cost():
                        # print("no depósito")
                        # remove u
                        U = routeU.popCustomer(i)
                        # insere u após v
                        routeV.insertCustomer(U, 0)
                        # atualizar custos das rotas
                        routeU.set_cost(
                            costRouteU[1], costRouteU[2], costRouteU[3])
                        routeV.set_cost(
                            costRouteV[1], costRouteV[2], costRouteV[3])
                        # atualizar giantTour
                        solution1.formGiantTour()
                        solution1.calculateCost()
                        return solution1

        return solution

    '''
    Método aplica a regra: Se u e x forem clientes, remova-os e insira (u,x) após v
    '''

    def M2(self, solution):
        return self.M2orM3(solution, "M2")

    '''
    Método aplica a regra: Se u e x forem clientes, remova-os e insira (x,u) após v
    '''

    def M3(self, solution):
        return self.M2orM3(solution, "M3")

    '''
    Método aplica a regra: type: M2 -> Se u e x forem clientes, remova-os e insira (u,x) após v
                           type: M3 -> Se u e x forem clientes, remova-os e insira (x,u) após v
    '''

    def M2orM3(self, solution, type):
        solution1 = copy.deepcopy(solution)
        # print(solution1)
        for routeU in solution1.get_routes():
            for i, u in enumerate(routeU.get_tour()):
                if i+1 < len(routeU.get_tour()):
                    costRouteU = routeU.costWithout2Nodes(i)
                    for routeV in solution1.get_routes():
                        for j, v in enumerate(routeV.get_tour()):
                            # se u e x são diferentes de v
                            if u != v and routeU.get_tour()[i+1] != v:
                                newCost = math.inf
                                indJ = j
                                if routeU is routeV:  # se pertencem a mesma rota:
                                    if j > i:
                                        indJ = j - 2
                                    auxRouteU = copy.deepcopy(routeU)
                                    auxRouteU.popCustomer(i)
                                    auxRouteU.popCustomer(i)
                                    auxRouteU.set_cost(
                                        costRouteU[1], costRouteU[2], costRouteU[3])
                                    if type.upper() == "M2":
                                        costRouteV = auxRouteU.costWith2Nodes(
                                            u, routeU.get_tour()[i+1], indJ+1)
                                    elif type.upper() == "M3":
                                        costRouteV = auxRouteU.costWith2Nodes(
                                            routeU.get_tour()[i+1], u, indJ+1)
                                    else:
                                        print("ERROR - método incorreto")
                                        exit(1)
                                    newCost = solution.get_cost() - routeU.get_totalCost() + \
                                        costRouteV[0]
                                    del auxRouteU
                                else:
                                    if type.upper() == "M2":
                                        costRouteV = routeV.costWith2Nodes(
                                            u, routeU.get_tour()[i+1], indJ+1)
                                    elif type.upper() == "M3":
                                        costRouteV = routeV.costWith2Nodes(
                                            routeU.get_tour()[i+1], u, indJ+1)
                                    else:
                                        print("ERROR - método incorreto")
                                        exit(1)
                                    newCost = solution.get_cost() - routeU.get_totalCost() - \
                                        routeV.get_totalCost() + \
                                        costRouteU[0] + costRouteV[0]
                                # melhora a solução:
                                if newCost < solution.get_cost():
                                    # print(costRouteU)
                                    #print("u e v:")
                                    # print(u)
                                    # print(v)
                                    # remove u e x
                                    U = routeU.popCustomer(i)
                                    X = routeU.popCustomer(i)
                                    # os insere após v
                                    if type.upper() == "M2":
                                        routeV.insertCustomer(U, indJ+1)
                                        routeV.insertCustomer(X, indJ+2)
                                    else:
                                        routeV.insertCustomer(X, indJ+1)
                                        routeV.insertCustomer(U, indJ+2)
                                    # atualizar custos das rotas
                                    routeU.set_cost(
                                        costRouteU[1], costRouteU[2], costRouteU[3])
                                    routeV.set_cost(
                                        costRouteV[1], costRouteV[2], costRouteV[3])
                                    # atualizar giantTour
                                    solution1.formGiantTour()
                                    solution1.calculateCost()
                                    return solution1

                        # caso v seja o depósito
                        newCost = math.inf
                        auxRouteU = copy.deepcopy(routeU)
                        if type.upper() == "M2":
                            # print(auxRouteU)
                            if u in routeV.get_tour():  # se pertencem a mesma rota:
                                auxRouteU.popCustomer(i)
                                auxRouteU.popCustomer(i)
                                auxRouteU.set_cost(
                                    costRouteU[1], costRouteU[2], costRouteU[3])
                                costRouteV = auxRouteU.costWith2Nodes(
                                    u, routeU.get_tour()[i+1], 0)
                                newCost = solution.get_cost() - routeU.get_totalCost() + \
                                    costRouteV[0]
                                del auxRouteU
                            else:
                                costRouteV = routeV.costWith2Nodes(
                                    u, routeU.get_tour()[i+1], 0)
                                newCost = solution.get_cost() - routeU.get_totalCost() - \
                                    routeV.get_totalCost() + \
                                    costRouteU[0] + costRouteV[0]
                        else:
                            if u in routeV.get_tour():  # se pertencem a mesma rota:
                                auxRouteU.popCustomer(i)
                                auxRouteU.popCustomer(i)
                                auxRouteU.set_cost(
                                    costRouteU[1], costRouteU[2], costRouteU[3])
                                costRouteV = auxRouteU.costWith2Nodes(
                                    routeU.get_tour()[i+1], u, 0)
                                newCost = solution.get_cost() - routeU.get_totalCost() + \
                                    costRouteV[0]
                                del auxRouteU
                            else:
                                costRouteV = routeV.costWith2Nodes(
                                    routeU.get_tour()[i+1], u, 0)
                                newCost = solution.get_cost() - routeU.get_totalCost() - \
                                    routeV.get_totalCost() + \
                                    costRouteU[0] + costRouteV[0]
                        # melhora a solução:
                        if newCost < solution.get_cost():
                            #print("u e v depósito:")
                            # print(u)

                            # remove u e x
                            U = routeU.popCustomer(i)
                            X = routeU.popCustomer(i)
                            # os insere após v
                            if type.upper() == "M2":
                                routeV.insertCustomer(U, 0)
                                routeV.insertCustomer(X, 1)
                            else:
                                routeV.insertCustomer(X, 0)
                                routeV.insertCustomer(U, 1)
                            # atualizar custos das rotas
                            routeU.set_cost(
                                costRouteU[1], costRouteU[2], costRouteU[3])
                            routeV.set_cost(
                                costRouteV[1], costRouteV[2], costRouteV[3])
                            # atualizar giantTour
                            solution1.formGiantTour()
                            solution1.calculateCost()

                            return solution1

        return solution

    '''
    Método aplica a regra: Se u e v forem clientes, troque u e v
    '''

    def M4(self, solution):
        return self.M4orM5orM6(solution, "M4")

    '''
    Método aplica a regra: Se u, x e v são clientes, troque (u,x) e v
    '''

    def M5(self, solution):
        return self.M4orM5orM6(solution, "M5")

    '''
    Método aplica a regra: Se u, x, v e y são clientes, troque (u,x) e (v,y)
    '''

    def M6(self, solution):
        return self.M4orM5orM6(solution, "M6")

    '''
    Método aplica a regra: type => M4 - Se u e v forem clientes, troque u e v
                           type => M5 - Se u, x e v são clientes, troque (u,x) e v
                           type => M6 - Se u, x, v e y são clientes, troque (u,x) e (v,y)
    '''

    def M4orM5orM6(self, solution, type):
        solution1 = copy.deepcopy(solution)
        costRouteU = None
        costRouteV = None
        for ru, routeU in enumerate(solution1.get_routes()):
            for i, u in enumerate(routeU.get_tour()):
                for routeV in solution1.get_routes():
                    for j, v in enumerate(routeV.get_tour()):
                        if u != v:
                            newCost = math.inf
                            # se eles são de rotas diferentes
                            if u not in routeV.get_tour():
                                # print("u e v rotas diferntes")
                                # print(u)
                                # print(v)
                                # verificar se há melhora na solução com o procedimento
                                if type.upper() == "M4":
                                    listIdOld = [i]
                                    listNew = [v]
                                    costRouteU = routeU.costShiftNodes(
                                        listIdOld, listNew, routeU)

                                    listIdOld = [j]
                                    listNew = [u]
                                    costRouteV = routeV.costShiftNodes(
                                        listIdOld, listNew, routeV)

                                    newCost = solution.get_cost() - routeU.get_totalCost() - \
                                        routeV.get_totalCost() + \
                                        costRouteU[0] + costRouteV[0]
                                elif type.upper() == "M5":
                                    if i+1 < len(routeU.get_tour()):
                                        listIdOld = [i, i+1]
                                        listNew = [v]
                                        costRouteU = routeU.costShiftNodes(
                                            listIdOld, listNew, routeU)

                                        listIdOld = [j]
                                        listNew = [u, routeU.get_tour()[i+1]]
                                        costRouteV = routeV.costShiftNodes(
                                            listIdOld, listNew, routeV)

                                        newCost = solution.get_cost() - routeU.get_totalCost() - \
                                            routeV.get_totalCost() + \
                                            costRouteU[0] + costRouteV[0]

                                elif type.upper() == "M6":
                                    if i+1 < len(routeU.get_tour()) and j+1 < len(routeV.get_tour()):
                                        # print("Não devia entrar aqui")
                                        listIdOld = [i, i+1]
                                        listNew = [v, routeV.get_tour()[j+1]]
                                        costRouteU = routeU.costShiftNodes(
                                            listIdOld, listNew, routeU)

                                        listIdOld = [j, j+1]
                                        listNew = [u, routeU.get_tour()[i+1]]
                                        costRouteV = routeV.costShiftNodes(
                                            listIdOld, listNew, routeV)

                                        newCost = solution.get_cost() - routeU.get_totalCost() - \
                                            routeV.get_totalCost() + \
                                            costRouteU[0] + costRouteV[0]
                                else:
                                    print("ERROR - método incorreto")
                                    exit(1)

                                # print(routeU)
                                # print(routeV)
                                # melhora a solução:
                                auxRouteU = copy.deepcopy(routeU)
                                auxRouteV = copy.deepcopy(routeV)
                                if newCost < solution.get_cost():
                                    if type.upper() == "M4":
                                        routeU.popCustomer(i)
                                        routeU.insertCustomer(v, i)
                                        routeV.popCustomer(j)
                                        routeV.insertCustomer(u, j)
                                        routeU.set_cost(
                                            costRouteU[1], costRouteU[2], costRouteU[3])
                                        routeV.set_cost(
                                            costRouteV[1], costRouteV[2], costRouteV[3])
                                    elif type.upper() == "M5":
                                        if i+1 < len(routeU.get_tour()):
                                            routeU.popCustomer(i)
                                            routeU.insertCustomer(v, i)
                                            routeU.popCustomer(i+1)
                                            routeV.popCustomer(j)
                                            routeV.insertCustomer(u, j)
                                            routeV.insertCustomer(
                                                auxRouteU.get_tour()[i+1], j+1)
                                            routeU.set_cost(
                                                costRouteU[1], costRouteU[2], costRouteU[3])
                                            routeV.set_cost(
                                                costRouteV[1], costRouteV[2], costRouteV[3])
                                    elif type.upper() == "M6":
                                        if i+1 < len(routeU.get_tour()) and j+1 < len(routeV.get_tour()):
                                            routeU.popCustomer(i)
                                            routeU.insertCustomer(v, i)
                                            routeU.popCustomer(i+1)
                                            routeU.insertCustomer(
                                                auxRouteV.get_tour()[j+1], i+1)
                                            routeV.popCustomer(j)
                                            routeV.insertCustomer(u, j)
                                            routeV.popCustomer(j+1)
                                            routeV.insertCustomer(
                                                auxRouteU.get_tour()[i+1], j+1)
                                            routeU.set_cost(
                                                costRouteU[1], costRouteU[2], costRouteU[3])
                                            routeV.set_cost(
                                                costRouteV[1], costRouteV[2], costRouteV[3])
                                        # print(routeU)
                                        # print(routeV)
                                    # atualizar custos

                                    # atualizar giantTour
                                    solution1.formGiantTour()
                                    solution1.calculateCost()
                                    # tour = solution1.get_giantTour()
                                    # for ii, c1 in enumerate(tour):
                                    #     for jj, c2 in enumerate(tour):
                                    #         if ii != jj and c1 == c2:
                                    #             # print(i)
                                    #             # print(j)
                                    #             print("Elementos iguais")
                                    #             print("sa")
                                    #             print(solution)
                                    #             print(solution.get_routes())
                                    #             print("solution1")
                                    #             print(solution1)
                                    #             print(solution1.get_routes())
                                    #             print(routeU)
                                    #             print(routeV)
                                    #             print(auxRouteU)
                                    #             print(auxRouteV)
                                    #             print(u)
                                    #             print(v)
                                    #             exit(1)
                                    # del auxRouteU
                                    # del auxRouteV
                                    return solution1

                            else:
                                # print("mesma rota")
                                # print(i)
                                # print(j)
                                if type.upper() == "M4":
                                    aux1 = [i]
                                    aux2 = [j]
                                    costRouteU = routeU.costShiftNodesSameRoute(
                                        aux1, aux2, routeU)
                                    newCost = solution1.get_cost() - routeU.get_totalCost() + \
                                        costRouteU[0]
                                # print(routeU.get_tour()[aux1[0]])
                                # print(aux2)
                                elif type.upper() == "M5":
                                    if i+1 < len(routeU.get_tour()) and routeU.get_tour()[i+1] != v:

                                        aux1 = [i, i+1]
                                        aux2 = [j]
                                        costRouteU = routeU.costShiftNodesSameRoute(
                                            aux1, aux2, routeU)
                                        newCost = solution1.get_cost() - routeU.get_totalCost() + \
                                            costRouteU[0]
                                elif type.upper() == "M6":
                                    maximum = max(i, j)
                                    minor = min(i, j)
                                    if maximum+1 < len(routeU.get_tour()) and minor+1 < maximum:
                                        # print("problema aqui")
                                        aux1 = [i, i+1]
                                        aux2 = [j, j+1]
                                        costRouteU = routeU.costShiftNodesSameRoute(
                                            aux1, aux2, routeU)
                                        newCost = solution1.get_cost() - routeU.get_totalCost() + \
                                            costRouteU[0]

                                # print(costRouteU)
                                # print(newCost)
                                # print(solution.get_cost())
                                # melhora a solução:
                                if newCost < solution1.get_cost():
                                    solution1.setRoute(costRouteU[1], ru)
                                    # print(routeU)
                                    # print(solution1)
                                    # atualizar giantTour
                                    solution1.formGiantTour()
                                    solution1.calculateCost()
                                    return solution1

        return solution

    '''
    Método aplica a regra: Se T(u) == T(v), substitua (u,x) e (v,y) por (u,v) e (x,y)
    '''

    def M7(self, solution):
        solution1 = copy.deepcopy(solution)
        for ru, routeU in enumerate(solution1.get_routes()):
            for i, u in enumerate(routeU.get_tour()):
                for routeV in solution1.get_routes():
                    for j, v in enumerate(routeV.get_tour()):
                        if u is not v:
                            # se eles são da mesma rota
                            if (u in routeV.get_tour()) and (v in routeU.get_tour()):
                                def minor(x, y): return x if x < y else y
                                def maximum(x, y): return x if x > y else y
                                max = maximum(i, j)
                                min = minor(i, j)
                                if max+1 < len(routeU.get_tour()) and min+1 < max:
                                    aux1 = [i, i+1]
                                    replaceWith1 = [u, v]
                                    # print("aux1")
                                    # print(aux1)
                                    # print("replaceWith1")
                                    # print(replaceWith1)
                                    aux2 = [j, j+1]
                                    replaceWith2 = [
                                        routeU.get_tour()[i+1], routeU.get_tour()[j+1]]
                                    # print("aux2")
                                    # print(aux2)
                                    # print("replaceWith2")
                                    # print(replaceWith2)
                                    costRouteU = routeU.costReplaceNodes(
                                        routeU, aux1, replaceWith1, aux2, replaceWith2)
                                    newCost = solution.get_cost() - routeU.get_totalCost() + \
                                        costRouteU[0]
                                    # print(costRouteU)
                                    # melhora a solução:
                                    if newCost < solution.get_cost():
                                        solution1.setRoute(costRouteU[1], ru)
                                        # atualizar giantTour
                                        solution1.formGiantTour()
                                        solution1.calculateCost()
                                        return solution1

        return solution

    '''
    Método aplica a regra: Se T(u) != T(v), substitua (u,x) e (v,y) por (u,v) e (x,y)
    '''

    def M8(self, solution):
        return self.M8orM9(solution, "M8")

    '''
    Método aplica a regra: Se T(u) != T(v), substitua (u,x) e (v,y) por (u,y) e (x,v)
    '''

    def M9(self, solution):
        return self.M8orM9(solution, "M9")

    '''
    Método aplica a regra: type => M8 - Se T(u) != T(v), substitua (u,x) e (v,y) por (u,v) e (x,y)
                           type => M9 - Se T(u) != T(v), substitua (u,x) e (v,y) por (u,y) e (x,v)
    '''

    def M8orM9(self, solution, type):
        solution1 = copy.deepcopy(solution)
        size = len(solution1.get_routes())
        for ru in range(size-1):
            routeU = solution1.get_routes()[ru]
            for i, u in enumerate(routeU.get_tour()):
                for rv in range(ru+1,size):
                    routeV = solution1.get_routes()[rv]
                    for j, v in enumerate(routeV.get_tour()):
                        if i+1 < len(routeU.get_tour()) and j+1 < len(routeV.get_tour()):
                            if type.upper() == "M8":
                                aux1 = [i, i+1]
                                replaceWith1 = [u, v]
                                aux2 = [j, j+1]
                                replaceWith2 = [
                                    routeU.get_tour()[i+1], routeV.get_tour()[j+1]]
                            elif type.upper() == "M9":
                                aux1 = [i, i+1]
                                replaceWith1 = [
                                    u, routeV.get_tour()[j+1]]
                                aux2 = [j, j+1]
                                replaceWith2 = [
                                    routeU.get_tour()[i+1], v]
                            else:
                                print("ERROR - método incorreto")
                                exit(1)

                            # mudança na rota U
                            costRouteU = routeU.costReplaceNodes(
                                routeU, aux1, replaceWith1)
                            # print("aux1")
                            # print(aux1)
                            # print("replaceWith1")
                            # print(replaceWith1)
                            # mudança na rota V
                            costRouteV = routeV.costReplaceNodes(
                                routeV, aux2, replaceWith2)
                            # print("aux2")
                            # print(aux2)
                            # print("replaceWith2")
                            # print(replaceWith2)

                            newCost = solution.get_cost() - routeU.get_totalCost() - \
                                routeV.get_totalCost() + \
                                costRouteU[0] + costRouteV[0]

                            if newCost < solution.get_cost():
                                solution1.setRoute(costRouteU[1], ru)
                                solution1.setRoute(costRouteV[1], rv)
                                # atualizar giantTour
                                solution1.formGiantTour()
                                solution1.calculateCost()
                                return solution1

        return solution

    '''
    Rotation 
    Bolaños 2018
    '''

    def M10(self, solution):
        solution1 = copy.deepcopy(solution)
        depots = dpts.get_depotsList()
        #escolha da rota
        routes = solution1.get_routes()
        idRoute = np.random.randint(len(routes))
        route = copy.deepcopy(routes[idRoute])
        length = len(route.get_tour()) # comprimento da rota
        oldDepot = route.get_depot()
        costWithoutRoute = solution1.get_cost() - route.get_totalCost()
        penalty = route.get_totalCost() - route.get_costWithoutPenalty()
        extraPenalty = 0
        # print(penalty)
        cont = 0

        bestRoute = copy.deepcopy(route)
        # print("tamanho de rotas")
        # print(len(routes))
        # print("route")
        # print(route)
        if length>0:
            route1 = copy.deepcopy(route)
            #rotação da rota
            for i in range(length):
                #rotacionar
                # print(route1)
                aux = route1.get_tour()[0]
                # print(aux)
                cost = route1.costWithoutNode(0)
                route1.removeCustomer(aux)
                route1.set_cost(cost[1], cost[2], cost[3])
                cost = route1.costWithNode(aux, length-1)
                route1.addCustomer(aux)
                route1.set_cost(cost[1], cost[2], cost[3])
                # print(route1)
                # print("-----")
                # verificar se rota gerada é melhor (considerando mesmo depósito)
                if bestRoute.get_totalCost() > route1.get_totalCost():
                    extraPenalty = 0
                    bestRoute = copy.deepcopy(route1)
                    cont = 1
                # verificar transferência da rota em outro depósito 
                for dpt in depots.values():
                    if str(dpt) != str(oldDepot):
                        # verificar rota para o novo depósito
                        tour = route1.get_tour()
                        # tirar o custo associado ao depósito
                        cost1 = route1.get_totalCost() - dist.euclidianDistance(tour[0].get_x_coord(),
                                tour[0].get_y_coord(), oldDepot.get_x_coord(), oldDepot.get_y_coord()) - \
                                dist.euclidianDistance(tour[length-1].get_x_coord(),
                                tour[length-1].get_y_coord(), oldDepot.get_x_coord(), oldDepot.get_y_coord())

                        # computar custo com o novo depósito
                        newCost = cost1 + dist.euclidianDistance(tour[0].get_x_coord(),
                            tour[0].get_y_coord(), dpt.get_x_coord(), dpt.get_y_coord()) + \
                            dist.euclidianDistance(tour[length-1].get_x_coord(),
                            tour[length-1].get_y_coord(), dpt.get_x_coord(), dpt.get_y_coord())
                        
                        if bestRoute.get_totalCost() > newCost:
                            # verifica número de veículos utilizados pelo depósito
                            nVehicles = 0
                            for r in solution1.get_routes():
                                if r.get_depot() == dpt:
                                    nVehicles += 1
                            if nVehicles < dpt.get_numberVehicles():
                                if (costWithoutRoute + newCost) < solution1.get_cost(): # é melhor
                                    extraPenalty = 0
                                    bestRoute = copy.deepcopy(route1)
                                    bestRoute.set_depot(dpt)
                                    newCost1 = newCost - penalty
                                    bestRoute.set_cost(newCost1, bestRoute.get_totalDemand(),
                                        bestRoute.get_totalService())

                                    cont = 1
                            # else:
                            #     if (costWithoutRoute + newCost + 1000) < solution1.get_cost(): # ainda é melhor
                            #         extraPenalty = 1000 #penalização por rota a mais
                            #         bestRoute.set_depot(dpt)
                            #         newCost1 = newCost - penalty
                            #         bestRoute.set_cost(newCost1, bestRoute.get_totalDemand(),
                            #             bestRoute.get_totalService())
                            #         cont = 1
                    
                 
            if cont == 1:
                # print(penalty)
                # # print(bestRoute.get_totalCost()) 
                # print(route)
                # # print("best")
                # print(bestRoute)
                solution1.setRoute(bestRoute, idRoute)
                solution1.formGiantTour()
                solution1.calculateCost(extraPenalty)
                return solution1
        
        return solution
