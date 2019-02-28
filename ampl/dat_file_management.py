from amplpy import DataFrame

# Formatta un oggetto sscfl_instance in un oggetto DataFrame per l'esecuzione del solver AMPL
def write_ampl_sscfl_dat_file(ampl, sscfl_instance):
    facility_set = []
    client_set = []
    for i in range(0, sscfl_instance.get_n_of_facility()):
        facility_set.append(i)
    for i in range(0, sscfl_instance.get_n_of_client()):
        client_set.append(i)
    df = DataFrame('facility')
    df.setColumn('facility', facility_set)
    df.addColumn('F', sscfl_instance.get_opening_cost())
    df.addColumn('Q', sscfl_instance.get_capacity())
    ampl.setData(df, 'facility')
    df = DataFrame('client')
    df.setColumn('client', client_set)
    df.addColumn('W', sscfl_instance.get_demand())
    ampl.setData(df, 'client')
    df = DataFrame(('client', 'facility'), 'C')
    df.setValues({
        (client, facility): sscfl_instance.get_transporting_cost()[i][j]
        for i, client in enumerate(client_set)
        for j, facility in enumerate(facility_set)
    })
    ampl.setData(df)
    return ampl


# Formatta un oggetto ufl_instance in un oggetto DataFrame per l'esecuzione del solver AMPL
def write_ampl_ufl_dat_file(ampl, ufl_instance):
    facility_set = []
    client_set = []
    for i in range(0, ufl_instance.get_n_of_facility()):
        facility_set.append(i)
    for i in range(0, ufl_instance.get_n_of_client()):
        client_set.append(i)
    df = DataFrame('facility')
    df.setColumn('facility', facility_set)
    df.addColumn('F', ufl_instance.get_opening_cost())
    ampl.setData(df, 'facility')
    df = DataFrame('client')
    df.setColumn('client', client_set)
    ampl.setData(df, 'client')
    df = DataFrame(('client', 'facility'), 'C')
    df.setValues({
        (client, facility): ufl_instance.get_transporting_cost()[i][j]
        for i, client in enumerate(client_set)
        for j, facility in enumerate(facility_set)
    })
    ampl.setData(df)
    return ampl
