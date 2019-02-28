# Rappresenta un'istanza di test per un problema di SSCFL
class SscflInstance(object):

    def __init__(self, transporting_cost, opening_cost, demand, capacity):
        self._transporting_cost = transporting_cost
        self._opening_cost = opening_cost
        self._demand = demand
        self._capacity = capacity

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

    def get_demand(self):
        return self._demand

    def get_capacity(self):
        return self._capacity
