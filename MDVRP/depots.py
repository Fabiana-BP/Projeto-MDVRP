'''
Arquivo responsável por armazenar dados de todos os depósitos
@author Fabiana Barreto Pereira
'''

from depot import Depot


class Depots:
    def __init__(self):
        self._depotsList={} #dicionário de depósitos

    def addDepots(self,rd):
        ldepot=[]
        for i in range(rd.get_numberDepots()):
            dataDepot = rd.get_dataDepots()[i].split()
            dpt = Depot()
            dpt.set_id(int(dataDepot[0]))
            dpt.set_xy_coord(float(dataDepot[1]),float(dataDepot[2]))
            dpt.set_durationRoute(rd.get_durationRoute())
            dpt.set_numberVehicles(rd.get_numberVehicles())
            dpt.set_loadTotal(rd.get_load()*rd.get_numberVehicles())

            ldepot.append((dataDepot[0],dpt))

        self._depotsList=dict(ldepot)

    def get_depotsList(self):
        return self._depotsList
