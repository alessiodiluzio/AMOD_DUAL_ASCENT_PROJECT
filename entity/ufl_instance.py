# Rappresenta un'istanza di ufl_instance_generator per un problema di UFL
class UflInstance(object):

    def __init__(self, transporting_cost, opening_cost):
        self._transporting_cost = transporting_cost
        self._opening_cost = opening_cost

    def get_transporting_cost(self):
        return self._transporting_cost

    def get_opening_cost(self):
        return self._opening_cost

    def get_n_of_client(self):
        return len(self._transporting_cost)

    def get_n_of_facility(self):
        return len(self._opening_cost)

    def set_transporting_cost(self, transporting_cost):
        self._transporting_cost = transporting_cost
