import random
from random import randint

from util.file_management import get_list_all_files_name, complete_path_name
from util.metric_hypothesis_check import metric_hypothesis_change
from util.parsing_instance_file import parse_test_instance_file_ufl


# Genera un'istanza di UFL con parametri random
def write_ufl_instance(n):
    facility_number = [16, 30, 50, 60, 80]
    client_number = [50, 200, 300, 500]
    clients = random.choice(client_number)
    facilities = random.choice(facility_number)
    # new_trasporting_cost = metric_hypothesis(sscfl_instance.get_transporting_cost(), sscfl_instance)
    # sscfl_instance.set_transporting_cost(new_trasporting_cost)
    filename = 'istanze/'+str(clients)+'-'+str(facilities)+'-'+str(n)+'.dat'
    with open(filename, "w") as f:
        c = str(facilities)
        p = str(clients)
        f.write(c+"    "+p+'\n')
        multiplier = randint(10, 100)
        setup_costs = []
        minimum = 0
        for i in range(facilities):
            setup_cost = multiplier * randint(1, 9)
            if minimum == 0:
                minimum = setup_cost
            if setup_cost < minimum:
                minimum = setup_cost
            setup_costs.append(setup_cost)
            f.write(str(0)+"    "+str(setup_cost)+'\n')
        string = ''
        for i in range(clients):
            string += str(0) + "    "
        string += "\n"
        f.write(string)
        setup_costs.sort()
        setup_1 = setup_costs[:int(len(setup_costs)/4)]
        setup_2 = setup_costs[3*int(len(setup_costs)/4):]
        tmp_setup = setup_1+setup_2
        for j in range(facilities):
            string = ''
            for i in range(clients):
                string += str(int(random.choice(tmp_setup)*randint(6, 9)/10)) + "    "
            string += "\n"
            f.write(string)
    return filename


# Genera un'istanza metrica di UFL partendo da un'altra istanza
def write_ufl_metric_instances(dir_path, k):
    files = get_list_all_files_name(dir_path)
    for y in range(k):
        file = random.choice(files)
        files.remove(file)
        print("Metric on " + file)
        ufl_instance = parse_test_instance_file_ufl(complete_path_name(dir_path)+file)
        ufl_instance = metric_hypothesis_change(ufl_instance)

        with open('C:\\Users\\aless\\OneDrive\\Documents'
                  '\\AMOD_DUAL_ASCENT_PROJECT\\ufl_instance_generator\\istanze_metriche\\metric-'+file, "w") as f:
            c = str(ufl_instance.get_n_of_facility())
            p = str(ufl_instance.get_n_of_client())
            f.write(c + "    " + p + '\n')
            for i in range(ufl_instance.get_n_of_facility()):
                f.write(str(0) + "    " + str(ufl_instance.get_opening_cost()[i]) + '\n')
            string = ''
            for i in range(ufl_instance.get_n_of_client()):
                string += str(0) + "    "
            string += "\n"
            f.write(string)
            for j in range(ufl_instance.get_n_of_facility()):
                string = ''
                for i in range(ufl_instance.get_n_of_client()):
                    string += str(ufl_instance.get_transporting_cost()[i][j]) + "    "
                string += "\n"
                f.write(string)
