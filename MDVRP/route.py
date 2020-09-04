'''
Arquivo responsável por computar e verificar restrições da rota
'''
from distances import Distances as dist
from customers import Customers as csts
from depots import Depots as dpts


class Route:
    _tour = None
    _depot = None
    _cost = float()
    _penaltyDuration = float()
    _penaltyDemand = float()
    _totalDemand = float()
    _totalDuration = float()
    _routeVehicle = None

    def __init__(self,depot):
        self._tour = [] #lista de Customer
        self._depot = depot


    '''
    Método reinicia variáveis
    '''
    def startValues(self):
        self._cost = 0.0
        self._penaltyDuration = 0.0
        self._penaltyDemand = 0.0
        self._totalDemand = 0.0
        self._totalDuration = 0.0


    '''
    Método adiciona clientes a rota
    @param id dos clientes (string)
    '''
    def addCustomer(self,customer):
        self._tour.append(customer)



    '''
    Método calcula custo total da rota
    '''
    def calculeCost(self):
        cost = 0
        demand = 0
        duration = 0
        length = len(self._tour)

        #custo do depósito ao primeiro cliente
        customer = self._tour[0]
        cost += dist.euclidianDistance(customer.get_x_coord(),customer.get_y_coord(),self._depot.get_x_coord(),self._depot.get_y_coord())
        demand += customer.get_demand()
        duration += customer.get_duration()
        #custo do último cliente ao depósito
        customer = self._tour[length-1]
        cost += dist.euclidianDistance(customer.get_x_coord(),customer.get_y_coord(),self._depot.get_x_coord(),self._depot.get_y_coord())
        demand += customer.get_demand()
        duration += customer.get_duration()
        #custo dos clientes intermediários
        for i in range(1,length-1):
            customer = self._tour[i]
            nextCustomer = self._tour[i+1]
            if i+1 < length-1:
                cost += dist.euclidianDistance(customer.get_x_coord(),customer.get_y_coord(),nextCustomer.get_x_coord(),nextCustomer.get_y_coord())
            demand += customer.get_demand()
            duration += customer.get_duration()

        self._totalDemand = demand
        self._totalDuration = duration
        self._cost = cost
        self.updatePenalty()



    '''
    Método atualiza penalizações caso restrições de duração total ou de capacidade sejam quebradas
    '''
    def updatePenalty(self):
        # se infrigir a restrição vai sofrer acréscimo de 1.000 x excedente
        capacity =  float(self._depot.get_loadVehicle())
        if self._totalDemand > capacity:
            self._penaltyDemand = 1000 * (self._totalDemand - capacity)
        else:
            self._penaltyDemand = 0.0

        duration = float(self._depot.get_durationRoute())
        #print(duration)
        if self._totalDuration > duration:
            self._penaltyDuration = 1000 * (self._totalDuration - duration)
        else:
            self._penaltyDuration = 0.0


    '''
    Método retorna o custo total calculado
    '''
    def get_totalCost(self):
        return self._cost + self._penaltyDuration + self._penaltyDemand


    def get_tour(self):
        return self._tour


    def get_depot(self):
        return self._depot


    '''
    Método imprime a rota com o depósito e o custo associado
    '''
    def printRoute(self):
        print("depósito: {} - custo: {:10.4f} - demanda: {:10.4f} - duração total: {:10.4f} - rota: {}".format(self._depot.get_id(),self.get_totalCost(),self._totalDemand,self._totalDuration,str(self._tour)))


    def __str__(self):
        return "depósito: {} - custo: {:10.4f} - demanda: {:10.4f} - duração total: {:10.4f} - rota: {}".format(self._depot.get_id(),self.get_totalCost(),self._totalDemand,self._totalDuration,str(self._tour))
