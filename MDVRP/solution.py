'''
Arquivo responsável pela representação e estruturação da solução
'''
from customers import Customers


class Solution:
    _giantTour = None
    _routes = None
    _cost = float()
    _depots = None

    def __init__(self):
        self._giantTour = []  # lista de clientes, cada item um Customer
        self._routes = []  # lista de Route

        self._idRoutes = []  # indicativo da rota

        self._cost = 0
        self._depots = []  # lista de depósitos, cada item o Depot de cada cliente
        self._infeasible = False

    def set_solution(self, giantTour, routes, idRoutes, depots, cost, infeasible=None):
        self._giantTour = giantTour
        self._routes = routes
        self._idRoutes = idRoutes
        self._cost = cost
        self._depots = depots
        if infeasible != None:
            self._infeasible = infeasible

    '''
    Método adiciona uma rota em uma lista
    '''

    def addRoutes(self, route):
        if route.is_infeasible():
            self._infeasible = True
        self._routes.append(route)

    '''
    Método remove uma rota
    '''

    def removeRoutesEmpty(self):
        self._routes = list(filter(lambda x: [] != x.get_tour(), self._routes))
        # print(self._routes)

    '''
    Método concatena as rotas em uma única lista (giantTour)
    '''

    def formGiantTour(self):
        self._giantTour = []
        self._depots = []
        ir = 0
        for r in self._routes:
            self._giantTour = self._giantTour + r.get_tour()
            for i in range(len(r.get_tour())):
                self._depots.append(r.get_depot())
                self._idRoutes.append(ir)
            ir += 1

    '''
    Método adiciona clientes no giantTour e o depósito correspondente
    '''

    def addGiantTour(self, customer, depot):
        self._giantTour.append(customer)
        self._depots.append(depot)

    '''
    Método calcula diversidade do indivíduo

    def diversity(self,nClose,population,individual):
        div = 0.0
        i=0;
        for t in self._giantTour:
            cst = Customers.get_customersList()[str(t)]
            depotCst = str(self._depots[i])
            #recuperando os nClose vizinhos mais próximos
            j = 0
            dist = 0.0
            for neighbor in cst.get_neighborsDistances():
                if j < nClose:
                    depotNbr = self._depots[self._giantTour.index(str(neighbor[0]))]
                    if depotCst != str(depotNbr):
                        dist += 1

                j += 1
            dist = dist / (2.0*nClose)
            div += dist
            i += 1

        div = div/float(len(self._giantTour))
        return div
    '''

    '''
    Método calcula o custo total da solução
    '''

    def calculateCost(self,extraPenalty = 0):
        self._cost = 0.0
        for r in self._routes:
            self._cost += r.get_totalCost()
        #penalidade por excesso de rotas
        if extraPenalty > 0:
            self._cost += extraPenalty
            self._infeasible = True

        #self._cost += self.diversity(10)
        # print(self._cost)

    '''
    Método retorna rotas
    '''

    def get_routes(self):
        return self._routes

    def get_idRoutes(self):
        return self._idRoutes

    def get_giantTour(self):
        return self._giantTour

    def get_depots(self):
        return self._depots

    def get_cost(self):
        return self._cost

    def __str__(self):
        aux = ""
        if self._infeasible:
            aux = "inviável"

        return "giantTour: " + str(self._giantTour) + "\n" + "depósitos: " + str(self._depots) + "\ncusto: " + str(self._cost) + " - " + aux

    def __repr__(self):
        aux = ""
        if self._infeasible:
            aux = "inviável"

        return "giantTour: " + str(self._giantTour) + "\n" + "depósitos: " + str(self._depots) + "\ncusto: " + str(self._cost) + " - " + aux + "\n"
