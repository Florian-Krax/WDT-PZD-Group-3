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

pm = pd.read_excel("aap_air_quality_database_2018_v14.xlsx", sheet_name = "latest availble PM25 (measured)", skiprows = 2)
pm10_latest = pm.drop(columns = pm.iloc[:,5:8])


pm = pd.read_excel("aap_air_quality_database_2018_v14.xlsx", sheet_name = "latest availble PM10 (measured)", skiprows = 2)
pm25_latest = pm.drop(columns = pm.iloc[:,8:11])
#data = {"PM10": pm10, "PM2.5": pm25}

#Feinstaub EU- & WHO-Grenzwert PM10 -> 40 Mikrorgamm pro Kubikmeter (Quelle: Umweltbundesamt)
#Feinstaub EU-Grenzwert PM2.5 -> 25 Mikrogramm pro Kubikmeter (Quelle: Umweltbundesamt)
#feststehende Grenzwerte 
PMLimits={"PM10": 40, "PM25": 25}

#im Folgenden wird häufig col[5] verwendet -> damit wird die Spalte der jährlichen 
#Werte ausgewählt

def zwischenlinie(length: int):
    print("".join(c for c in itertools.repeat("#", length + 10)))

def einkommensVergleich(df:pd.DataFrame, limit:int, df_info:str):
    
    
    print("Prozentualer Anteil der Städte, die die ")
    print("WHO-Grenzwerte einhalten.\n")
    pm = pd.read_excel("aap_air_quality_database_2018_v14.xlsx", sheet_name = "latest availble PM25 (measured)", skiprows = 2)
    pm = pm.drop(columns = pm.iloc[:,5:8])
    col = list(pm.columns.values)
    pm25Gr = 25
    pm["Limit"] = pm[col[5]] <= pm25Gr
    income = ["LMIC", "HIC"]
    print("Prozentualer Anteil der Städte, die die WHO-Grenzwerte einhalten (", df_info,")\n" )
    #pm = pd.read_excel("aap_air_quality_database_2018_v14.xlsx", sheet_name = "latest availble PM25 (measured)", skiprows = 2)
    #pm = pm.drop(columns = pm.iloc[:,5:8])
    
    #col = list(pm.columns.values)
    #pm25Gr = 25
    
    df["Limit"] = df.annual_mean <= limit
    HighIncome = [ False,True]
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
    
#    def PrintValue(dataTmp:pd.DataFrame,ein:str):
#         #Prüfen, ob der DataFrame überhaupt Daten enthält (gibt es HIC-Städte,
#         #im jeweiligen Kontinent im Datensatz)
#         if dataTemp.Region.count() > 0:
#                p = round((dataTemp.Limit == True).sum()/dataTemp.Region.count()*100,2)
#                
#                #Die Raute am Ende muss nur bei HIC (letzte Spalte) eingefügt werden
#                if ein == "LMIC":
#                    print("# %5.2f" % p, end = " ")
#                else:
#                    format = "# %%%d.2f #" % lenNoV
#                    print(format % p)    
#         else:
#                #percentage.append("No values")
#                print("# No values #")
                
    #Datenermittlung: Für jeden Kontinent in der Liste wird nach LMIC und HIC gefiltert,
    #ausgewertet und gleichzeitig ausgegeben.
    for con in continents:
        data = df.loc[df.Region.str.contains(con)]
        #data = df.Region.str.contains(con)
        format = "# %%%ds" % maxCon
        print(format % con, end = " ")
        #for ein in income:
        #dataTemp = data.loc[data.HIC == True]
       # PrintValue(dataTemp,"LMIC")
        #dataTemp = data.loc[data.HIC == False]
        #PrintValue(dataTemp,"HIC")
       # zwischenlinie(length)
        
        for ein in HighIncome:
            dataTemp = data.loc[data.HIC==ein]
            
            #Prüfen, ob der DataFrame überhaupt Daten enthält (gibt es HIC-Städte,
            #im jeweiligen Kontinent im Datensatz)
            if dataTemp.Region.count() > 0:
                p = round((dataTemp.Limit == True).sum()/dataTemp.Region.count()*100,2)
                
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
<<<<<<< Updated upstream
=======


>>>>>>> Stashed changes
    
def stadtEntwicklung(stadt: str):
    global pm10
    global pm25
    
    frames = {"PM10": pm10, "PM2.5": pm25}
    color = ["blue", "red"]
<<<<<<< Updated upstream
    for index, key in enumerate(frames):
        df = frames[key]
        col = list(df.columns.values)
        data = df.loc[df["City/Town"] == stadt]
=======
    for index, df in enumerate(frames):
        #col = list(df.columns.values)
        data = df.loc[df["City"] == stadt]
>>>>>>> Stashed changes
        
        #Die Regression soll nur durchgeführt werden, wenn mehr als zwei Datensätze
        #vorhanden sind.
        if data["Year"].count() > 2:
            xp = np.linspace(min(data["Year"]), max(data["Year"]), 100)
            anMean = np.array(data.annual_mean)
            p = np.poly1d(np.polyfit(data["Year"], anMean, 1))
            plt.plot(data["Year"], anMean, "o", c=color[index])
            plt.plot(xp, p(xp), c = color[index], label = key)
            plt.xticks(np.arange(min(data["Year"]), max(data["Year"])+1))
        elif data["Year"].count() == 0:
            print("Die angegebene Stadt wurde nicht gefunden")
            break
        else:
            print("Zu dieser Stadt gibt es nicht genug Datenpunkte")
            break
    plt.title(stadt)
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
        #col = list(df.columns.values)
        data = df.loc[df["Year"] == 2016]
        data = data.loc[data["Country"] == country].sort_values("annual_mean", ascending=asc)
        data = data.loc[:, ["City", "annual_mean"]]
        print("Top 10 Ranking",key,"(Best):") if asc == True else print("Top 10 Ranking",key,"(Worst):")
        print(data.head(10), "\n")
        plt.barh(data.head(10).City, data.head(10).annual_mean)    
        plt.title(str("Top 10 Ranking Cities " +key+" (Best):"))  if asc == True else plt.title(str("Top 10 Ranking Cities " +key+" (Worst):"))    
        plt.gca().invert_yaxis()
        plt.show()
       # plt.barh(data.head(10).annual_mean,width=5)

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
    
    cols = ['Region','iso3','Country','City','Year','annual_mean','temp_coverage','measured','monitor_station_count','Reference','DB','status','HIC']
    global pm10
    global pm25
    frames = [pm10, pm25, pm10_latest, pm25_latest]
    for df in frames:
               
        #Neue Spalte HIC
        df["HIC"]=df.Region
        #Bereinigen der Region Spalte
        df.Region= df.Region.str.split('(').str[0]
        #Zu einem logischen Attribut machen
        df.HIC=df.HIC.str.contains('HIC')
        
        df.columns=cols
        
        #Measured zu einem logischen Attribut machen
        df.measured=df.measured.str.contains('measured',case=False)
        
            #col = list(df.columns.values)
        #Bereinigen von Annual mean --> nur noch Wert
        df.annual_mean.replace(r'\D', '', regex = True, inplace = True)
        df.annual_mean= df.annual_mean.astype(int)
        #Bereinigen von temo coverage --> 
        df.temp_coverage = df.temp_coverage.fillna(0)
        df.temp_coverage= df.temp_coverage.astype(str)
            #df[col[5]].replace(r'\D', '', regex = True, inplace = True)
            #df[col[5]] = df[col[5]].astype(int)
            #df[col[6]] = df[col[6]].fillna(0)
            #df[col[6]] = df[col[6]].astype(str)
        temp = list(df.temp_coverage.unique())
        temp.sort()
        for index, cover in enumerate(temp):
            df.temp_coverage.replace(cover, index, inplace = True)   
        df.monitor_station_count= [GetStationCount(x) for x in df.monitor_station_count]

def main():
    aufbereitung()
<<<<<<< Updated upstream
    einkommensVergleich()
    stadtRanking("India", False)
    stadtRanking("India")
    stadtEntwicklung("Pasakha")
=======
    einkommensVergleich(pm10_latest,PMLimits["PM10"],"PM10")
    einkommensVergleich(pm25_latest,PMLimits["PM25"], "PM2.5")
    stadtRanking("China", True)
    stadtEntwicklung("Beijing")
>>>>>>> Stashed changes

if __name__ == "__main__":
    main()