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
        self._infeasible = False


    '''
    Método reinicia variáveis
    '''
    def startValues(self):
        self._cost = 0.0
        self._penaltyDuration = 0.0
        self._penaltyDemand = 0.0
        self._totalDemand = 0.0
        self._totalDuration = 0.0
        self._infeasible = False


    '''
    Método adiciona clientes a rota
    @param id dos clientes (string)
    '''
    def addCustomer(self,customer):
        self._tour.append(customer)

    '''
    Método insere cliente na rota no índice index
    @param cliente
    @param índice
    '''
    def insertCustomer(self,customer,index):
        self._tour.insert(index,customer)


    '''
    Método remove cliente da rota
    @param índice do cliente a ser removido
    @return cliente removido
    '''
    def popCustomer(self,index):
        return self._tour.pop(index)



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
    Método calcula custo ao adicionar um nó a mais na rota
    @param customer, índice de inserção
    @return lista [custo com penalização, custo sem penalização, carregamento total, duração total]
    '''
    def costWithNode(self,customer,index):
        cost = 0.0
        load = self._totalDemand + customer.get_demand()
        duration = self._totalDuration + customer.get_duration()
        length = len(self._tour)

        #verificar se ele ligará ao depósito
        if index == 0:
            cost = self._cost - dist.euclidianDistance(self._depot.get_x_coord(),self._depot.get_y_coord(),self._tour[0].get_x_coord(),self._tour[0].get_y_coord())
            + dist.euclidianDistance(self._depot.get_x_coord(),self._depot.get_y_coord(),customer.get_x_coord(),customer.get_y_coord())
            + dist.euclidianDistance(customer.get_x_coord(),customer.get_y_coord(),self._tour[0].get_x_coord(),self._tour[0].get_y_coord())
        elif index == length:
            cost = self._cost - dist.euclidianDistance(self._depot.get_x_coord(),self._depot.get_y_coord(),self._tour[length-1].get_x_coord(),self._tour[length-1].get_y_coord())
            + dist.euclidianDistance(self._depot.get_x_coord(),self._depot.get_y_coord(),customer.get_x_coord(),customer.get_y_coord())
            + dist.euclidianDistance(self._tour[length-1].get_x_coord(),self._tour[length-1].get_y_coord(),customer.get_x_coord(),customer.get_y_coord())
        #está entre dois clientes
        else:
             cost = self._cost - dist.euclidianDistance(self._tour[index-1].get_x_coord(),self._tour[index-1].get_y_coord(),self._tour[index+1].get_x_coord(),self._tour[index+1].get_y_coord())
             + dist.euclidianDistance(self._tour[index-1].get_x_coord(),self._tour[index-1].get_y_coord(),customer.get_x_coord(),customer.get_y_coord())
             + dist.euclidianDistance(customer.get_x_coord(),customer.get_y_coord(),self._tour[index].get_x_coord(),self._tour[index].get_y_coord())

        #verificar se há penalizações
        costTotal = cost
        if load > self._depot.get_loadVehicle():
            costTotal += 1000 * load - self._depot.get_loadVehicle()
        if duration > self._depot.get_durationRoute():
            costTotal += 1000 * duration - self._depot.get_durationRoute()

        return [costTotal,cost,load,duration]


    '''
    Método calcula custo ao remover um nó da rota
    @param customer
    @return lista [custo com penalização, custo sem penalização, carregamento total, duração total]
    '''
    def costWithoutNode(self,customer):
        cost = 0.0
        load = self._totalDemand - customer.get_demand()
        duration = self._totalDuration - customer.get_duration()
        length = len(self._tour)

        if length == 1:#só tem esse cliente
            return [0,0,0,0]
        #verificar se ele liga ao depósito
        elif self._tour[0].get_id() == customer.get_id():
            cost = self._cost - dist.euclidianDistance(self._depot.get_x_coord(),self._depot.get_y_coord(),customer.get_x_coord(),customer.get_y_coord())
            + dist.euclidianDistance(self._depot.get_x_coord(),self._depot.get_y_coord(),self._tour[1].get_x_coord(),self._tour[1].get_y_coord())
            - dist.euclidianDistance(customer.get_x_coord(),customer.get_y_coord(),self._tour[1].get_x_coord(),self._tour[1].get_y_coord())

        elif self._tour[length-1].get_id() == customer.get_id():
            cost = self._cost - dist.euclidianDistance(self._depot.get_x_coord(),self._depot.get_y_coord(),customer.get_x_coord(),customer.get_y_coord())
            + dist.euclidianDistance(self._depot.get_x_coord(),self._depot.get_y_coord(),self._tour[length-2].get_x_coord(),self._tour[length-2].get_y_coord())
            - dist.euclidianDistance(customer.get_x_coord(),customer.get_y_coord(),self._tour[length-2].get_x_coord(),self._tour[length-2].get_y_coord())
        #está entre dois clientes
        else:
            for i,cst in enumerate(self._tour):
                if cst.get_id() == customer.get_id():
                    cost = self._cost - dist.euclidianDistance(self._tour[i-1].get_x_coord(),self._tour[i-1].get_y_coord(),customer.get_x_coord(),customer.get_y_coord())
                    - dist.euclidianDistance(customer.get_x_coord(),customer.get_y_coord(),self._tour[i+1].get_x_coord(),self._tour[i+1].get_y_coord())
                    + dist.euclidianDistance(self._tour[i-1].get_x_coord(),self._tour[i-1].get_y_coord(),self._tour[i+1].get_x_coord(),self._tour[i+1].get_y_coord())
                    break
        #verificar se há penalizações
        costTotal = cost
        if load > self._depot.get_loadVehicle():
            costTotal += 1000 * load - self._depot.get_loadVehicle()
        if duration > self._depot.get_durationRoute():
            costTotal += 1000 * duration - self._depot.get_durationRoute()

        return [costTotal,cost,load,duration ]



    '''
    Método atualiza penalizações caso restrições de duração total ou de capacidade sejam quebradas
    '''
    def updatePenalty(self):
        # se infrigir a restrição vai sofrer acréscimo de 1.000 x excedente
        capacity =  float(self._depot.get_loadVehicle())
        if self._totalDemand > capacity:
            self._penaltyDemand = 1000 * (self._totalDemand - capacity)
            self._infeasible = True
        else:
            self._penaltyDemand = 0.0

        duration = float(self._depot.get_durationRoute())
        #print(duration)
        if self._totalDuration > duration:
            self._penaltyDuration = 1000 * (self._totalDuration - duration)
            self._infeasible = True
        else:
            self._penaltyDuration = 0.0


    '''
    Método retorna o custo total calculado
    '''
    def get_totalCost(self):
        return self._cost + self._penaltyDuration + self._penaltyDemand


    def set_cost(self,cost,load,duration):
        self._cost = cost
        self._totalDemand = load
        self._totalDuration = duration
        self.updatePenalty()



    def get_tour(self):
        return self._tour


    def get_depot(self):
        return self._depot

    def is_infeasible(self):
        return self._infeasible


    '''
    Método imprime a rota com o depósito e o custo associado
    '''
    def printRoute(self):
        print("depósito: {} - custo: {:10.4f} - demanda: {:10.4f} - duração total: {:10.4f} - rota: {}".format(self._depot.get_id(),self.get_totalCost(),self._totalDemand,self._totalDuration,str(self._tour)))


    def __str__(self):
        return "depósito: {} - custo: {:10.4f} - demanda: {:10.4f} - duração total: {:10.4f} - rota: {}".format(self._depot.get_id(),self.get_totalCost(),self._totalDemand,self._totalDuration,str(self._tour))

    def __repr__(self):
        return "depósito: {} - rota: {} - custo com penalização: {:10.4f}".format(self._depot.get_id(),str(self._tour),self.get_totalCost())
