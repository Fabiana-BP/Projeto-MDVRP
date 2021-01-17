import math

I = []  # instâncias (amostragem)
X = []  # espaço de parâmetros
C = math.inf  # custo
B = 0  # estimativa de ajuste


class IR:
    _nIter = int()  # número de iterações
    _nParams = int()  # número de parâmetros
    _params = {}  # parâmetros
    _mi = int()  # número necessário de instâncias para um primeiro teste - tFirst

    def __init__(self, params, mi):
        self._nParams = len(params)
        self._params = params
        self._nIter = 2 + math.log(self._nParams, 2)
        self._mi = mi

    def iterateRacing(self, BUsed, budget1, tEach):
        paramsSample = self.sampleUniform(X)
        paramsElite = self.race(paramsSample, budget1)
        j = 1
        while BUsed <= B:
            j += 1
            paramsNew = self.sample(X, paramsElite)
            Bj = self.budgetJ(BUsed, j)
            paramsJ = self.join(paramsNew, paramsElite,
                                self.nCandidateConfigurationsJ(Bj, j, tEach))
            paramsElite = self.race(paramsJ, Bj)

        return paramsElite

    def race(self, paramsSample, budget):
        return ""

    '''
    Método retorna uma amostra uniforme do espaço de parâmetros 
    '''

    def sampleUniform(self, X):
        return ""

    '''
    Método retorna uma amostra do espaço de parâmetros 
    '''

    def sample(self, X, paramsElite):
        return ""

    '''
    Método retorna uuma lista de n elementos a partir de dois conjuntos iniciais
    '''
    def join(conjA, conjB, n):
        return ""

    '''
    Método retorna a estimativa de ajuste limite
    @param BUsed
    @param j
    @return estimativa de ajuste limite
    '''

    def budgetJ(self, BUsed, j):
        return (B-BUsed)/(self._nIter-j+1)

    '''
    Método retorna o número de configurações candidatas
    @param budeget j
    @param j
    @param tEach - número necessário de instâncias
    @return número de configurações candidatas
    '''

    def nCandidateConfigurationsJ(self, budgetJ, j, tEach):
        return int(round(budgetJ/(self._mi + tEach * min(5, j))))
