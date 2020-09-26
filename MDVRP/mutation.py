from distances import Distances as dist
import copy

'''
Pesquisa local como operador de mutação
Prins2004
'''
class Mutation:
    '''
    Cada iteração varre todos os pares possíveis de nós distintos (u,v). Esses nós podem pertencer à mesma viagem ou a viagens diferentes
    e um deles pode ser o depósito. x e y são os sucessores de u e v em suas respectivas viagens.
    '''
    def mutation(solution):
        movimentation = [Mutation.M1, Mutation.M2, Mutation.M3, Mutation.M4, Mutation.M5, Mutation.M6, Mutation.M7, Mutation.M8, Mutation.M9]
        bestSolution = copy.deepcopy(solution)
        #print(bestSolution)
        for i,m in enumerate(movimentation):
            solution1 = m(bestSolution)
            # print(solution1)
            # if i>6:
            #
            #     print(solution1.get_routes())

            if solution1.get_cost() < bestSolution.get_cost():
                bestSolution = copy.deepcopy(solution1)
            else:
                #excluir rotas vazias
                bestSolution.removeRoutesEmpty()
                return bestSolution

        #excluir rotas vazias
        bestSolution.removeRoutesEmpty()
        return bestSolution

    '''
    Método aplica a regra: Se u for um nó cliente, remova u e insira-o após v
    '''
    def M1(solution):
        solution1 = copy.deepcopy(solution)
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

    '''
    Método aplica a regra: Se u e x forem clientes, remova-os e insira (u,x) após v
    '''
    def M2(solution):
        return Mutation.M2orM3(solution,"M2")

    '''
    Método aplica a regra: Se u e x forem clientes, remova-os e insira (x,u) após v
    '''
    def M3(solution):
        return Mutation.M2orM3(solution,"M3")


    '''
    Método aplica a regra: type: M2 -> Se u e x forem clientes, remova-os e insira (u,x) após v
                           type: M3 -> Se u e x forem clientes, remova-os e insira (x,u) após v
    '''
    def M2orM3(solution,type):
        solution1 = copy.deepcopy(solution)
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
                                    if type.upper() == "M2":
                                        costRouteV = auxRouteU.costWith2Nodes(u,routeU.get_tour()[i+1],indJ+1)
                                    elif type.upper() == "M3":
                                        costRouteV = auxRouteU.costWith2Nodes(routeU.get_tour()[i+1],u,indJ+1)
                                    else:
                                        print("ERROR - método incorreto")
                                        exit(1)
                                    newCost = solution.get_cost() - routeU.get_totalCost() + costRouteV[0]
                                else:
                                    if type.upper() == "M2":
                                        costRouteV = routeV.costWith2Nodes(u,routeU.get_tour()[i+1],indJ+1)
                                    elif type.upper() == "M3":
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
                                    if type.upper() == "M2":
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
                        if type.upper() == "M2":
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
                            if type.upper() == "M2":
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
        return Mutation.M4orM5orM6(solution,"M4")


    '''
    Método aplica a regra: Se u, x e v são clientes, troque (u,x) e v
    '''
    def M5(solution):
        return Mutation.M4orM5orM6(solution,"M5")


    '''
    Método aplica a regra: Se u, x, v e y são clientes, troque (u,x) e (v,y)
    '''
    def M6(solution):
        return Mutation.M4orM5orM6(solution,"M6")


    '''
    Método aplica a regra: type => M4 - Se u e v forem clientes, troque u e v
                           type => M5 - Se u, x e v são clientes, troque (u,x) e v
                           type => M6 - Se u, x, v e y são clientes, troque (u,x) e (v,y)
    '''
    def M4orM5orM6(solution,type):
        solution1 = copy.deepcopy(solution)
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
                                if type.upper() == "M4":
                                    listIdOld = [i]
                                    listNew = [v]
                                elif type.upper() == "M5":
                                    if i+1 < len(routeU.get_tour()):
                                        listIdOld = [i,i+1]
                                        listNew = [v]
                                    else:
                                        break
                                elif type.upper() == "M6":
                                    if i+1 < len(routeU.get_tour()) and j+1 < len(routeV.get_tour()):
                                        listIdOld = [i,i+1]
                                        listNew = [v,routeV.get_tour()[j+1]]
                                    else:
                                        break
                                else:
                                    print("ERROR - método incorreto")
                                    exit(1)

                                costRouteU = routeU.costShiftNodes(listIdOld,listNew,routeU)
                                listIdOld = [j]
                                listNew = [u]
                                if type.upper() == "M5":
                                    listIdOld = [j]
                                    listNew = [u,routeU.get_tour()[i+1]]
                                if type.upper() == "M6":
                                    listIdOld = [j,j+1]
                                    listNew = [u,routeU.get_tour()[i+1]]
                                    # print(routeV.get_tour()[listIdOld[0]])
                                    # print(listNew)
                                costRouteV = routeV.costShiftNodes(listIdOld,listNew,routeV)
                                newCost = solution.get_cost() - routeU.get_totalCost() - routeV.get_totalCost() + costRouteU[0] + costRouteV[0]
                                # print(routeU)
                                # print(routeV)
                                #melhora a solução:
                                auxRouteU = copy.deepcopy(routeU)
                                auxRouteV = copy.deepcopy(routeV)
                                if newCost < solution.get_cost():
                                    if type.upper() == "M4":
                                        routeU.popCustomer(i)
                                        routeU.insertCustomer(v,i)
                                        routeV.popCustomer(j)
                                        routeV.insertCustomer(u,j)
                                    elif type.upper() == "M5":
                                        routeU.popCustomer(i)
                                        routeU.insertCustomer(v,i)
                                        routeU.popCustomer(i+1)
                                        routeV.popCustomer(j)
                                        routeV.insertCustomer(u,j)
                                        routeV.insertCustomer(auxRouteU.get_tour()[i+1],j)
                                    elif type.upper() == "M6":
                                        routeU.popCustomer(i)
                                        routeU.insertCustomer(v,i)
                                        routeU.popCustomer(i+1)
                                        routeU.insertCustomer(auxRouteV.get_tour()[j+1],i+1)
                                        routeV.popCustomer(j)
                                        routeV.insertCustomer(u,j)
                                        routeV.popCustomer(j+1)
                                        routeV.insertCustomer(auxRouteU.get_tour()[i+1],j+1)
                                        # print(routeU)
                                        # print(routeV)
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
                                aux1 = [i]
                                aux2 = [j]
                                #print(routeU.get_tour()[aux1[0]])
                                #print(aux2)
                                if type.upper() == "M5":
                                    if i+1 < len(routeU.get_tour()):
                                        aux1 = [i,i+1]
                                        aux2 = [j]
                                    else:
                                        break
                                if type.upper() == "M6":
                                    if i+1 < len(routeU.get_tour()) and j+1 < len(routeU.get_tour()):
                                        aux1 = [i,i+1]
                                        aux2 = [j,j+1]
                                    else:
                                        break
                                costRouteU = routeU.costShiftNodesSameRoute(aux1,aux2,routeU)
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


    '''
    Método aplica a regra: Se T(u) == T(v), substitua (u,x) e (v,y) por (u,v) e (x,y)
    '''
    def M7(solution):
        solution1 = copy.deepcopy(solution)
        for ru,routeU in enumerate(solution1.get_routes()):
            for i,u in enumerate(routeU.get_tour()):
                for routeV in solution1.get_routes():
                    for j,v in enumerate(routeV.get_tour()):
                        if u is not v:
                            if (u in routeV.get_tour()) and (v in routeU.get_tour()): #se eles são da mesma rota
                                minor = lambda x,y:x if x<y else y
                                maximum = lambda x,y:x if x>y else y
                                max = maximum(i,j)
                                min = minor(i,j)
                                if max+1 < len(routeU.get_tour()) and min+1 < max:
                                    aux1 = [i,i+1]
                                    replaceWith1 = [u,v]
                                    # print("aux1")
                                    # print(aux1)
                                    # print("replaceWith1")
                                    # print(replaceWith1)
                                    aux2 = [j,j+1]
                                    replaceWith2 = [routeU.get_tour()[i+1],routeU.get_tour()[j+1]]
                                    # print("aux2")
                                    # print(aux2)
                                    # print("replaceWith2")
                                    # print(replaceWith2)
                                    costRouteU = routeU.costReplaceNodes(routeU,aux1,replaceWith1,aux2,replaceWith2)
                                    newCost = solution.get_cost() - routeU.get_totalCost() + costRouteU[0]
                                    # print(costRouteU)
                                    #melhora a solução:
                                    if newCost < solution.get_cost():
                                        solution1.get_routes()[ru]  = None
                                        solution1.get_routes()[ru] = costRouteU[1]
                                        #atualizar giantTour
                                        solution1.formGiantTour()
                                        solution1.calculateCost()
                                        return solution1

        return solution

    '''
    Método aplica a regra: Se T(u) != T(v), substitua (u,x) e (v,y) por (u,v) e (x,y)
    '''
    def M8(solution):
        return Mutation.M8orM9(solution,"M8")


    '''
    Método aplica a regra: Se T(u) != T(v), substitua (u,x) e (v,y) por (u,y) e (x,v)
    '''
    def M9(solution):
        return Mutation.M8orM9(solution,"M9")


    '''
    Método aplica a regra: type => M8 - Se T(u) != T(v), substitua (u,x) e (v,y) por (u,v) e (x,y)
                           type => M9 - Se T(u) != T(v), substitua (u,x) e (v,y) por (u,y) e (x,v)
    '''
    def M8orM9(solution,type):
        solution1 = copy.deepcopy(solution)
        for ru,routeU in enumerate(solution1.get_routes()):
            for i,u in enumerate(routeU.get_tour()):
                for rv,routeV in enumerate(solution1.get_routes()):
                    for j,v in enumerate(routeV.get_tour()):
                        if u is not v:
                            if (u not in routeV.get_tour()) and (v not in routeU.get_tour()): #se eles não são da mesma rota
                                if i+1 < len(routeU.get_tour()) and j+1 < len(routeV.get_tour()):
                                    if type.upper() == "M8":
                                        aux1 = [i,i+1]
                                        replaceWith1 = [u,v]
                                        aux2 = [j,j+1]
                                        replaceWith2 = [routeU.get_tour()[i+1],routeV.get_tour()[j+1]]
                                    elif type.upper() == "M9":
                                        aux1 = [i,i+1]
                                        replaceWith1 = [u,routeV.get_tour()[j+1]]
                                        aux2 = [j,j+1]
                                        replaceWith2 = [routeU.get_tour()[i+1],v]
                                    else:
                                        print("ERROR - método incorreto")
                                        exit(1)


                                    #mudança na rota U
                                    costRouteU = routeU.costReplaceNodes(routeU,aux1,replaceWith1)
                                    # print("aux1")
                                    # print(aux1)
                                    # print("replaceWith1")
                                    # print(replaceWith1)
                                    #mudança na rota V
                                    costRouteV = routeV.costReplaceNodes(routeV,aux2,replaceWith2)
                                    # print("aux2")
                                    # print(aux2)
                                    # print("replaceWith2")
                                    # print(replaceWith2)

                                    newCost = solution.get_cost() - routeU.get_totalCost() - routeV.get_totalCost() + costRouteU[0] + costRouteV[0]

                                    if newCost < solution.get_cost():
                                        solution1.get_routes()[ru]  = None
                                        solution1.get_routes()[ru] = costRouteU[1]
                                        solution1.get_routes()[rv]  = None
                                        solution1.get_routes()[rv] = costRouteV[1]
                                        #atualizar giantTour
                                        solution1.formGiantTour()
                                        solution1.calculateCost()
                                        return solution1

        return solution
