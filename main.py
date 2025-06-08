import pvlib
import pandas as pd
import matplotlib.pyplot as plt
from pvlib.modelchain import ModelChain
from pvlib.location import Location
from pvlib.pvsystem import PVSystem

location = Location(latitude=32.2, longitude=-111, tz='America/Detroit', altitude=700, name='Tucson')
sandia_modules = pvlib.pvsystem.retrieve_sam('SandiaMod')
cec_inverters = pvlib.pvsystem.retrieve_sam('CECInverter')

module = sandia_modules['Canadian_Solar_CS5P_220M___2009_']
inverter = cec_inverters['ABB__MICRO_0_25_I_OUTD_US_208__208V_']
temperature_model_parameters = pvlib.temperature.TEMPERATURE_MODEL_PARAMETERS['sapm']['open_rack_glass_glass']


system = PVSystem(
    surface_tilt=45, 
    surface_azimuth=180, 
    module_parameters=module,
    inverter_parameters=inverter,
    temperature_model_parameters=temperature_model_parameters, 
    modules_per_string=1,
    strings_per_inverter=1
    )

modelChain = ModelChain(system, location, name="Tucson")

times = pd.date_range(start='2020-06-01', end='2020-06-07', freq='1min', tz=location.tz)

clear_sky_data = location.get_clearsky(times)

clear_sky_data.plot()
plt.title('Clear Sky Data')
plt.xlabel('Time')
plt.ylabel('Irradiance (W/m^2)')
plt.savefig('clear_sky_data.png')
plt.close()

modelChain.run_model(clear_sky_data)

modelChain.results.ac.plot()
plt.title('AC Power Output')
plt.xlabel('Time')
plt.ylabel('Power (W)')
plt.savefig('ac_power_output.png')
plt.close()

modelChain.results.dc.plot()
plt.title('DC Power Output')
plt.xlabel('Time')
plt.ylabel('Power (W)')
plt.savefig('dc_power_output.png')
plt.close()

max_module_power = module.Impo * module.Vmpo * 1 * 1 # modules_per_string * strings_per_inverter
inverter_capacity = inverter.Paco
inverter_capacity_dc = inverter.Pdco

print(f"Max Module Power: {max_module_power} W")
print(f"Inverter AC Capacity: {inverter_capacity} W")
print(f"Inverter DC Capacity: {inverter_capacity_dc} W")
print(f"AC Power Output Stats:\n{modelChain.results.ac.describe()}")
