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
        self._giantTour = [] #lista de strings, cada item um cliente
        self._routes = [] #lista de Route
        self._cost = 0
        self._depots = [] #lista de strings, cada item o depósito de cada cliente


    '''
    Método adiciona uma rota em uma lista
    '''
    def addRoutes(self,route):
        self._routes.append(route)


    '''
    Método concatena as rotas em uma única lista (giantTour)
    '''
    def formGiantTour(self):
        for r in self._routes:
            self._giantTour = self._giantTour + r.get_tour()
            for i in range(len(r.get_tour())):
                self._depots.append(r.get_depotId())


    '''
    Método adiciona clientes no giantTour e o depósito correspondente
    '''
    def addGiantTour(self,idCustomer,idDepot):
        self._giantTour.append(idCustomer)
        self._depots.append(idDepot)


    '''
    Método calcula diversidade do indivíduo
    '''
    def diversity(self,nClose):
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
    Método calcula o custo total da solução
    '''
    def calculateCost(self):
        self._cost = 0.0
        for r in self._routes:
            r.calculeCost()
            self._cost += r.get_totalCost()

        self._cost += self.diversity(10)
        print(self._cost)


    '''
    Método retorna rotas
    '''
    def get_routes(self):
        return self._routes


    def get_giantTour(self):
        return self._giantTour

    def get_depots(self):
        return self._depots

    def __str__(self):

        return "giantTour: " + str(self._giantTour) + "\n" + "depósitos: " + str(self._depots)
