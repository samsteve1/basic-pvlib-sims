import pvlib
import pandas as pd
import matplotlib.pyplot as plt
from main import location, poa_data_2020
from pvlib.location import Location
from pvlib.modelchain import ModelChain

celltype = "monosi"
pdc0 = 400
v_mp = 44.1
i_mp = 9.08
v_oc = 53.4
i_sc = 9.60
alpha_sc = 0.0005 * i_mp
beta_pdc = -0.0029 * v_mp
gamma_pdc = - 0.0037
cells_in_series = 6*27
temp_ref = 25

location = Location(latitude=41.662, longitude=-83.612, tz='America/Detroit', altitude=187, name='McMaster')

surface_tilt = 45
surface_azimuth = 180

start = "2020-07-01 00:00"
end = "2020-07-07 23:00"

poa_data_2020 = pd.read_csv("poa_data_2020.csv", index_col=0)
poa_data_2020.index = pd.date_range(start="2020-01-01 00:00", periods=len(poa_data_2020.index), freq="h")
poa_data = poa_data_2020[start:end]

solar_position = location.get_solarposition(times = pd.date_range(start=start, end=end, freq = "h"))

aoi = pvlib.irradiance.aoi(
    surface_tilt=surface_tilt, 
    surface_azimuth=surface_azimuth, 
    solar_zenith=solar_position.apparent_zenith, 
    solar_azimuth=solar_position.azimuth
)

iam = pvlib.iam.ashrae(aoi)

effective_irradiance = poa_data["poa_direct"] * iam + poa_data["poa_diffuse"]

temp_cell = pvlib.temperature.faiman(poa_data["poa_global"], poa_data["temp_air"], poa_data["wind_speed"])

result_dc = pvlib.pvsystem.pvwatts_dc(
    effective_irradiance,
    temp_cell,
    pdc0,
    gamma_pdc,
    temp_ref=25
)

result_dc.plot()
plt.title('Custom DC Power Output')
plt.xlabel('Time')
plt.ylabel('Power (W)')
plt.savefig('custom_dc_power_output.png')
plt.close()

result_ac = pvlib.pvsystem.inverter.pvwatts(
    pdc=result_dc,
    pdc0=200, # inverted max power
    eta_inv_nom=0.96,
    eta_inv_ref=0.96,
)

result_ac.plot()
plt.title('Custom AC Power Output')
plt.xlabel('Time')
plt.ylabel('Power (W)')
plt.savefig('custom_ac_power_output.png')
plt.close()