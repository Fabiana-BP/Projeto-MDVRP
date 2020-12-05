'''
Arquivo responsável pela representação e estruturação da solução
'''
from customers import Customers


class Solution:
    _giantTour = None
    _routes = None
    _cost = float()
    _depots = None
    _ranking = float()

    def __init__(self):
        self._giantTour = []  # lista de clientes, cada item um Customer
        self._routes = []  # lista de Route

        # self._idRoutes = []  # indicativo da rota

        self._cost = 0
        self._depots = []  # lista de depósitos, cada item o Depot de cada cliente
        self._infeasible = False

    def set_ranking(self,ranking):
        self._ranking = ranking
    
    def get_ranking(self):
        return self._ranking

    '''
    Método adiciona uma rota em uma lista
    '''

    def addRoutes(self, route):
        if route.is_infeasible():
            self._infeasible = True
        self._routes.append(route)

    '''
    Método atualiza uma rota
    '''
    def setRoute(self, route, idRoute):
        self._routes[idRoute] = route

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
        for r in self._routes:
            self._giantTour = self._giantTour + r.get_tour()
            for i in range(len(r.get_tour())):
                self._depots.append(r.get_depot())
            

    '''
    Método adiciona clientes no giantTour e o depósito correspondente
    '''

    def addGiantTour(self, customer, depot):
        self._giantTour.append(customer)
        self._depots.append(depot)


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

        return "ranking: " + str(self._ranking)+ " \ngiantTour: " + str(self._giantTour) + "\n" + "depósitos: " + str(self._depots) + "\ncusto: " + str(self._cost) + " - " + aux

    def __repr__(self):
        aux = ""
        if self._infeasible:
            aux = "inviável"

        return "ranking: " + str(self._ranking)+" \ngiantTour: " + str(self._giantTour) + "\n" + "depósitos: " + str(self._depots) + "\ncusto: " + str(self._cost) + " - " + aux + "\n"
