# algoritmo di Ascesa Duale 'semplice'
def simple_dualoc(ufl_instance, output):
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
    v_set = [i for i in range(0, ufl_instance.get_n_of_client())]
    # Ripeti per ogni v in V
    for v in v_set:
        step = step + 1
        if output:
            print("\n\n### STEP :", step, " ###\n")
        # 𝑏𝑣= 𝑚𝑖𝑛𝑢∈𝑈{𝑐𝑢𝑣+ 𝜏𝑣𝑢− 𝑧𝑣} dove 𝜏𝑣𝑢= 𝑓𝑢− Σ𝑚𝑎𝑥{0,𝑧𝑣− 𝑐𝑢𝑣};
        block_value = compute_block_value(ufl_instance, v, z, output)
        # incremento della variabile Z esaminata nell'iterazione corrente
        z[v] += block_value
        if output:
            print("z({0}) = ".format(step), z)
    print("### SIMPLE DUALOC SOLUTION ###\nZ = ", sum(z[0:len(z)]))
    if output:
        print("Zv = ", z)
    return sum(z[0:len(z)])


# calcola il valore di blocco (incremento) di una specifica iterazione dell'algoritmo
# 𝑏𝑣= 𝑚𝑖𝑛𝑢∈𝑈{𝑐𝑢𝑣+ 𝜏𝑣𝑢− 𝑧𝑣} dove 𝜏𝑣𝑢= 𝑓𝑢− Σ𝑚𝑎𝑥{0,𝑧𝑣− 𝑐𝑢𝑣};
def compute_block_value(ufl_instance, v, z, output):
    bv_vector = []
    for i in range(0, ufl_instance.get_n_of_facility()):
        summation = 0
        for j in range(0, ufl_instance.get_n_of_client()):
            if j == v:
                continue
            # summation rappresenta il termine Σ𝑚𝑎𝑥{0,𝑧𝑣− 𝑐𝑢𝑣}
            summation += max(0, z[j] - ufl_instance.get_transporting_cost()[j][i])
        # 𝜏𝑣𝑢= 𝑓𝑢− Σ𝑚𝑎𝑥{0,𝑧𝑣− 𝑐𝑢𝑣};
        tvu = ufl_instance.get_opening_cost()[i] - summation
        # viene inserito in un vettore il valore 𝑏𝑣u= {𝑐𝑢𝑣+ 𝜏𝑣𝑢− 𝑧𝑣} calcolato per una facility
        bv_vector.append(ufl_instance.get_transporting_cost()[v][i] + tvu - z[v])
        if output:
            print("Tvu({0}{1}) = {2} (Fu) - {3} (SUM(max[0,Zv-Cvu])  = {4}\n".format(v, i,
                                                                                     ufl_instance.get_opening_cost()[i],
                                                                                     summation, tvu))
            print("B({0}) = ( {1} (Cvu) + {2} (Tvu) - {3} (Zv)) = {4}\n".format(i, ufl_instance.get_transporting_cost()[
                v][i], tvu, z[v], bv_vector[i]))
    if output:
        print("bv = ", min(bv_vector))
    # viene restituito il minimo del vettore bv_vector che corrisponde a
    # b𝑣= 𝑚𝑖𝑛𝑢∈𝑈{𝑐𝑢𝑣+ 𝜏𝑣𝑢− 𝑧𝑣}
    return min(bv_vector)
