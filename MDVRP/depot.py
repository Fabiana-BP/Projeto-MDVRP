class Depot:

    def __init__(self):
        self._id = 0
        self._x_coord = 0
        self._y_coord = 0
        self._durationRoute = 0
        self._numberVehicles = 0
        self._loadTotal = 0


    def get_id(self):
        return self._id


    def set_id(self,id):
        self._id = id


    def get_x_coord(self):
        return self._x_coord


    def get_y_coord(self):
        return self._y_coord


    def set_xy_coord(self,x,y):
        self._x_coord = x
        self._y_coord = y


    def get_durationRoute(self):
        return self._durationRoute


    def set_durationRoute(self,d):
        self._durationRoute = d


    def get_numberVehicles(self):
        return self._numberVehicles


    def set_numberVehicles(self,v):
        self._numberVehicles = v


    def get_loadTotal(self):
        return self._load


    def set_loadTotal(self,l):
        self._load = l


    def __str__(self):
        return "id: " + str(self._id) + "  coord: " + str(self._x_coord) + ".." + str(self._y_coord) + "  loadTotal: " + str(self._load) + "  vehicles: "+ str(self._numberVehicles)
