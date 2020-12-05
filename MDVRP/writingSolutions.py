
class WritingSolutions:

    def __init__(self,name_file):
        self._f = name_file

    def writeFile(self,solution):
        content = []
        # f = open(self._f,'r')
        # content = f.readlines()
        # primeira linha o custo
        content.append('%.2f \n' % (solution.get_cost()))
        routes = solution.get_routes()
        # para cada rota: no_do_dpto no_do_veic durac_rota carreg_veic list_ord_clientes  
        text = ""
        j = 0
        # ordenar rota por depósito
        routesSorted = sorted(routes, key = lambda x: x.get_depot().get_id())
        depotPrev = routesSorted[0].get_depot().get_id()
        for r in routesSorted:
            depot = r.get_depot().get_id()
            if depotPrev != depot:
                j = 0
            j += 1
            text += str(depot) + " "
            text += str(j) + " " + str(r.get_totalDuration()) + " "
            text += str(r.get_totalDemand()) + "   "
            for c in r.get_tour():
                text += str(c.get_id()) + " "
            text += "\n"
            depotPrev = depot
            
        content.append(text+"\n")
        f = open(self._f,'a')
        f.writelines(content)
        f.close()


