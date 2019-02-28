import csv
import os

from prettytable import PrettyTable


# Restituisce una lista contenenete il nome di tutti i file contenuti in un directory
# dir_path : Path alla directory
def get_list_all_files_name(dir_path):
    all_files_path = []
    for (dirpath, dirnames, filenames) in os.walk(dir_path):
        for f in filenames:
            all_files_path.append(f)
    return all_files_path


# Stampa su file .txt una tabella con i risultati di test di una esecuzione
# filename : file di output
# field : nomi delle colonne della tabella
# results : risultati di test
def print_table_to_file(filename, field, results):
    table = PrettyTable()
    table.field_names = field
    for row in results:
        table.add_row(row)
    with open(filename, 'w') as output:
        output.write(str(table))
        output.flush()


# Estrae il nome di un file dal Path che lo indica
def extract_file_name_from_path(path):
    path, filename = os.path.split(path)
    return filename


# Completa un Path aggiungendo '\' o '/' finali
def complete_path_name(dir_path):
    try:
        if dir_path[len(dir_path)-1] != '\\' and dir_path[len(dir_path)-1] != '/':
            if '/' in dir_path:
                dir_path += '/'
            else:
                dir_path += '\\'
        return dir_path
    except Exception:
        raise SystemExit("Invalid Path")


# Stampa su file .csv una  i risultati di test di una esecuzione
# filename : file di output
# field : nomi dei campi del file
# results : risultati di test
def write_csv_file(filename, fields, lines):
    with open(filename, mode='w') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(fields)
        csv_writer.writerows(lines)
        csv_file.flush()



