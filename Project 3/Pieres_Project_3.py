import pandas as pd
import numpy as np
import itertools
import matplotlib.pyplot as plt
from sklearn import linear_model
from sklearn import svm
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import LogisticRegression

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
    
def rankingLifeLadder(start: int):
    #eigener Durchschnitt
    pass

def ranking():
    df = pd.read_excel("WHR2018Chapter2OnlineData.xls", sheet_name = "Figure2.2")
    col = list(df.columns.values)
    df = df.drop(columns=col[11:])
    #Es wird eine Zeile zu viel eingelesen
    df = df.dropna()
    print(df.sort_values("Happiness score", ascending = False))
    plt.barh(np.array(df["Country"]), np.array(df["Happiness score"]))
    plt.show()
    
def entwicklung(country: list):
    global df
    lr = LinearRegression()
    #LogisticRegression funktioniert nur mit Float-Werten?
    lor = LogisticRegression()
    for land in country:
        data = df.loc[df["country"] == land]
        plt.scatter(data["year"], data["Life Ladder"])
        jahr = np.array(data["year"]).reshape(-1,1)
        ladder = np.array(data["Life Ladder"]).reshape(-1,1)
        lr.fit(jahr, ladder)
        #lor.fit(jahr, ladder)
        plt.plot(data["year"], lr.predict(jahr), label = land)
        #plt.plot(data["year"], lor.predict(jahr.append(c for c in range(2018,2022))), label = land)
    plt.legend(loc="best")
    plt.show()

def continents():
    df = pd.read_excel("WHR2018Chapter2OnlineData.xls", sheet_name = "SupportingFactors")
    data = df[["Region indicator", "Life ladder, 2015-2017"]]
    data = data.groupby("Region indicator").mean().sort_values("Life ladder, 2015-2017", ascending=False)
    print(data)
    
def einzel():
    df = pd.read_excel("WHR2018Chapter2OnlineData.xls", sheet_name = "Figure2.2")
    col = list(df.columns.values)
    df = df.drop(columns = col[11:])
    print("Ranglistenerster: ", df["Country"][0])
    factors = ["GDP", "Social Support", "Healthy Life", "Freedom", "Generosity", "Corruption"]
    facCoun = {}
    length = 0
    for index, key in enumerate(factors, 4):
        #Interpretation von Perception of corruption??
        asc = False if index < 9 else True
        dataTemp = df.sort_values(col[index], ascending = asc)
        dataTemp.reset_index(drop = True, inplace = True)
        loes = dataTemp["Country"][0]
        facCoun[key] = loes
        if len(loes) > len(key):
            length += len(loes)
        else:
            length += len(key)
        keys = list(facCoun.keys())
    print("".join(c for c in itertools.repeat("#", length + 1 + 3*len(factors))))
    print("# ", end="")
    for key in facCoun:
        if len(facCoun[key]) > len(key):
            zusatz = "".join(c for c in itertools.repeat(" ", len(facCoun[key]) - len(key)))
        else:
            zusatz=""
        print(str(key + zusatz), "| ", end = "") if key != keys[-1] else print(key + zusatz, end="")
    print(" #")
    print("".join(c for c in itertools.repeat("#", length + 1 + 3*len(factors))))
    print("# ", end="")
    for key in facCoun:
        if len(key) > len(facCoun[key]):
            zusatz = "".join(c for c in itertools.repeat(" ", len(key) - len(facCoun[key])))
        else:
            zusatz=""
        print(str(facCoun[key] + zusatz), "| ", end ="") if key != keys[-1] else print(str(facCoun[key] + zusatz), end="")
    print(" #")
    print("".join(c for c in itertools.repeat("#", length + 1 + 3*len(factors))))
    
def corruption():
    global df
    data = df[["country", "Perceptions of corruption"]]
    data = data.groupby("country").mean()
    print(data.sort_values("Perceptions of corruption", ascending = False))

def rankingDetail():
    df = pd.read_excel("WHR2018Chapter2OnlineData.xls", sheet_name = "Figure2.2")
    colorList = ["blue", "mediumvioletred", "green", "orange", "darkcyan", "firebrick", "mediumpurple"]
    col = list(map(lambda x: str.replace(x, "Explained by: ", ""), df.columns.values))
    df.columns = col
    df = df.drop(columns=col[11:])
    col = col[:11]
    df = df.dropna()
    step = 25
    for index in range(0,126,step):
        plt.xlim(0,8)
        rest = 0 if df["Country"].count() - index > 2*step else (df["Country"].count() - index) % step
        daten = []
        dfTemp = df.loc[index:index+step+rest,:]
        for spalte in col[4:]:
            daten.append(dfTemp[spalte])
        left=0
        for i, (data, color) in enumerate(zip(daten, colorList),4):
            #Platzierung wäre noch gut
            xerr = dfTemp.iloc[:,2]-dfTemp.iloc[:,3] if i == 10 else None
            plt.barh(dfTemp["Country"], data, color=color, left=left, xerr=xerr, label = col[i])
            plt.gca().invert_yaxis()
            plt.legend(ncol = int(len(colorList)/2), bbox_to_anchor=(0,1), loc="lower left", fontsize="small")
            left+=data
        plt.show()
        
def noData():
    global df
    data = df.groupby("country").mean()
    print(data.isnull().sum())

def whereToGo():
    df = pd.read_excel("WHR2018Chapter2OnlineData.xls", sheet_name = "Figure2.4")
    col = df.columns.values
    df = df.drop(columns=col[5:])
    col = col[:5]
    col = list(map(lambda x: str.replace(x, "Average happiness of", "happiness"), col))
    df.columns = col
    df["Diff"] = df.iloc[:,1] - df.iloc[:,4]
    df = df.sort_values("Diff", ascending = False)
    print(df.head())

def main():
    entwicklung(["Germany", "Finland", "Denmark"])
    #rankingDetail()
    #einzel()
    whereToGo()
    
if __name__ == "__main__":
    main()