'''
Arquivo responsável por computar e verificar restrições da rota
'''
from distances import Distances as dist
from customers import Customers as csts
from depots import Depots as dpts


class Route:
    _tour = None
    _depotId = str()
    _cost = float()
    _penaltyDuration = float()
    _penaltyDemand = float()
    _totalDemand = float()
    _totalDuration = float()

    def __init__(self,depotId):
        self._tour = [] #lista de strings
        self._depotId = depotId


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
    def addCustomer(self,idCustomer):
        self._tour.append(str(idCustomer))


    '''
    Método calcula custo total da rota
    '''
    def calculeCost(self):
        cost = 0
        demand = 0
        duration = 0
        length = len(self._tour)

        #custo do depósito ao primeiro cliente
        idcustomer = self._tour[0]
        customer = csts.get_customersList()[idcustomer]
        depot = dpts.get_depotsList()[self._depotId]
        cost += dist.euclidianDistance(customer.get_x_coord(),customer.get_y_coord(),depot.get_x_coord(),depot.get_y_coord())
        demand += customer.get_demand()
        duration += customer.get_duration()
        #custo do último cliente ao depósito
        idcustomer = self._tour[length-1]
        customer = csts.get_customersList()[idcustomer]
        cost += dist.euclidianDistance(customer.get_x_coord(),customer.get_y_coord(),depot.get_x_coord(),depot.get_y_coord())
        demand += customer.get_demand()
        duration += customer.get_duration()
        #custo dos clientes intermediários
        for i in range(1,length-1):
            idcustomer = self._tour[i]
            customer = csts.get_customersList()[idcustomer]
            idcustomer2 = self._tour[i+1]
            nextCustomer = csts.get_customersList()[idcustomer2]
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
        capacity =  float(dpts.get_depotsList()[self._depotId].get_loadVehicle())
        if self._totalDemand > capacity:
            self._penaltyDemand = 1000 * (self._totalDemand - capacity)
        else:
            self._penaltyDemand = 0.0

        duration = float(dpts.get_depotsList()[self._depotId].get_durationRoute())
        print(duration)
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


    def get_depotId(self):
        return self._depotId

    '''
    Método imprime a rota com o depósito e o custo associado
    '''
    def printRoute(self):
        print("depósito: {} - custo: {:10.4f} - demanda: {:10.4f} - duração total: {:10.4f} - rota: {}".format(self._depotId,self.get_totalCost(),self._totalDemand,self._totalDuration,self._tour))


    def __str__(self):
        return "depósito: {} - custo: {:10.4f} - demanda: {:10.4f} - duração total: {:10.4f} - rota: {}".format(self._depotId,self.get_totalCost(),self._totalDemand,self._totalDuration,self._tour)
