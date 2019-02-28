# DUALOC
def dualoc(ufl_instance, output, primal):
    completed = [False]*ufl_instance.get_n_of_client()
    if output:
        print("Fu = ", ufl_instance.get_opening_cost())
        print("C = ")
        for row in ufl_instance.get_transporting_cost():
            print(row)
    # Viene inizializzato il vettore z : Zv = min(Cuv)
    z = []
    for i in range(0, ufl_instance.get_n_of_client()):
        z.append(min(ufl_instance.get_transporting_cost()[i]))
    if output:
        print("z(0) = ", z)
    step = 0
    # Ripeti finchè è possibile calcolare un incremento strettamento positivo per qualche variabile Zv
    while False in completed:
        v_set = initialize_v_set(completed)
        # Ripeti finchè V non è vuoto
        while len(v_set) != 0:
            step = step + 1
            # h_min_v =  v tale che rende minimo h(v) dove h(v) = |{u : Zv - Cuv >= 0}|
            h_min_v = compute_h_index(z, ufl_instance.get_transporting_cost(), completed, v_set)
            if output:
                print("\n\n### STEP :", step, " ###\n")
                print("V = ", v_set)
                print("argmin{h(v)} = ", h_min_v)
            v_set.remove(h_min_v)
            # 𝑏𝑣'= 𝑚𝑖𝑛{𝑏𝑣,𝑚𝑖𝑛 su 𝑢∈𝑈 e 𝑐𝑢𝑣−𝑧𝑣 >0 di {𝑐𝑢𝑣− 𝑧𝑣} };
            # dove 𝑏𝑣= 𝑚𝑖𝑛𝑢∈𝑈{𝑐𝑢𝑣+ 𝜏𝑣𝑢− 𝑧𝑣};
            # e 𝜏𝑣𝑢= 𝑓𝑢− Σ𝑚𝑎𝑥{0,𝑧𝑣− 𝑐𝑢𝑣};
            block_value = compute_block_value(ufl_instance, h_min_v, z, output)
            # Se il valore di blocco calcolato è 0 allora il cliente v è marcato come 'completato' e non sarà
            # più esaminato dalle prossime iterazioni
            if block_value == 0:
                completed[h_min_v] = True
            z[h_min_v] += block_value
            if output:
                print("z({0}) = ".format(step), z)
    print("### DUALOC SOLUTION ###\nZ = ", sum(z[0:len(z)]))
    if primal:
        # in caso si richieda il calcolo della soluzione primale
        primal_value = compute_primal_solution(z, ufl_instance)
        print("PRIMAL SOLUTION : ", primal_value)
        return [sum(z[0:len(z)]), primal_value]
    return sum(z[0:len(z)])


# calcola  𝑏𝑣'= 𝑚𝑖𝑛{𝑏𝑣,𝑚𝑖𝑛 su 𝑢∈𝑈 e 𝑐𝑢𝑣−𝑧𝑣 >0 di {𝑐𝑢𝑣− 𝑧𝑣} };
# dove 𝑏𝑣= 𝑚𝑖𝑛𝑢∈𝑈{𝑐𝑢𝑣+ 𝜏𝑣𝑢− 𝑧𝑣};
# e 𝜏𝑣𝑢= 𝑓𝑢− Σ𝑚𝑎𝑥{0,𝑧𝑣− 𝑐𝑢𝑣};
def compute_block_value(ufl_instance, h_min_v, z, output):
    bv_vector = []
    bv_star_vector = []
    for i in range(0, ufl_instance.get_n_of_facility()):
        summation = 0
        for j in range(0, ufl_instance.get_n_of_client()):
            if j == h_min_v:
                continue
            # summation rappresenta il termine Σ𝑚𝑎𝑥{0,𝑧𝑣− 𝑐𝑢𝑣}
            summation += max(0, z[j] - ufl_instance.get_transporting_cost()[j][i])
        # 𝜏𝑣𝑢= 𝑓𝑢− Σ𝑚𝑎𝑥{0,𝑧𝑣− 𝑐𝑢𝑣};
        tvu = ufl_instance.get_opening_cost()[i] - summation
        # viene inserito in un vettore il valore 𝑏𝑣u= {𝑐𝑢𝑣+ 𝜏𝑣𝑢− 𝑧𝑣} calcolato per una facility
        bv_vector.append(ufl_instance.get_transporting_cost()[h_min_v][i] + tvu - z[h_min_v])
        if output:
            print("Tvu({0}{1}) = {2} (Fu) - {3} (SUM(max[0,Zv-Cvu])  = {4}\n".format(h_min_v, i,
                                                                                     ufl_instance.get_opening_cost()[
                                                                                         i], summation, tvu))
            print("B({0}) = ( {1} (Cvu) + {2} (Tvu) - {3} (Zv)) = {4}\n".format(i, ufl_instance.get_transporting_cost()[
                h_min_v][i], tvu, z[h_min_v], bv_vector[i]))
        # Cuv - Zv > 0 è inserito in un vettore anche il valore Cuv - Zv
        if ufl_instance.get_transporting_cost()[h_min_v][i] - z[h_min_v] > 0:
            bv_star_vector.append(ufl_instance.get_transporting_cost()[h_min_v][i] - z[h_min_v])
    # 𝑏𝑣= 𝑚𝑖𝑛𝑢∈𝑈{𝑐𝑢𝑣+ 𝜏𝑣𝑢− 𝑧𝑣};
    bv = min(bv_vector)
    if output:
        print("bv_vector = ", bv_vector)
        print("bv_star_vector = ", bv_star_vector)
        print("bv = ", bv)
    # se è stato possibile calcolare un valore positivo Cuv - Zv
    if len(bv_star_vector) > 0:
        # si estrae 𝑚𝑖𝑛 su 𝑢∈𝑈 e 𝑐𝑢𝑣−𝑧𝑣 >0 di {𝑐𝑢𝑣− 𝑧𝑣}
        bv_star = min(bv_star_vector)
        # e si restituisce come valore di blocco
        # 𝑏𝑣'= 𝑚𝑖𝑛{𝑏𝑣,𝑚𝑖𝑛 su 𝑢∈𝑈 e 𝑐𝑢𝑣−𝑧𝑣 >0 di {𝑐𝑢𝑣− 𝑧𝑣} };
        block_value = min(bv, bv_star)
    else:
        bv_star = None
        # altrimenti il valore di blocco è banalmente uguale a
        # 𝑏𝑣= 𝑚𝑖𝑛𝑢∈𝑈{𝑐𝑢𝑣+ 𝜏𝑣𝑢− 𝑧𝑣};
        block_value = bv
    if output:
        print("bv' = min[{0},{1}] = {2}".format(bv, bv_star, block_value))
    return block_value


# Calcolo euristico della soluzione primale partendo da una soluzione duale del DUALOC
def compute_primal_solution(z, ufl_instance):
    # Calcolo della matrice W le cui componenti assumono il valore delle variabili Wuv del problema risolto dal DUALOC
    w_matrix = []
    for i in range(0, ufl_instance.get_n_of_client()):
        vector = []
        for j in range(0, ufl_instance.get_n_of_facility()):
            vector.append(max(0, z[i]-ufl_instance.get_transporting_cost()[i][j]))
        w_matrix.append(vector)
    # Sono considerate candidate all'apertura le facility per cui fu = sum{v in V}Wuv
    u_set = []
    for j in range(0, ufl_instance.get_n_of_facility()):
        summation = 0
        for i in range(0, ufl_instance.get_n_of_client()):
            summation += w_matrix[i][j]
        if summation == ufl_instance.get_opening_cost()[j]:
            u_set.append(j)
    # Calcolo della matrice di connessione Y le cui componenti Yuv assumono valore 1 se Cvu = min(u in U){Cvu}
    y_matrix = [[0 for i in range(0, ufl_instance.get_n_of_facility())]
                for j in range(0, ufl_instance.get_n_of_client())]
    for i in range(0, ufl_instance.get_n_of_client()):
        minimum = ufl_instance.get_transporting_cost()[i][u_set[0]]
        min_j = u_set[0]
        for j in u_set:
            if minimum > ufl_instance.get_transporting_cost()[i][j]:
                minimum = ufl_instance.get_transporting_cost()[i][j]
                min_j = j
        y_matrix[i][min_j] = 1
    u_final_set = []
    z_value = 0
    # Delle facility candidate all'apertura sono chiuse tutte quelle che non hanno alcuna connessione  nella matrice Y
    for i in range(0, ufl_instance.get_n_of_client()):
        for j in range(0, ufl_instance.get_n_of_facility()):
            if y_matrix[i][j] == 1:
                if j not in u_final_set:
                    u_final_set.append(j)
                    z_value += ufl_instance.get_opening_cost()[j]
                z_value += ufl_instance.get_transporting_cost()[i][j]
    print("Z = ", z_value)
    # Viene restituito il valore della soluzione primale tenendo conto delle facility definitivamente aperte
    # e delle scelte di connessione rappresentate dalla matrice Y
    return z_value


# calcola h_min_v =  v tale che rende minimo h(v) dove h(v) = |{u : Zv - Cuv >= 0}|
def compute_h_index(z, transporting_cost, completed, v_set):
    h_vector = []
    for i in range(0, len(z)):
        hv = 0
        if completed[i] or i not in v_set:
            h_vector += [len(transporting_cost[0])+1]
            continue
        for c in transporting_cost[i]:
            if z[i] >= c:
                hv += 1
        h_vector += [hv]
    return h_vector.index(min(h_vector))


# Inizializzaione dell'insieme V di ogni iterazione considerando solo i clienti
# che non sono stati marcati come completati
def initialize_v_set(completed):
    v_set = []
    for i in range(0, len(completed)):
        if not completed[i]:
            v_set += [i]
    return v_set
