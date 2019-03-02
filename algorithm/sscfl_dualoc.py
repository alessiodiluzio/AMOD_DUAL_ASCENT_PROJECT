from fractions import Fraction
from algorithm.ufl_dualoc import compute_h_index


# DUALOC adattato a istanze di SSCFL
# sscfl_istanza : oggetto che rappresenta l'istanza di ufl_instance_generator
# output : True se si richiede la stampa dei calcoli dell'algoritmo False altrimenti
def sscfl_dualoc(sscfl_instance, output):
    completed = [False] * sscfl_instance.get_n_of_client()
    if output:
        pass
    # Viene inizializzato il vettore z : Zv = min(Cuv)
    z = []
    for i in range(0, sscfl_instance.get_n_of_client()):
        z += [min(sscfl_instance.get_transporting_cost()[i])]
    if output:
        print("z(0) = ", z)
    step = 0
    # Insieme dei clienti V dell'istanza
    v_set = [i for i in range(0, sscfl_instance.get_n_of_client())]
    # Ripeti per ogni v in V
    while len(v_set) != 0:
        step = step + 1
        # h_min_v =  v tale che rende minimo h(v) dove h(v) = |{u : Zv - Cuv >= 0}|
        h_min_v = compute_h_index(z, sscfl_instance.get_transporting_cost(), completed, v_set)
        if output:
            print("\n\n### STEP :", step, " ###\n")
        v_set.remove(h_min_v)
        # 𝑏𝑣=𝑚𝑖𝑛 𝑢∈𝑈{𝑞𝑢/𝑑𝑣∗𝑓𝑢 − Z𝑣+ C𝑢𝑣};
        block_value = compute_delta(z[h_min_v], sscfl_instance, h_min_v)
        if block_value < 0:
            continue
        # incremento della variabile Z esaminata nell'iterazione corrente
        z[h_min_v] += block_value
    print("### DUALOC SOLUTION ###\nZ = ", float(sum(z[0:len(z)])))
    return float(sum(z[0:len(z)]))


# calcola il valore di blocco (incremento) di una specifica iterazione dell'algoritmo
# 𝑏𝑣=𝑚𝑖𝑛 𝑢∈𝑈{𝑞𝑢/𝑑𝑣∗𝑓𝑢 − Z𝑣+ C𝑢𝑣};
def compute_delta(zv, sscfl_instance, h_min_v):
    c = sscfl_instance.get_transporting_cost()
    f = sscfl_instance.get_opening_cost()
    q = sscfl_instance.get_capacity()
    d = sscfl_instance.get_demand()
    delta_vector = []
    for u in range(0, sscfl_instance.get_n_of_facility()):
        # per ogni facility u calcolo il valore
        # 𝑏𝑣u={𝑞𝑢/𝑑𝑣∗𝑓𝑢 − Z𝑣+ C𝑢𝑣};
        delta_tmp = Fraction(d[h_min_v] * f[u], q[u]) + c[h_min_v][u] - zv
        delta_vector.append(delta_tmp)
    # restituisco il minimo tra i valori calcolati
    return min(delta_vector)
