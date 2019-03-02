from fractions import Fraction


# Algoritmo Primale - Duale per la risoluzione di problemi di UFL
def primal_dual(ufl_instance, output, primal):
    # Vettore a che contiene il valore corrente delle variabili duali Aj
    a = [Fraction(0, 1)] * ufl_instance.get_n_of_client()
    # Vettore b che contiene il valore corrente delle variabili duali Bij
    b = [[Fraction(0, 1) for i in range(0, ufl_instance.get_n_of_facility())]
         for j in range(0, ufl_instance.get_n_of_client())]
    # active_a[j] = True se e solo se la variabile duale Aj può essere incrementata nell'iterazione corrente
    active_a = [True] * ufl_instance.get_n_of_client()
    # active_b[i][j] = True se e solo se la variabile duale Bij può essere incrementata nell'iterazione corrente
    active_b = [[False for i in range(0, ufl_instance.get_n_of_facility())]
                for j in range(0, ufl_instance.get_n_of_client())]
    # Insieme degli 'archi tight' nella soluzione corrente
    tight_arch = []
    # Assegnamento dei clienti alle facility temporaneamente aperte
    assigned = {}
    # facility temporaneamente aperte
    opened_facility = []
    iteration = 0
    clock = 0
    while True in active_a:
        iteration += 1
        # calcolo del valore di incremento massimo  delta per l'iterazione corrente
        delta = compute_delta(a, b, ufl_instance, active_b, opened_facility, tight_arch)
        # incremento del clock del problema
        clock += delta
        if output:
            print("--- STEP ", iteration, "---")
            print("delta = ", float(delta))
            print("clock_t = ", float(clock))
        # ogni variabile Aj e Bij attiva viene incrementata di Delta
        for i in range(0, ufl_instance.get_n_of_client()):
            if active_a[i]:
                a[i] += delta
            else:
                continue
            for j in range(0, ufl_instance.get_n_of_facility()):
                if [i, j] in tight_arch:
                    b[i][j] += delta
        if output:
            print("a = ", a)
            print("b = ")
            for row in b:
                print("[", [i for i in row], "]")
        # verifico la presenza di nuovi archi tight a seguito dell'incremento e
        # ne aggiungo i nuovi all'insieme tight_arch
        new_tight_arch = check_new_tight_arch(a, b, ufl_instance, tight_arch)
        for arch in new_tight_arch:
            tight_arch.append(arch)
        # verifico se a seguito dell'incremento sono state ' aperte temporaneamente ' delle nuove facility
        # e le aggiungo all'insieme opened_facility e assigned
        opened = check_opened_facility(b, opened_facility, ufl_instance)
        for temp_fac in opened:
            opened_facility.append(temp_fac)
            assigned[temp_fac] = []
        if output:
            print("Tight arch = ", tight_arch)
        if output:
            print("Opened = ", opened)
        # vengono assegnati ad ogni nuova facility aperta tutti quei clienti
        # non ancora collocati che vi hanno un arco tight
        for facility in opened:
            assigned_client = check_tight_facility(facility, assigned, tight_arch)
            for client in assigned_client:
                assigned[facility].append(client)
                active_a[client] = False
                for j in range(0, ufl_instance.get_n_of_facility()):
                    active_b[client][j] = False
        # vengono assegnati ad ogni facility aperta tutti quei clienti
        # non ancora collocati che vi hanno un arco tight
        for facility in opened_facility:
            assigned_client = check_tight_facility(facility, assigned, tight_arch)
            for client in assigned_client:
                assigned[facility].append(client)
                active_a[client] = False
                for j in range(0, ufl_instance.get_n_of_facility()):
                    active_b[client][j] = False
        # la presenza di un nuovo arco tight indica che un vincolo Aj - Bij <= Dij è soddisfatto all'uguaglianza
        # occorre attivare l'incremento delle variabili Bij per contrastare quello delle variabili Aj
        for arch in new_tight_arch:
            if not client_assigned(arch[0], assigned):
                active_b[arch[0]][arch[1]] = True
        if output:
            print("Opened facility ", opened_facility, "\nAssignment = ", assigned)
            print("Active a =", active_a)
            print("Active b = ")
            for row in active_b:
                print(row)
            print("z = ", int(sum(a[0:len(a)])))
    print("### Primal - Dual SOLUTION ###")
    print("Dual solution : Z = ", float(sum(a[0:len(a)])))
    if primal:
        # Se richiesto viene calcolato il valore della soluzione primale
        primal_value = compute_primal_solution(opened_facility, b, ufl_instance, assigned, tight_arch)
        return [float(sum(a[0:len(a)])), primal_value]
    return float(sum(a[0:len(a)]))


# Verifica se un cliente non assegnato ha archi tight nei confronti di una particolare facility
def check_tight_facility(facility, assigned, tight_arch):
    tight_client = []
    for arch in tight_arch:
        if arch[1] != facility:
            continue
        if not client_assigned(arch[0], assigned):
            tight_client.append(arch[0])
    return tight_client


# ritorna True se un cliente è già stato assegnato False altrimenti
def client_assigned(client, assigned):
    for key in assigned:
        if client in assigned[key]:
            return True
    return False


# Calcola il valore della soluzione primale relativa ad un'esecuzione dell'algoritmo Primale - Duale
def compute_primal_solution(opened_facility, b, ufl_instance, assigned, tight_arch):
    x = [[0 for i in range(0, ufl_instance.get_n_of_facility())] for j in range(0, ufl_instance.get_n_of_client())]
    # print(opened_facility)
    closed = {}
    assigned_bis = {}
    for elem in assigned:
        assigned_bis[elem] = []
        for i in assigned[elem]:
            assigned_bis[elem].append(i)
    # per ogni coppia di facility temporaneamente aperte verifico se esistono dei conflitti
    # i conflitti sono risolti chiudendo la facility aperta per seconda in ordine di tempo
    for elem in opened_facility:
        conflict = False
        for i in assigned[elem]:
            for j in range(0, ufl_instance.get_n_of_facility()):
                if b[i][j] != Fraction(0, 1) and j != elem and j in opened_facility:
                    # print("CONFLITTO TRA FACILITY ", elem, " E ", j, "
                    # per il cliente ", i, " b[{0}{1}] = {2} b[{3}{4}] = {5}".format(i,j,b[i][j],i,elem,b[i][elem]))
                    opened_facility.remove(j)
                    indirect_client = assigned[j]
                    del assigned[j]
                    del assigned_bis[j]
                    closed[elem] = indirect_client
                    # assegno i cienti della facility chiusa a quella che ha vinto il conflitto
                    assigned_bis[elem] += indirect_client
                    conflict = True
                    break
            if conflict:
                break
    # sono possibili due opzioni per assegnare i clienti delle facility chiuse

    # 1) assegnare i clienti alle facility aperte verso cui hanno un arco tight
    for elem in closed:
        for client in closed[elem]:
            for j in opened_facility:
                if [client, j] in tight_arch:
                    assigned[j].append(client)
                    closed[elem].remove(client)
                    break
    # i clienti che non hanno alcun arco tight verso le facility rimaste vengono assegnati alle
    # facility responsabili della chiusura della facility a cui erano assegnati
    for elem in closed:
        for client in closed[elem]:
            assigned[elem].append(client)
    z = 0
    for facility in assigned:
        z += ufl_instance.get_opening_cost()[facility]
        for client in assigned[facility]:
            x[client][facility] = 1
            z += ufl_instance.get_transporting_cost()[client][facility]
    # 2) Assegnare i clienti alle facility responsabili della chiusura della facility a cui erano assegnati
    z2 = 0
    x = [[0 for i in range(0, ufl_instance.get_n_of_facility())] for j in range(0, ufl_instance.get_n_of_client())]
    for facility in assigned_bis:
        z2 += ufl_instance.get_opening_cost()[facility]
        for client in assigned_bis[facility]:
            x[client][facility] = 1
            z2 += ufl_instance.get_transporting_cost()[client][facility]
    print("Primal solution : Z = ", min(z, z2))
    # viene restituito il valore minore tra le due alternative calcolate
    return min(z, z2)


# Verifica se per una soluzione corrente sono presenti nuovi archi tight
# ovvero se ci sono {i,j] per cui il vincolo Aj - Bij <= Dij è soddisfatto all'uguaglianza
def check_new_tight_arch(a, b, ufl_instance, tight_arch):
    tight_a = []
    for i in range(0, ufl_instance.get_n_of_client()):
        for j in range(0, ufl_instance.get_n_of_facility()):
            if ufl_instance.get_transporting_cost()[i][j] - a[i] + b[i][j] == 0 and [i, j] not in tight_arch:
                tight_a.append([i, j])
    return tight_a


# Verifica se per una soluzione corrente possono esseere aperte temporaneamente delle nuove facility
# ovvero se ci sono facility i per cui il vincolo sum{j in clienti}BiJ <= fi è soddisfatto all'uguaglianza
def check_opened_facility(b, opened_facility, ufl_instance):
    opened = []
    for j in range(0, ufl_instance.get_n_of_facility()):
        summation = 0
        if j in opened_facility:
            continue
        for i in range(0, ufl_instance.get_n_of_client()):
            summation += b[i][j]
        if ufl_instance.get_opening_cost()[j] == summation:
            opened.append(j)
    return opened


# calcolo del valore di incremento per una particolare iterazione dell'algoritmo
def compute_delta(a, b, ufl_instance, active_b, opened_facility, tight_arch):
    # il valore dell'incremento deve essere il minimo tra due valori delta_a e delta_b
    # delta_a è il massimo incremento possibile che consenta di mantenere rispettati i vincoli
    # del tipo Aj - Bij <= Dij (non tight)
    # delta_b è il massimo incremento possibile che consenta di mantenere rispettati i vincoli
    # del tipo sum{j in clienti}Bij <= fi (per facility ancora non aperte)

    # Calcolo delta_a restituendo il minimo tra i valori delta che consentano di rispettare
    # ogni vintolo Aj - Bij <= Dij (non tight)
    delta_a_vector = []
    for i in range(0, ufl_instance.get_n_of_client()):
        for j in range(0, ufl_instance.get_n_of_facility()):
            if [i, j] in tight_arch:
                continue
            delta_tmp = ufl_instance.get_transporting_cost()[i][j] - a[i] + b[i][j]
            delta_a_vector.append(delta_tmp)
    if len(delta_a_vector) == 0:
        delta_a = 0
    else:
        delta_a = Fraction(Fraction(min(delta_a_vector)), 1)

    # Calcolo delta_b restituendo il minimo tra i valori delta che consentano di rispettare
    # ogni vintolo sum{j in clienti}Bij <= fi (per facility ancora non aperte)
    delta_b_vector = []
    for j in range(0, ufl_instance.get_n_of_facility()):
        if j in opened_facility:
            continue
        summation = 0
        den_tmp = 0
        for i in range(0, ufl_instance.get_n_of_client()):
            summation += b[i][j]
            if active_b[i][j]:
                den_tmp += 1
        if den_tmp == 0:
            continue
        delta_b_vector.append(Fraction(Fraction(ufl_instance.get_opening_cost()[j] - summation), den_tmp))
    # Alla fine viene restituito il minimo valore tra delta_a e delta_b
    if len(delta_b_vector) == 0:
        delta_b = None
    else:
        delta_b = min(delta_b_vector)
    if delta_b is not None:
        if delta_b == 0:
            return delta_a
        elif delta_a == 0:
            return delta_b
        return min(delta_a, delta_b)
    return delta_a
