import pandas as pd

global_2020 = pd.read_csv("pvgis_2020_global.csv", skiprows=8, nrows=8784, index_col=0)
components_2020 =  pd.read_csv("pvgis_2020_components.csv", skiprows=8, nrows=8784, index_col=0)

poa_data_2020 = pd.DataFrame(columns=[
    'poa_global',
    'poa_direct',
    'poa_diffuse',
    'temp_air',
    'wind_speed'
], index=global_2020.index)

poa_data_2020['poa_global'] = global_2020['G(i)']
poa_data_2020['poa_direct'] = components_2020['Gb(i)']
poa_data_2020['poa_diffuse'] = components_2020['Gd(i)'] + components_2020['Gr(i)']
poa_data_2020['temp_air'] = components_2020['T2m']
poa_data_2020['wind_speed'] = components_2020['WS10m']


poa_data_2020.index = pd.to_datetime(poa_data_2020.index, format="%Y%m%d:%H%M")

poa_data_2020.to_csv("poa_data_2020.csv")
print(poa_data_2020)