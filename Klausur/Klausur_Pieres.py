import pandas as pd
import itertools
import numpy as np
import matplotlib.pyplot as plt
import re

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
PMLimits={"PM10": [40, pm10_latest], "PM2.5": [25, pm25_latest]}

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
    format = "# %%%ds" % maxCon
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
                p = round((dataTemp.limit == True).sum()/dataTemp.region.count()*100,2)
                
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
    global pm10
    global pm25
    
    frames = [pm10, pm25]
    color = ["blue", "red"]
    for index, df in enumerate(frames):
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
            plt.plot(data["year"], anMean, "o")
            plt.plot(xp, p(xp), c = color[index], label=stadt)
        elif data["year"].count() == 0:
            print("Die angegebene Stadt wurde nicht gefunden")
            break
        else:
            print("Zu dieser Stadt gibt es nicht genug Datenpunkte")
            break
    plt.title(stadt)
    plt.xticks(np.arange(min(data.year), max(data.year)+1))
    plt.legend(loc="best")
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
    global pm10
    global pm25
    
    frames = {"PM10": pm10, "PM2.5": pm25}
    for key in frames:
        df = frames[key]
        data = df.loc[df["year"] == 2016]
        data = data.loc[data["country"] == country].sort_values("annual_mean", ascending=asc)
        data = data.loc[:, ["city", "annual_mean"]]
        plt.barh(data.head(10).city, data.head(10).annual_mean)    
        plt.title(str("Top 10 Ranking Cities in " +country + " " +key+" (Best):"))  if asc == True else plt.title(str("Top 10 Ranking Cities in " +country+ " " +key+" (Worst):"))    
        plt.gca().invert_yaxis()
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
    global pm10
    global pm25
    frames = [pm10, pm25, pm10_latest, pm25_latest]
    for df in frames:
               
        #Neue Spalte HIC
        df["HIC"]=df.Region
        df.columns=cols
        #Bereinigen der Region Spalte
        df.region= df.region.str.split('(').str[0]
        #Zu einem logischen Attribut machen
        df.HIC=df.HIC.str.contains('HIC')
        
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
    for key in PMLimits:
        einkommensVergleich(PMLimits[key][1],PMLimits[key][0], key)
    stadtRanking("India", False)
    stadtEntwicklung("Berlin")

if __name__ == "__main__":
    main()