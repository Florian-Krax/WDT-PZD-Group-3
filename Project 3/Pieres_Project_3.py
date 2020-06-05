import pandas as pd

df = pd.read_excel("WHR2018Chapter2OnlineData.xls")
pd.options.display.max_columns = None

def datensatzAnalyse():
    global df
    col = list(df.columns.values)

    #GINI = statistisches Maß zum Aufzeigen von Ungleichverteilungen

    print(col)
    print(df.describe())

def letztesJahr():
    global df
    print("Anzahl Länder:", len(list(df["country"].unique())))
    print(df.loc[df["year"]==2017].sort_values("Life Ladder", ascending=False))
    
def rankingLifeLadder():
    #Ranking der Länder mit Durchschnitt von 2015-2017
    pass

def entwicklung(country: str):
    pass

def main():
    letztesJahr()

if __name__ == "__main__":
    main()