from entity.sscfl_instance import SscflInstance
from entity.ufl_instance import UflInstance


# Parsing del file di una istanza d ufl_instance_generator di SSCFL in un oggetto sscfl_instance
def parse_test_instance_file_sscfl(file):
    with open(file) as fp:
        lines = fp.readlines()
    values = read_numbers_from_line(1, lines, 2)
    n_of_facility = values[0]
    n_of_clients = values[1]
    opening_costs = []
    demand = []
    capacity = []
    for i in range(2, 2+n_of_facility):
        read = read_numbers_from_line(i, lines, 2)
        opening_costs.append(read[1])
        capacity.append(read[0])
    transporting_costs_tmp = []
    tmp = read_numbers_from_line(2+n_of_facility, lines, n_of_clients)
    for dem in tmp:
        demand.append(dem)
    for i in range(3+n_of_facility, 3+2*n_of_facility):
        transporting_costs_tmp += [read_numbers_from_line(i, lines, n_of_clients)]
    transporting_costs = [[0 for i in range(0, n_of_facility)] for j in range(0, n_of_clients)]
    for i in range(0, n_of_facility):
        for j in range(0, n_of_clients):
            transporting_costs[j][i] = transporting_costs_tmp[i][j]
    return SscflInstance(transporting_costs, opening_costs, demand, capacity)


# Parsing del file di una istanza d ufl_instance_generator di UFL in un oggetto ufl_instance
def parse_test_instance_file_ufl(file):
    with open(file) as fp:
        lines = fp.readlines()
    values = read_numbers_from_line(1, lines, 2)
    n_of_facility = values[0]
    n_of_clients = values[1]
    opening_costs = []
    for i in range(2, 2+n_of_facility):
        opening_costs += [read_numbers_from_line(i, lines, 2)[1]]
    transporting_costs_tmp = []
    for i in range(3+n_of_facility, 3+2*n_of_facility):
        transporting_costs_tmp.append(read_numbers_from_line(i, lines, n_of_clients))
    transporting_costs = [[0 for i in range(0, n_of_facility)] for j in range(0, n_of_clients)]
    for i in range(0, n_of_facility):
        for j in range(0, n_of_clients):
            transporting_costs[j][i] = transporting_costs_tmp[i][j]
    return UflInstance(transporting_costs, opening_costs)


# Legge n interi da una stringa contenuta in una lista
def read_numbers_from_line(line, lines, n):
    c = lines[line-1]
    read_values = [int(s) for s in c.split() if s.isdigit()]
    return read_values
    k = 0
    for i in range(0, n):
        tmp = ''
        while k < len(c) and (c[k] == ' ' or c[k] == '.'):
            k += 1
        while k < len(c) and c[k] != ' ' and c[k] != '\n':
            tmp += c[k]
            k += 1
        read_values += [int(tmp)]
        print(c, " ", k)
    return read_values
