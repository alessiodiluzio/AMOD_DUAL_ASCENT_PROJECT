import sys

from amplpy import AMPL, Environment

from controller.ufl_sscfl_controller import compute_metric_ufl, compute_ufl, compute_sscfl
from util.file_management import complete_path_name


def main():
    print('UFL - SSCFL SOLVER')
    ampl_folder = None
    while True:
        try:
            if ampl_folder is None:
                AMPL()
                break
            else:
                AMPL(Environment(ampl_folder))
                break
        except Exception:
            ampl_folder = input('Indicate AMPL path :\n')
    start_message = '\n\nChoose one :\n' \
                    'A) Solve an instance\nB) Solve all the instances inside a folder\nC) Exit\n'
    while True:
        choice = ''
        while choice.lower() != 'a' and choice.lower() != 'b' and choice.lower() != 'c':
            choice = input(start_message)
        if choice.lower() == 'a':
            message = 'A) UFL\nB) SSCFL\n'
            choice = input(message)
            while choice.lower() != 'a' and choice.lower() != 'b':
                choice = input(message)
            if choice.lower() == 'a':
                primal = is_primal()
                output = is_output()
                path = input("Insert the path to the data file:\n")
                results = is_table()
                if results is not None:
                    results = complete_path_name(results)
                if is_primal_dual():
                    compute_metric_ufl(path, primal, output, results, True, ampl_folder)
                else:
                    compute_ufl(path, primal, output, results, True, ampl_folder)
            elif choice.lower() == 'b':
                output = is_output()
                path = input("Insert the path to the data file\n")
                results = is_table()
                if results is not None:
                    results = complete_path_name(results)
                compute_sscfl(path, output, results, True, ampl_folder)
        elif choice.lower() == 'b':
            message = 'A) UFL\nB) SSCFL\n'
            choice = input(message)
            while choice.lower() != 'a' and choice.lower() != 'b':
                choice = input(message)
            if choice.lower() == 'a':
                primal = is_primal()
                output = is_output()
                path = input("Insert the path to the folder of the data files,the folder "
                             "must contains only the data files:\n")
                results = is_table()
                if results is not None:
                    results = complete_path_name(results)
                if is_primal_dual():
                    compute_metric_ufl(complete_path_name(path), primal, output, results, False, ampl_folder)
                else:
                    compute_ufl(complete_path_name(path), primal, output, results, False, ampl_folder)
            elif choice.lower() == 'b':
                output = is_output()
                path = input("Insert the path to the folder of the data files,the folder "
                             "must contains only the data files:\n")
                results = is_table()
                if results is not None:
                    results = complete_path_name(results)
                compute_sscfl(complete_path_name(path), output, results, False, ampl_folder)
        else:
            sys.exit()


def is_primal():
    message = 'Do you want to compute also the dualoc/primal-dual primal solution ? write y or n\n'
    choice = input(message)
    while choice.lower() != 'y' and choice.lower() != 'n':
        choice = input(message)
    if choice.lower() == 'y':
        return True
    return False


def is_output():
    message = 'Do you want to see the ouput messages of the calculation of algorithms ' \
              '(lot of messages will be shown) ? write y or n\n'
    choice = input(message)
    while choice.lower() != 'y' and choice.lower() != 'n':
        choice = input(message)
    if choice.lower() == 'y':
        return True
    return False


def is_table():
    message = 'Do you want output .txt and .csv files with execution results? write y or n\n'
    choice = input(message)
    while choice.lower() != 'y' and choice.lower() != 'n':
        choice = input(message)
    if choice.lower() == 'n':
        return None
    return complete_path_name(input('Insert the path to the folder where you want the results .txt file:\n'))


def is_primal_dual():
    message = 'Do you want also the computation of primal-dual algorithm ' \
              '(instances must respect metric hypothesis)? write y or n\n'
    choice = input(message)
    while choice.lower() != 'y' and choice.lower() != 'n':
        choice = input(message)
    if choice.lower() == 'n':
        return False
    return True


if __name__ == '__main__':
    main()

