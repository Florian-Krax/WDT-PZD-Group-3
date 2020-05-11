# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %% [markdown]
# # Die Corona Lage 
# %% [markdown]
# ## Daten URLs

# %%
URL_CORONA_INFECTED = r"https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv"
URL_CORONA_RECOVER = r"https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv"
URL_CORONA_DEATHS = r"https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv"

# %% [markdown]
# ## Umsetzung
# %% [markdown]
# ### Import

# %%
import pandas
import datetime
import numpy as np
import matplotlib.pyplot as plt

# %% [markdown]
# ### Herunterladen der Daten von Github

# %%
infected = pandas.read_csv(URL_CORONA_INFECTED)
recovered = pandas.read_csv(URL_CORONA_RECOVER)
death = pandas.read_csv(URL_CORONA_DEATHS)


# %%


