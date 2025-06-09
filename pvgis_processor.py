import pandas as pd

tmy = pd.read_csv(
    "tmy_data_mcmaster.csv", 
    skiprows=17, 
    nrows=8760, 
    usecols=["time(UTC)", "T2m", "G(h)", "Gb(n)", "Gd(h)", "WS10m"], 
    index_col=0
    )

tmy.index = pd.date_range("2021-01-01 00:00", "2021-12-31 23:00", freq="h")
tmy.columns = ["temp_air", "ghi", "dni", "dhi", "wind_speed"]

tmy.to_csv("tmy_data_mcmaster_clean.csv")
