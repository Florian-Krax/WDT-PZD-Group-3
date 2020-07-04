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

#im Folgenden wird häufig col[5] verwendet -> damit wird die Spalte der jährlichen 
#Werte ausgewählt

def zwischenlinie(length: int):
    print("".join(c for c in itertools.repeat("#", length + 10)))

def einkommensVergleich():
    
    #Feinstaub EU- & WHO-Grenzwert PM10 -> 40 Mikrorgamm pro Kubikmeter (Quelle: Umweltbundesamt)
    #Feinstaub EU-Grenzwert PM2.5 -> 25 Mikrogramm pro Kubikmeter (Quelle: Umweltbundesamt)
    
    print("Prozentualer Anteil der Städte, die die WHO-Grenzwerte einhalten.\n")
    pm = pd.read_excel("aap_air_quality_database_2018_v14.xlsx", sheet_name = "latest availble PM25 (measured)", skiprows = 2)
    pm = pm.drop(columns = pm.iloc[:,5:8])
    col = list(pm.columns.values)
    pm25Gr = 25
    pm["Limit"] = pm[col[5]] <= pm25Gr
    income = ["LMIC", "HIC"]
    #Die Kontinente ggf. über replace HIC, LMIC in Python ermitteln lassen -> Vermeidung von Tippfehlern
    continents = ["Africa", "Americas", "Eastern Mediterranean", "Europe", "South-East Asia", "Western Pacific"]
    
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
        data = pm.loc[pm["Region"].str.contains(con)]
        format = "# %%%ds" % maxCon
        print(format % con, end = " ")
        for ein in income:
            dataTemp = data.loc[data["Region"].str.contains(ein)]
            
            #Prüfen, ob der DataFrame überhaupt Daten enthält (gibt es HIC-Städte,
            #im jeweiligen Kontinent im Datensatz)
            if dataTemp.Region.count() > 0:
                p = round((dataTemp.Limit == True).sum()/dataTemp.Region.count()*100,2)
                
                #Die Raute am Ende muss nur bei HIC (letzte Spalte) eingefügt werden
                if ein == "LMIC":
                    print("# %5.2f" % p, end = " ")
                else:
                    format = "# %%%d.2f #" % lenNoV
                    print(format % p)
            else:
                #percentage.append("No values")
                print("# No values #")
        zwischenlinie(length)

    
def stadtEntwicklung(stadt: str):
    global pm10
    global pm25
    
    frames = [pm10, pm25]
    color = ["blue", "red"]
    for index, df in enumerate(frames):
        col = list(df.columns.values)
        data = df.loc[df["City/Town"] == stadt]
        
        #Die Regression soll nur durchgeführt werden, wenn mehr als zwei Datensätze
        #vorhanden sind.
        if data["Year"].count() > 2:
            xp = np.linspace(min(data["Year"]), max(data["Year"]), 100)
            anMean = np.array(data[col[5]])
            p = np.poly1d(np.polyfit(data["Year"], anMean, 1))
            plt.plot(data["Year"], anMean, "o", xp, p(xp), c = color[index])
        elif data["Year"].count() == 0:
            print("Die angegebene Stadt wurde nicht gefunden")
            break
        else:
            print("Zu dieser Stadt gibt es nicht genug Datenpunkte")
            break
    plt.title(stadt)
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
        col = list(df.columns.values)
        data = df.loc[df["Year"] == 2016]
        data = data.loc[data["Country"] == country].sort_values(col[5], ascending=asc)
        data = data.loc[:, ["City/Town", col[5]]]
        print("Top 10 Ranking",key,"(Best):") if asc == True else print("Top 10 Ranking",key,"(Worst):")
        print(data.head(10), "\n")

def GetStationCount(value: str)->int:
    count = 0
    strvalue = str(value)
    for match in re.findall(r'(\d+)\s+\D+', strvalue):
        count += int(match)
    return count

def aufbereitung():
    
    #Zur einfacheren Handhabung werden die umgerechneten Zahlen gleichbetrachtet
    #Temporal coverage wird in Klassen aufgeteilt
    
    #ggf. weitere Spalten aufgrund von Nichtbetrachtung droppen
    #ggf. noch dropna    
    
    global pm10
    global pm25
    frames = [pm10, pm25]
    for df in frames:
        col = list(df.columns.values)
        df[col[5]].replace(r'\D', '', regex = True, inplace = True)
        df[col[5]] = df[col[5]].astype(int)
        df[col[6]] = df[col[6]].fillna(0)
        df[col[6]] = df[col[6]].astype(str)
        temp = list(df[col[6]].unique())
        temp.sort()
        for index, cover in enumerate(temp):
            df[col[6]].replace(cover, index, inplace = True)   
        df[col[-4]] = [GetStationCount(x) for x in df[col[-4]]]

def main():
    aufbereitung()
    einkommensVergleich()
    stadtRanking("China", False)
    stadtEntwicklung("Beijing")

if __name__ == "__main__":
    main()