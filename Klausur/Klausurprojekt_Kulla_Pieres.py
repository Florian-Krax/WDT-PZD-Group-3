"""

@authors: Armin Kulla, Hendrik Pieres

"""

import pandas as pd
import itertools
import numpy as np
import matplotlib.pyplot as plt
import re
from scipy import stats

pm = pd.read_csv("aap_air_quality_database_2018_v14.csv", skiprows=2, sep=";")
pd.options.display.max_columns = None

#Aufteilung in zwei unterschiedliche DataFrames
pm10 = pm.drop(columns=pm.iloc[:,8:11])
pm25 = pm.drop(columns=pm.iloc[:,5:8])

pm = pd.read_csv("aap_air_quality_database_2018_v14_pm10_latest.csv")
pm10_latest = pm.drop(columns = pm.iloc[:,8:11])

pm = pd.read_csv("aap_air_quality_database_2018_v14_pm25_latest.csv")
pm25_latest = pm.drop(columns = pm.iloc[:,5:8])

#data = {"PM10": pm10, "PM2.5": pm25}

#Feinstaub EU- & WHO-Grenzwert PM10 -> 40 Mikrorgamm pro Kubikmeter (Quelle: Umweltbundesamt)
#Feinstaub EU-Grenzwert PM2.5 -> 25 Mikrogramm pro Kubikmeter (Quelle: Umweltbundesamt)
#feststehende Grenzwerte 
plt.style.use("default")
plt.style.use("ggplot")

def zwischenlinie(length: int):
    r"""
    

    Parameters
    ----------
    length : int
        Wie viele Zeichen beinhalten die längste Werte in den jeweiligen Spalten zusammengerechnet.

    Returns
    -------
    None.

    """
    
    #Der Wert 10 ergibt sich aus den Leerzeichen am Anfang und am Ende jeder Spalte (3*2) und den 
    #Rauten zum Trennen sowie am Anfang und Ende (4*1)
    print("".join(c for c in itertools.repeat("#", length + 10)))

def einkommensVergleich(df:pd.DataFrame, limit:int, df_info:str):
    r"""
    

    Parameters
    ----------
    df : pd.DataFrame
        Datensatz, auf dem der Vergleich, wie viele Städte prozentual den Maximal-Wert 
        der Luftverschmutzung übersteigen.
    limit : int
        Je nachdem, welche Partikelmasse betrachtet wird, wird ein unterschiedlicher
        Maximal-Wert vorausgesetzt.
    df_info : str
        Wird lediglich als Extra-Parameter übergeben, um diesen in den Titel zu übernehmen.

    Returns
    -------
    None.

    """
    
    
    print(str("Prozentualer Anteil der Städte, die die \nWHO-Grenzwerte einhalten (" + df_info +")\n" ))
    
    df["limit"] = df.annual_mean <= limit
    HighIncome = [False,True]
    continents = df.region.unique()
    continents.sort()
    
    #Länge der längsten Strings ermitteln, um Zwischenlinie zu skalieren
    maxCon = max([len(x) for x in continents])
    lenNoV = len("No values")
    lenNum = 5
    length = maxCon+lenNoV+lenNum
    zwischenlinie(length)
    
    #Überschriften ausgeben, format-Methode, um String-Formatter nach Variable auszurichten
    format = "# %%%ds" % maxCon # -> %10s
    print(format % "Continent", end = " ")
    print("# %5s" % "LMIC", end = " ")
    print("# %9s #" % "HIC")
    zwischenlinie(length)
                
    #Datenermittlung: Für jeden Kontinent in der Liste wird nach LMIC und HIC gefiltert,
    #ausgewertet und gleichzeitig ausgegeben.
    for con in continents:
        data = df.loc[df.region.str.contains(con)]
        format = "# %%%ds" % maxCon
        print(format % con, end = " ")
        
        for ein in HighIncome:
            dataTemp = data.loc[data.HIC==ein]
            
            #Prüfen, ob der DataFrame überhaupt Daten enthält (gibt es HIC-Städte,
            #im jeweiligen Kontinent im Datensatz)
            if dataTemp.region.count() > 0:
                p = round((len(dataTemp.loc[dataTemp.limit]))/len(dataTemp)*100,2)
                
                #Die Raute am Ende muss nur bei HIC (letzte Spalte) eingefügt werden
                if ein == False:
                    print("# %5.2f" % p, end = " ")
                else:
                    format = "# %%%d.2f #" % lenNoV
                    print(format % p)
            else:
                #percentage.append("No values")
                print("# No values #")
        zwischenlinie(length)
    print("\n")


    
def stadtEntwicklung(stadt: str):
    r"""
    

    Parameters
    ----------
    stadt : str
        Stadt, für die die Entwicklung über die letzten Jahre über die Datenpunkte
        inkl. einer Regressionsgraden angezeigt werden soll. 
        Voraussetzung: Mehr als 2 Dateneinträge.

    Returns
    -------
    None.

    """
    
    frames = {"PM10": pm10, "PM2.5": pm25}
    color = ["blue", "red"]
    for index, key in enumerate(frames):
        df = frames[key]
        data = df.loc[df["city"] == stadt]
        
        #Die Regression soll nur durchgeführt werden, wenn mehr als zwei Datensätze
        #vorhanden sind.
        if data["year"].count() > 2:
            
            #Hundert gleichverteilte Werte zur Regressionsberechnung
            xp = np.linspace(min(data["year"]), max(data["year"]), 100)
            
            #Ermittlung der Luft-Verschmutzungswerte
            anMean = np.array(data.annual_mean)
            
            #Berechnung der Regressionsgraden
            p = np.poly1d(np.polyfit(data["year"], anMean, 1))
            
            #Visuelle Darstellung
            plt.plot(data["year"], anMean, "o", c=color[index])
            plt.plot(xp, p(xp), c = color[index], label=key)
        elif data["year"].count() == 0:
            print("Die angegebene Stadt wurde nicht gefunden")
            break
        else:
            print("Zu dieser Stadt gibt es nicht genug Datenpunkte")
            break
    plt.title(stadt)
    plt.xticks(np.arange(min(data.year), max(data.year)+1))
    plt.legend(loc="best")
    plt.xlabel("Jahr")
    plt.ylabel("Partikelmasse μg/m³")
    plt.show()

def scipyRegression(stadt:str):
    frames = {"PM10": pm10, "PM2.5": pm25}
    color = ["blue", "red"]
    for index, key in enumerate(frames):
        df = frames[key]
        data = df.loc[df["city"] == stadt]
        
        #Die Regression soll nur durchgeführt werden, wenn mehr als zwei Datensätze
        #vorhanden sind.
        if data["year"].count() > 2:
            
            #Slope = Steigung
            #Intercept = Schnittpunkt mit der y-Achse
            
            #*rest, da insgesamt fünf Rückgabewerte, jedoch nur die ersten beiden interessant
            slope, intercept, *rest = stats.linregress(data.year, data.annual_mean)
            plt.plot(data.year, data.annual_mean, "o", c=color[index])
            plt.plot(data.year, intercept+data.year*slope, c=color[index], label = key)
        elif data["year"].count() == 0:
            print("Die angegebene Stadt wurde nicht gefunden")
            break
        else:
            print("Zu dieser Stadt gibt es nicht genug Datenpunkte")
            break
    plt.title(stadt)
    plt.xticks(np.arange(min(data.year), max(data.year)+1))
    plt.legend(loc="best")
    plt.xlabel("Jahr")
    plt.ylabel("Partikelmasse μg/m³")
    plt.show()
            

def stadtRanking(country: str, asc = True):
    r"""
    

    Parameters
    ----------
    country : str
        Land, für welches das Städteranking durchgeführt werden soll.
    asc : TYPE, optional
        Ob der DataFrame auf- (True) bzw. absteigend (False) ausgegeben werden soll. 
        The default is True.

    Returns
    -------
    None.

    """
    
    frames = {"PM10": pm10, "PM2.5": pm25}
    for key in frames:
        df = frames[key]
        #print(df.groupby("year").region.count())
        data = df.loc[df["year"] == 2016]
        data = data.loc[data["country"] == country].sort_values("annual_mean", ascending=asc)
        data = data.loc[:, ["city", "annual_mean"]]
        plt.barh(data.head(10).city, data.head(10).annual_mean)
        rank = "(Best):" if asc == True else "(Worst):"
        plt.title(str("Top 10 Ranking Cities in " +country + " " + key + " " + rank))      
        plt.gca().invert_yaxis()
        plt.xlabel("Partikelmasse μg/m³")
        plt.show()

def GetStationCount(value: str)->int:
    r"""
    

    Parameters
    ----------
    value : str
        Jeweiliger Pandas-Dateneintrag.
        Funktion zum Bereinigen und Addieren der Messstationen einer Stadt.

    Returns
    -------
    int
        Anzahl der Messstationen in der Stadt.

    """
    count = 0
    strvalue = str(value)
    for match in re.findall(r'(\d+)\s+\D+', strvalue):
        count += int(match)
    return count

def uebersichtMessstationen():
    r"""
    
    In dieser Methode wird lediglich ein Donut-Diagramm 
    zur Verteilung der Anzahl an Messtationen geplottet.

    Returns
    -------
    None.

    """
    """
    regions = pm10.region.unique()
    regions.sort()
    data=[]
    for element in regions :
        data.append(pm10.loc[pm10.region == element].monitor_station_count.sum())
    """
    plt.pie(pm10.groupby("region").monitor_station_count.sum(), labels= pm10.region.unique(),wedgeprops=dict(width=0.5))
    plt.title("Verteilung Anzahl an Messstationen nach Kontinenten")
    plt.show()

def uebersichtWertVerteilung():
    r"""
    
    In dieser Methode werden alle Datenpunkte (PM10 und PM25)
    in einem Scatter Diagramm angezeigt.
    Dies zeigt die Verteilung der Datenpunkte an nach Regionen.
    

    Returns
    -------
    None.

    """
    regions = pm10.region.unique()
    plt.style.use("dark_background")
    plt.figure(figsize=(12, 12), dpi= 100)
    for element in regions:
        data10=pm10.loc[pm10.region == element]
        data25=pm25.loc[pm25.region == element]       
        plt.scatter(data25.annual_mean,data10.annual_mean, label=element, s=3)  
    plt.title("DatenPunkte (PM2.5 , PM10) Jahresdurchschnitt nach Regionen")
    plt.xlabel("PM2.5 (annual mean)")
    plt.ylabel("PM10 (annual mean)")
    plt.legend()
    plt.show()

def aufbereitung():
    r"""
    
    In dieser Methode werden die Datensätze gleich bereinigt.
    Es wird nicht berücksichtigt, ob die Werte berechnet oder gemessen wurden.
    Der Wert "temporal coverage" wurde durch eine Klassifikation ersetzt.
    Das Einkommen der Stadt sowie die Angabe, ob es sich um einen berechneten oder einen
    gemessenen Wert handelt, wurden als binäre Werte in eine separate Spalte aufgenommen bzw.
    umgewandelt.

    Returns
    -------
    None.

    """
    
    cols = ['region','iso3','country','city','year','annual_mean','temp_coverage','measured','monitor_station_count','reference','db','status','HIC']
    frames = [pm10, pm25, pm10_latest, pm25_latest]
    for df in frames:
               
        #Neue binäre Spalte HIC
        df["HIC"]=df.Region.str.contains('HIC')
        df.columns=cols
        #Bereinigen der Region Spalte
        df.region= df.region.str.split('(').str[0].str.strip()
        
        #Measured zu einem logischen Attribut machen
        df.measured=df.measured.str.contains('measured', case=False)
        
        #Bereinigen von Annual mean --> nur noch Wert
        df.annual_mean.replace(r'\D', '', regex = True, inplace = True)
        df.annual_mean= df.annual_mean.astype(int)
        #Bereinigen von temp coverage --> 
        df.temp_coverage = df.temp_coverage.fillna(0)
        df.temp_coverage= df.temp_coverage.astype(str)
        temp = list(df.temp_coverage.unique())
        temp.sort()
        for index, cover in enumerate(temp):
            df.temp_coverage.replace(cover, index, inplace = True)   
        df.monitor_station_count= [GetStationCount(x) for x in df.monitor_station_count]

def main():
    aufbereitung()
    PMLimits={"PM10": [40, pm10_latest], "PM2.5": [25, pm25_latest]}
    for key in PMLimits:
        einkommensVergleich(PMLimits[key][1],PMLimits[key][0], key)
    stadtRanking("India", False)
    #stadtEntwicklung("Beijing")
    #stadtEntwicklung("Pasakha")
    scipyRegression("Beijing")
    scipyRegression("Pasakha")
    uebersichtMessstationen()
    uebersichtWertVerteilung()
    
    
if __name__ == "__main__":
    main()