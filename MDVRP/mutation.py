from distances import Distances as dist
import copy

class Mutation:

    def mutation(solution):
        movimentation = [Mutation.M1,Mutation.M2,Mutation.M3,Mutation.M4]
        bestSolution = copy.deepcopy(solution)
        print(bestSolution)
        for i,m in enumerate(movimentation):
            solution1 = m(bestSolution)
            print(solution1)
            # if i>2:
            #
            #     print(solution1.get_routes())

            if solution1.get_cost() < bestSolution.get_cost():
                bestSolution = copy.deepcopy(solution1)
            else:
                return bestSolution

        return bestSolution

    '''
    Método aplica a regra: Se u for um nó cliente, remova u e insira-o após v
    '''
    def M1(solution):
        solution1 = copy.deepcopy(solution)
        customers = solution1.get_giantTour()
        routes = solution1.get_routes()
        for routeU in solution1.get_routes():
            for i,u in enumerate(routeU.get_tour()):
                #verificar se há melhora na solução com o procedimento
                costRouteU = routeU.costWithoutNode(i)

                for routeV in solution1.get_routes():
                    for j,v in enumerate(routeV.get_tour()):
                        if u is not v: #se eles são diferentes
                            indJ = j
                            if routeV is routeU: #pertencem a mesma rota
                                auxRouteU = copy.deepcopy(routeU)
                                auxRouteU.popCustomer(i)
                                auxRouteU.set_cost(costRouteU[1],costRouteU[2],costRouteU[3])
                                if j>i:
                                    indJ = j - 1
                                costRouteV = auxRouteU.costWithNode(u,indJ+1)
                                newCost = solution.get_cost() - routeU.get_totalCost() + costRouteV[0]
                            else:
                                costRouteV = routeV.costWithNode(u,indJ+1)
                                newCost = solution.get_cost() - routeU.get_totalCost() - routeV.get_totalCost() + costRouteU[0] + costRouteV[0]

                            #melhora a solução:
                            if newCost < solution.get_cost():
                                #remove u
                                U = routeU.popCustomer(i)
                                #insere u após v
                                routeV.insertCustomer(U,indJ+1)
                                #atualizar custos das rotas
                                routeU.set_cost(costRouteU[1],costRouteU[2],costRouteU[3])
                                routeV.set_cost(costRouteV[1],costRouteV[2],costRouteV[3])
                                #atualizar giantTour
                                solution1.formGiantTour()
                                solution1.calculateCost()
                                return solution1

                    #caso v seja o depósito
                    if routeV is routeU: #pertencem a mesma rota
                        auxRouteU = copy.deepcopy(routeU)
                        auxRouteU.popCustomer(i)
                        auxRouteU.set_cost(costRouteU[1],costRouteU[2],costRouteU[3])
                        costRouteV = auxRouteU.costWithNode(u,0)
                        newCost = solution.get_cost() - routeU.get_totalCost() + costRouteV[0]
                    else:
                        costRouteV = routeV.costWithNode(u,0)
                        newCost = solution.get_cost() - routeU.get_totalCost() - routeV.get_totalCost() + costRouteU[0] + costRouteV[0]
                    #melhora a solução:
                    if newCost < solution.get_cost():
                        #remove u
                        U = routeU.popCustomer(i)
                        #insere u após v
                        routeV.insertCustomer(U,0)
                        #atualizar custos das rotas
                        routeU.set_cost(costRouteU[1],costRouteU[2],costRouteU[3])
                        routeV.set_cost(costRouteV[1],costRouteV[2],costRouteV[3])
                        #atualizar giantTour
                        solution1.formGiantTour()
                        solution1.calculateCost()
                        return solution1

        return solution

    def M2(solution):
        return Mutation.M2orM3(solution,"M2")


    def M3(solution):
        return Mutation.M2orM3(solution,"M3")


    '''
    Método aplica a regra: type: M2 -> Se u e x forem clientes, remova-os e insira (u,x) após v
                           type: M3 -> Se u e x forem clientes, remova-os e insira (x,u) após v
    '''
    def M2orM3(solution,type):
        solution1 = copy.deepcopy(solution)
        customers = solution1.get_giantTour()
        routes = solution1.get_routes()
        for routeU in solution1.get_routes():
            for i,u in enumerate(routeU.get_tour()):
                #verificar se há melhora na solução com o procedimento
                if i+1 < len(routeU.get_tour()):
                    costRouteU = routeU.costWithout2Nodes(i)

                    auxRouteU = copy.deepcopy(routeU)
                    for routeV in solution1.get_routes():
                        for j,v in enumerate(routeV.get_tour()):
                            if u is not v and routeU.get_tour()[i+1] is not v: #se u e x são diferentes de v

                                indJ = j
                                if routeU is routeV: #se pertencem a mesma rota:
                                    if j>i:
                                        indJ = j - 2
                                    auxRouteU = copy.deepcopy(routeU)
                                    auxRouteU.popCustomer(i)
                                    auxRouteU.popCustomer(i)
                                    auxRouteU.set_cost(costRouteU[1],costRouteU[2],costRouteU[3])
                                    if type == "M2" or type =="m2":
                                        costRouteV = auxRouteU.costWith2Nodes(u,routeU.get_tour()[i+1],indJ+1)
                                    elif type == "M3" or type =="m3":
                                        costRouteV = auxRouteU.costWith2Nodes(routeU.get_tour()[i+1],u,indJ+1)
                                    else:
                                        print("ERROR - método incorreto")
                                        exit(1)
                                    newCost = solution.get_cost() - routeU.get_totalCost() + costRouteV[0]
                                else:
                                    if type == "M2" or type =="m2":
                                        costRouteV = routeV.costWith2Nodes(u,routeU.get_tour()[i+1],indJ+1)
                                    elif type == "M3" or type =="m3":
                                        costRouteV = routeV.costWith2Nodes(routeU.get_tour()[i+1],u,indJ+1)
                                    else:
                                        print("ERROR - método incorreto")
                                        exit(1)
                                    newCost = solution.get_cost() - routeU.get_totalCost() - routeV.get_totalCost() + costRouteU[0] + costRouteV[0]
                                #melhora a solução:
                                if newCost < solution.get_cost():
                                    #print(costRouteU)
                                    #print("u e v:")
                                    #print(u)
                                    #print(v)
                                    #remove u e x
                                    U = routeU.popCustomer(i)
                                    X = routeU.popCustomer(i)
                                    #os insere após v
                                    if type == "M2" or type =="m2":
                                        routeV.insertCustomer(U,indJ+1)
                                        routeV.insertCustomer(X,indJ+2)
                                    else:
                                        routeV.insertCustomer(X,indJ+1)
                                        routeV.insertCustomer(U,indJ+2)
                                    #atualizar custos das rotas
                                    routeU.set_cost(costRouteU[1],costRouteU[2],costRouteU[3])
                                    routeV.set_cost(costRouteV[1],costRouteV[2],costRouteV[3])
                                    #atualizar giantTour
                                    solution1.formGiantTour()
                                    solution1.calculateCost()
                                    return solution1

                        #caso v seja o depósito
                        if type == "M2" or type =="m2":
                            if routeU is routeV: #se pertencem a mesma rota:
                                auxRouteU = copy.deepcopy(routeU)
                                auxRouteU.popCustomer(i)
                                auxRouteU.popCustomer(i)
                                auxRouteU.set_cost(costRouteU[1],costRouteU[2],costRouteU[3])
                                costRouteV = auxRouteU.costWith2Nodes(u,routeU.get_tour()[i+1],0)
                                newCost = solution.get_cost() - routeU.get_totalCost() + costRouteV[0]
                            else:
                                costRouteV = routeV.costWith2Nodes(u,routeU.get_tour()[i+1],0)
                                newCost = solution.get_cost() - routeU.get_totalCost() - routeV.get_totalCost() + costRouteU[0] + costRouteV[0]
                        else:
                            if routeU is routeV: #se pertencem a mesma rota:
                                auxRouteU = copy.deepcopy(routeU)
                                auxRouteU.popCustomer(i)
                                auxRouteU.popCustomer(i)
                                auxRouteU.set_cost(costRouteU[1],costRouteU[2],costRouteU[3])
                                costRouteV = auxRouteU.costWith2Nodes(routeU.get_tour()[i+1],u,0)
                                newCost = solution.get_cost() - routeU.get_totalCost() + costRouteV[0]
                            else:
                                costRouteV = routeV.costWith2Nodes(routeU.get_tour()[i+1],u,0)
                                newCost = solution.get_cost() - routeU.get_totalCost() - routeV.get_totalCost() + costRouteU[0] + costRouteV[0]
                        #melhora a solução:
                        if newCost < solution.get_cost():
                            #print("u e v depósito:")
                            #print(u)

                            #remove u e x
                            U = routeU.popCustomer(i)
                            X = routeU.popCustomer(i)
                            #os insere após v
                            if type == "M2" or type =="m2":
                                routeV.insertCustomer(U,0)
                                routeV.insertCustomer(X,1)
                            else:
                                routeV.insertCustomer(X,0)
                                routeV.insertCustomer(U,1)
                            #atualizar custos das rotas
                            routeU.set_cost(costRouteU[1],costRouteU[2],costRouteU[3])
                            routeV.set_cost(costRouteV[1],costRouteV[2],costRouteV[3])
                            #atualizar giantTour
                            solution1.formGiantTour()
                            solution1.calculateCost()
                            return solution1

        return solution

    '''
    Método aplica a regra: Se u e v forem clientes, troque u e v
    '''
    def M4(solution):
        solution1 = copy.deepcopy(solution)
        customers = solution1.get_giantTour()
        routes = solution1.get_routes()
        for ru,routeU in enumerate(solution1.get_routes()):
            for i,u in enumerate(routeU.get_tour()):
                for routeV in solution1.get_routes():
                    for j,v in enumerate(routeV.get_tour()):
                        if u is not v:

                            if (u not in routeV.get_tour()) and (v not in routeU.get_tour()): #se eles são de rotas diferentes
                                # print("u e v rotas diferntes")
                                # print(u)
                                # print(v)
                                #verificar se há melhora na solução com o procedimento
                                listIdOld = [i]
                                listNew = [v]
                                costRouteU = routeU.costShiftNodes(listIdOld,listNew,routeU)
                                listIdOld = [j]
                                listNew = [u]
                                costRouteV = routeV.costShiftNodes(listIdOld,listNew,routeV)
                                #print(costRouteU)
                                #print(costRouteV)
                                newCost = solution.get_cost() - routeU.get_totalCost() - routeV.get_totalCost() + costRouteU[0] + costRouteV[0]
                                #melhora a solução:
                                if newCost < solution.get_cost():
                                    routeU.popCustomer(i)
                                    routeU.insertCustomer(v,i)
                                    routeV.popCustomer(j)
                                    routeV.insertCustomer(u,j)
                                    #atualizar custos
                                    routeU.set_cost(costRouteU[1],costRouteU[2],costRouteU[3])
                                    routeV.set_cost(costRouteV[1],costRouteV[2],costRouteV[3])
                                    #atualizar giantTour
                                    solution1.formGiantTour()
                                    solution1.calculateCost()
                                    return solution1

                            else:
                                # print("mesma rota")
                                # print(i)
                                # print(j)
                                costRouteU = routeU.costShiftNodesSameRoute([i],[j],routeU)
                                newCost = solution.get_cost() - routeU.get_totalCost() + costRouteU[0]
                                # print(costRouteU)
                                # print(newCost)
                                # print(solution.get_cost())
                                #melhora a solução:
                                if newCost < solution.get_cost():
                                    solution1.get_routes()[ru]  = None
                                    solution1.get_routes()[ru] = costRouteU[1]
                                    # print(routeU)
                                    # print(solution1)
                                    #atualizar giantTour
                                    solution1.formGiantTour()
                                    solution1.calculateCost()
                                    return solution1

        return solution
