# dados base
DIRECTORY_DATAS = "instances/"
DIRECTORY_RESULT = "result/"
BST_COST = [576.87, 473.53, 641.19, 1001.04, 750.03, 876.50, 881.97, 4387.38, 3873.64, 3650.04, 3546.06,
            1318.95, 1318.95, 1360.12, 2505.42, 2572.23, 2708.99, 3702.85, 3827.06, 4058.07, 5474.74, 5702.16, 6078.75]
INSTANCES = ["p01", "p02", "p03", "p04", "p05", "p06", "p07", "p08", "p09", "p10", "p11",
             "p12", "p13", "p14", "p15", "p16", "p17", "p18", "p19", "p20", "p21", "p22", "p23"]
# parametros
# fração máxima de distribuição de clientes entre depósitos
FRAC_MAX_DISTRIBUTION = 1.5
SIZE_POP = 20  # população inicial
SIZE_DESC = 5  # número de descendentes
PROB_MUTATION = 0.2
PROB_LS_POP = 0.8  # probabilidade de busca local na formação da população
PROB_LS = 0.9  # probabilidade busca local
PROB_LS_BEST = 0.7  # probabilidade busca local promotion
PROB_LS_BEST_P = 0.7  # probabilidade busca local assíncrona
GEN = 60  # número de gerações
GEN_NO_EVOL = 15  # número permitido de gerações sem mudanças
SP = 2  # pressão seletiva para linear ranking
N_REPETITIONS = 10
TIME_TOTAL = 3600  # tempo em segundos

# METRIC = 3.5 # métrica de diversidade
# CONT_METRIC = 5 # quantidade de vezes que a métrica de diversidade pode ser desrespeitada
