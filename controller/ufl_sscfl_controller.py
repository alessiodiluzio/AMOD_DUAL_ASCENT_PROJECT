import time

from algorithm.sscfl_dualoc import sscfl_dualoc
from algorithm.ufl_dualoc import dualoc
from algorithm.ufl_primal_dual import primal_dual
from algorithm.ufl_simple_dualoc import simple_dualoc
from ampl.solve import solve_ufl_instance, solve_sscfl_instance
from util.file_management import get_list_all_files_name, print_table_to_file, write_csv_file
from util.metric_hypothesis_check import metric_hypothesis
from util.parsing_instance_file import parse_test_instance_file_ufl, parse_test_instance_file_sscfl


# Calcola la soluzione di un problema di UFL usando il solver AMPL per il problema intero e rilassato
# e l'algoritmo DUALOC restituendo oltre alle soluzioni anche i relativi tempi di esecuzione
# filename : path al file di istanza
# primal : True se si richiede il calcolo della soluzione primale del Dualoc False altrimenti
# output : True se richiede la stampa dei calcoli delgli algoritmi eseguiti
# ampl_folder : Path alla cartella di installazione di AMPL
def ufl(filename, primal, output, ampl_folder):
    try:
        ufl_instance = parse_test_instance_file_ufl(filename)
    except Exception:
        raise SystemExit("Error reading file")
    time_profile = []
    start = time.time()
    optimal_pli = solve_ufl_instance('UFL.mod', ufl_instance, ampl_folder)
    time_profile.append(time.time()-start)
    start = time.time()
    optimal_pl = solve_ufl_instance('RELAXED_UFL.mod', ufl_instance, ampl_folder)
    time_profile.append(time.time()-start)
    start = time.time()
    dualoc_value = dualoc(ufl_instance, output, primal)
    time_profile.append(time.time()-start)
    result = [ufl_instance.get_n_of_facility()] + [ufl_instance.get_n_of_client()] + [optimal_pli] + \
             [time_profile[0]] + [optimal_pl] + [time_profile[1]]
    if primal:
        result += [dualoc_value[0]] + [time_profile[2]] + [dualoc_value[1]]
        return result
    return result + [dualoc_value] + [time_profile[2]]


# Calcola la soluzione di un problema di UFL metri usando il solver AMPL per il problema intero e rilassato
# l'algoritmo DUALOC e l'algoritmo Primale - Duale restituendo oltre alle soluzioni anche i relativi tempi di esecuzione
# filename : path al file di istanza
# primal : True se si richiede il calcolo della soluzione primale False altrimenti
# output : True se richiede la stampa dei calcoli delgli algoritmi eseguiti
# ampl_folder : Path alla cartella di installazione di AMPL
def metric_ufl(filename, primal, output, ampl_folder):
    try:
        ufl_instance = parse_test_instance_file_ufl(filename)
    except Exception:
        raise SystemExit("Error reading file")
    time_profile = []
    start = time.time()
    optimal_pli = solve_ufl_instance('UFL.mod', ufl_instance, ampl_folder)
    time_profile.append(time.time() - start)
    start = time.time()
    optimal_pl = solve_ufl_instance('RELAXED_UFL.mod', ufl_instance, ampl_folder)
    time_profile.append(time.time() - start)
    start = time.time()
    dualoc_value = dualoc(ufl_instance, output, primal)
    time_profile.append(time.time() - start)
    if metric_hypothesis(ufl_instance):
        start = time.time()
        primal_dual_value = primal_dual(ufl_instance, output, primal)
        time_profile.append(time.time() - start)
    else:
        primal_dual_value = 'Violated metric Hp'
        if primal:
            primal_dual_value = ['Violated metric Hp', 'Violated metric Hp']
        time_profile.append(0)
    result = [ufl_instance.get_n_of_facility()] + [ufl_instance.get_n_of_client()] + \
             [optimal_pli] + [time_profile[0]] + [optimal_pl] + [time_profile[1]]
    if primal:
        result += [dualoc_value[0]] + [time_profile[2]] + [primal_dual_value[0]] + [time_profile[3]] \
                  + [dualoc_value[1]] + [primal_dual_value[1]]
    else:
        result += [dualoc_value] + [time_profile[2]] + [primal_dual_value] + [time_profile[3]]
    return result


# Calcola la soluzione di un problema di SSCFL usando il solver AMPL per il problema intero e rilassato
# e l'algoritmo DUALOC adattato restituendo oltre alle soluzioni anche i relativi tempi di esecuzione
# filename : path al file di istanza
# output : True se richiede la stampa dei calcoli delgli algoritmi eseguiti
# ampl_folder : Path alla cartella di installazione di AMPL
def sscfl(filename, output, ampl_folder):
    try:
        sscfl_instance = parse_test_instance_file_sscfl(filename)
    except Exception:
        raise SystemExit("Error reading file")
    time_profile = []
    start = time.time()
    optimal_pli = solve_sscfl_instance('SSCFL.mod', sscfl_instance, ampl_folder)
    time_profile.append(time.time() - start)
    start = time.time()
    optimal_pl = solve_sscfl_instance('RELAXED_SSCFL.mod', sscfl_instance, ampl_folder)
    time_profile.append(time.time() - start)
    start = time.time()
    dualoc_value = sscfl_dualoc(sscfl_instance, output)
    time_profile.append(time.time() - start)
    return [sscfl_instance.get_n_of_facility()] + [sscfl_instance.get_n_of_client()] + [optimal_pli] + \
           [time_profile[0]] + [optimal_pl] + [time_profile[1]] + [dualoc_value] + [time_profile[2]]


# Calcola la soluzione di un problema di UFL usando l'algoritmo DUALOC
# e l'algoritmo di ascesa duale 'semplice'
# restituendo oltre alle soluzioni anche i relativi tempi di esecuzione
# filename : path al file di istanza
# output : True se richiede la stampa dei calcoli delgli algoritmi eseguiti
def ufl_simple_dualoc(filename, output):
    try:
        ufl_instance = parse_test_instance_file_ufl(filename)
    except Exception:
        raise SystemExit("Error reading file")
    time_profile = []
    start = time.time()
    dualoc_value = dualoc(ufl_instance, output, False)
    time_profile.append(time.time()-start)
    start = time.time()
    simple_dualoc_value = simple_dualoc(ufl_instance, output)
    time_profile.append(time.time() - start)
    return [ufl_instance.get_n_of_facility(), ufl_instance.get_n_of_client(), dualoc_value,
            time_profile[0], simple_dualoc_value, time_profile[1]]


# Calcola la soluzione di molteplici istanze di SSCFL
# dir_path : Path alla directory contenente i file di istanza
# output : True se richiede la stampa dei calcoli delgli algoritmi eseguiti
# results : Path alla directory di output per il file del risultato del testing
# single_file : True se si è richiesta l'analisi di un singolo file
# ampl_folder : Path alla cartella di installazione di AMPL
def compute_sscfl(dir_path, output, results, single_file, ampl_folder):
    field = ['Instance name', 'n of facilities', 'n of clients', 'PLI optimal solution', 'PLI execution time (sec)',
             'relaxed PLI optimal solution', 'PL execution time  (sec)', 'dualoc solution value',
             'dualoc execution time (sec)']
    if not single_file:
        files = get_list_all_files_name(dir_path)
    else:
        files = [dir_path]
    table = []
    computed = 0
    for file in files:
        print("Computing : ", file, " Computed : ", computed)
        if single_file:
            filename = file
        else:
            filename = dir_path+file
        row = [file] + sscfl(filename, output, ampl_folder)
        table.append(row)
        computed += 1
    if results is not None:
        write_csv_file(results + 'sscfl_results.csv', field, table)
        print_table_to_file(results+'sscfl_results.txt', field, table)


# Calcola la soluzione di molteplici istanze di UFL
# dir_path : Path alla directory contenente i file di istanza
# primal : True se si richiede il calcolo della soluzione primale del Dualoc False altrimenti
# output : True se richiede la stampa dei calcoli delgli algoritmi eseguiti
# results : Path alla directory di output per il file del risultato del testing
# single_file : True se si è richiesta l'analisi di un singolo file
# ampl_folder : Path alla cartella di installazione di AMPL
def compute_ufl(dir_path, primal, output, results, single_file, ampl_folder):
    field = ['Instance name', 'n of facilities', 'n of clients', 'PLI optimal solution', 'PLI execution time (sec)',
             'relaxed PLI optimal solution', 'PL execution time (sec)', 'dualoc solution value',
             'dualoc execution time (sec)']
    if primal:
        field += ['dualoc primal solution']
    if not single_file:
        files = get_list_all_files_name(dir_path)
    else:
        files = [dir_path]
    table = []
    computed = 0
    for file in files:
        print("Computing : ", file, " Computed : ", computed)
        if single_file:
            filename = dir_path
        else:
            filename = dir_path+file
        print(filename)
        row = [file] + ufl(filename, primal, output, ampl_folder)
        table.append(row)
        computed += 1
    if results is not None:
        write_csv_file(results+'ufl_results.csv', field, table)
        print_table_to_file(results+'ufl_results.txt', field, table)


# Calcola la soluzione di molteplici istanze di UFL metrico
# dir_path : Path alla directory contenente i file di istanza
# primal : True se si richiede il calcolo della soluzione primale  False altrimenti
# output : True se richiede la stampa dei calcoli delgli algoritmi eseguiti
# results : Path alla directory di output per il file del risultato del testing
# single_file : True se si è richiesta l'analisi di un singolo file
# ampl_folder : Path alla cartella di installazione di AMPL
def compute_metric_ufl(dir_path, primal, output, results, single_file, ampl_folder):
    field = ['Instance name', 'n of facilities', 'n of clients', 'PLI optimal solution', 'PLI execution time (sec)',
             'relaxed PLI optimal solution', 'PL execution time  (sec)', 'dualoc solution value',
             'dualoc execution time (sec)', 'Primal-Dual solution', 'P-D   execution time (sec)']
    if primal:
        field += ['dualoc primal solution', 'P-D primal solution']
    if not single_file:
        files = get_list_all_files_name(dir_path)
    else:
        files = [dir_path]
    table = []
    computed = 0
    for file in files:
        print("Computing : ", file, " Computed : ", computed)
        if single_file:
            filename = file
        else:
            filename = dir_path+file
        row = [file] + metric_ufl(filename, primal, output, ampl_folder)
        table.append(row)
        computed += 1
    if results is not None:
        write_csv_file(results + 'metric_ufl_results.csv', field, table)
        print_table_to_file(results+'metric_ufl_results.txt', field, table)


# Calcola la soluzione di molteplici istanze di UFL comprando l'esecuzione di DUALOC
# e algoritmo di Ascesa Duale semplice
# dir_path : Path alla directory contenente i file di istanza
# output : True se richiede la stampa dei calcoli delgli algoritmi eseguiti
# results : Path alla directory di output per il file del risultato del testing
# single_file : True se si è richiesta l'analisi di un singolo file
def compute_comparison_simple_erlenkotter_dualoc(dir_path, output, results, single_file):
    field = ['Instance name', 'n of facilities', 'n of clients', 'dualoc solution value',
             'dualoc execution time (sec)', 'simple dualoc solotion value', 'simple dualoc execution time (sec)']
    if not single_file:
        files = get_list_all_files_name(dir_path)
    else:
        files = [dir_path]
    table = []
    computed = 0
    for file in files:
        print("Computing : ", file, " Computed : ", computed)
        if single_file:
            filename = file
        else:
            filename = dir_path+file
        print(filename)
        row = [file] + ufl_simple_dualoc(filename, output)
        table.append(row)
        computed += 1
    if results is not None:
        write_csv_file(results+'ufl_simple_dualoc_results.csv', field, table)
        print_table_to_file(results+'ufl_simple_dualoc_results.txt', field, table)



