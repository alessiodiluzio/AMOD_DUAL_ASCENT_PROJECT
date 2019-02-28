from amplpy import AMPL, Environment

from ampl.dat_file_management import write_ampl_ufl_dat_file, write_ampl_sscfl_dat_file


# Usande le API ampl utilizza il solver cplex per la risolluzione di un problema di UFL
# mod_file : Path al file .mod del problema
# ufl_istance : oggetto che rappresenta l'istanza da risolvere
# ampl_folder : Path alla directory di installazione del software AMPL
def solve_ufl_instance(mod_file, ufl_instance, ampl_folder):
    print('### AMPL SOLUTION ###')
    if ampl_folder is None:
        primal_pl = AMPL()
    else:
        primal_pl = AMPL(Environment(ampl_folder))
    primal_pl.read('ampl_mod_files/'+mod_file)
    primal_pl.setOption('solver_msg', 0)
    primal_pl.setOption('solver', 'cplex')
    primal_pl = write_ampl_ufl_dat_file(primal_pl, ufl_instance)
    primal_pl.solve()
    f = primal_pl.getObjective('f')
    print("\nZ = ", f.value())
    return f.value()


# Usande le API ampl utilizza il solver cplex per la risolluzione di un problema di SSCFL
# mod_file : Path al file .mod del problema
# sscfl_istance : oggetto che rappresenta l'istanza da risolvere
# ampl_folder : Path alla directory di installazione del software AMPL
def solve_sscfl_instance(mod_file, sscfl_instance, ampl_folder):
    print('### AMPL SOLUTION ###')
    if ampl_folder is None:
        primal_pl = AMPL()
    else:
        primal_pl = AMPL(Environment(ampl_folder))
    primal_pl.read('ampl_mod_files/'+mod_file)
    primal_pl.setOption('solver', 'cplex')
    primal_pl = write_ampl_sscfl_dat_file(primal_pl, sscfl_instance)
    primal_pl.solve()
    f = primal_pl.getObjective('f')
    print('\nZ = ', '%.5f' % (f.value()))
    return f.value()
