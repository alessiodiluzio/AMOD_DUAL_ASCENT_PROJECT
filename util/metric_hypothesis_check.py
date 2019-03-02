# Verifica se un'istanza di UFL rispetta l'ipotesa metrica
def metric_hypothesis(ufl_instance):
    d = ufl_instance.get_transporting_cost()
    for i in range(0, ufl_instance.get_n_of_client()):
        for j in range(0, ufl_instance.get_n_of_facility()):
            for k in range(0, ufl_instance.get_n_of_facility()):
                for y in range(0, ufl_instance.get_n_of_client()):
                    delta = d[i][j] - (d[i][k] + d[y][k] + d[y][j])
                    if delta > 0:
                        return False
    return True


def metric_hypothesis_change(ufl_instance):
    d = ufl_instance.get_transporting_cost()
    metric = True
    count = 0
    for i in range(0, ufl_instance.get_n_of_client()):
        for j in range(0, ufl_instance.get_n_of_facility()):
            for k in range(0, ufl_instance.get_n_of_facility()):
                for y in range(0, ufl_instance.get_n_of_client()):
                    delta = d[i][j] - (d[i][k] + d[y][k] + d[y][j])
                    if delta > 0:
                        count += 1
                        d[i][j] -= delta
                        metric = False
    print(str(count) + " swap ")
    if metric:
        return ufl_instance
    else:
        ufl_instance.set_transporting_cost(d)
        return metric_hypothesis_change(ufl_instance)
