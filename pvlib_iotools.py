import pandas as pd
import pvlib

poa_data_2020, meta = pvlib.iotools.get_pvgis_hourly(
    latitude=41.662,
    longitude=-83.612,
    start='2020',
    end='2020',
   raddatabase="PVGIS-ERA5", components=True,
   surface_tilt=45,
    surface_azimuth=0,
    outputformat='csv',
    usehorizon=True, 
    userhorizon=None,
    pvcalculation=False,
    peakpower=None,
    pvtechchoice="crystSi",
    mountingplace="free",
    loss=0,
    trackingtype=0,
    optimal_surface_tilt=False,
    optimalangles=False,
    url="https://re.jrc.ec.europa.eu/api/v5_2/",
    map_variables=True,
    timeout=30
)

poa_data_2020['poa_diffuse'] = poa_data_2020["poa_sky_diffuse"] + poa_data_2020["poa_ground_diffuse"]
poa_data_2020["poa_global"] = poa_data_2020["poa_diffuse"] + poa_data_2020["poa_direct"]

print(poa_data_2020)
poa_data_2020.to_csv("poa_data_2020.csv")
