'''
Arquivo responsável por carregar a aplicação
@author Fabiana Barreto Pereira
'''
from readingDatas import ReadingDatas
from customers import Customers
from depots import Depots
from distances import Distances

def main():
    r = ReadingDatas("dat/p01")
    r.readFile()
    c = Customers()
    c.addCustomers(r)
    print(c.get_customersList()['8'])
    for cst in c.get_customersList().values():
        print(cst)

    dpts = Depots()
    dpts.addDepots(r)
    #print("\n\n\n\")
    print(dpts.get_depotsList()['1'])
    for dpt in dpts.get_depotsList().values():
        print(dpt)

    d = Distances()
    d.euclidianDistanceAll(c.get_customersList(),dpts.get_depotsList())



if __name__ == "__main__":
    main()
