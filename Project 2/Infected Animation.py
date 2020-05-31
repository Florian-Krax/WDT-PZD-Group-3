from itertools import count
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
#from matplotlib import animation

#Pyplot Animation nicht die beste Methode (Geopandas, Cartopy)

URL_CORONA_INFECTED = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/" + \
                      "csse_covid_19_data/csse_covid_19_time_series/" + \
                      "time_series_covid19_confirmed_global.csv"

inf = pd.read_csv(URL_CORONA_INFECTED)
col = list(inf.columns.values)

index = count(start=4)
inf = inf.groupby(["Country/Region"]).mean() 
x = inf[col[3]]
y = inf[col[2]]
sc = plt.scatter(x,y,c="red", s=10, label="Infected", zorder=1)

img = plt.imread("weltkarteV4.png")
plt.imshow(img, extent=[-150,190,-60,100], zorder=0)
plt.tight_layout()
plt.legend(loc = "upper right")

def animate(i):
     if(next(index) < len(col)):
         maxWert = max(inf[col[next(index)]])
         minWert = min(inf[col[next(index)]])
         size = (inf[col[next(index)]] - minWert) / (maxWert - minWert)
         sc.set_sizes(np.array(size*100))
        
ani = FuncAnimation(plt.gcf(), animate, frames=30, interval=200)
#writer = animation.FFMpegWriter(fps=200, metadata = dict(artist='Me'), bitrate=1800)

plt.tight_layout()
plt.show()
#ani.save("Coronaverlauf.mp4", writer = writer)