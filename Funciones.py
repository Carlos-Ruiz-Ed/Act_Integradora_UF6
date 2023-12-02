def safety_lvl(data):

    #Obteneos que tantos crimenes hay en la zona
    crime_rate = len(data)
    crime_type = data['Incident Category'].nunique()

    #Asignamos una denominacon dependiendo de los indicadores
    if crime_rate >= 100 and crime_type >= 5:
        safety_level = 'High'
    elif crime_rate >= 50 or crime_type >= 3:
        safety_level = 'Medium'
    else:
        safety_level = 'Low'

    return safety_level

