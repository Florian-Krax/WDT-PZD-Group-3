import pandas as pd
import numpy as np
import itertools
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

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
    df = df.dropna()
    print(df.sort_values("Happiness score", ascending = False))
    plt.barh(np.array(df["Country"]), np.array(df["Happiness score"]))
    plt.show()
    
def entwicklung(country):
    global df
    lr = LinearRegression()
    for land in country:
        data = df.loc[df["country"] == land]
        plt.scatter(data["year"], data["Life Ladder"])
        jahr = np.array(data["year"]).reshape(-1,1)
        ladder = np.array(data["Life Ladder"]).reshape(-1,1)
        lr.fit(jahr, ladder)
        plt.plot(data["year"], lr.predict(jahr), label = land)
    plt.legend(loc="best")
    plt.show()

def einzel():
    df = pd.read_excel("WHR2018Chapter2OnlineData.xls", sheet_name = "Figure2.2")
    col = list(df.columns.values)
    df = df.drop(columns = col[11:])
    print("Ranglistenerster: ", df["Country"][0])
    factors = ["GDP", "Social Support", "Healthy Life", "Freedom", "Generosity", "Corruption"]
    facCoun = {}
    length = 0
    for index, key in enumerate(factors, 5):
        dataTemp = df.sort_values(col[index], ascending = False)
        dataTemp.reset_index(drop = True, inplace = True)
        loes = dataTemp["Country"][0]
        facCoun[key] = loes
        if len(loes) > len(key):
            length += len(loes)
        else:
            length += len(key)
    print("".join(c for c in itertools.repeat("#", length + 3*len(factors) + 4)))
    print("# ", end="")
    for key in facCoun:
        if len(facCoun[key]) > len(key):
            zusatz = "".join(c for c in itertools.repeat(" ", len(facCoun[key]) - len(key)))
        else:
            zusatz=""
        print(str(key + zusatz), "| ", end = "")
    print(" #")
    print("".join(c for c in itertools.repeat("#", length + 3*len(factors) + 4)))
    print("# ", end="")
    for key in facCoun:
        if len(key) > len(facCoun[key]):
            zusatz = "".join(c for c in itertools.repeat(" ", len(key) - len(facCoun[key])))
        else:
            zusatz=""
        print(str(facCoun[key] + zusatz), "| ", end ="")
    print(" #")
    print("".join(c for c in itertools.repeat("#", length + 3*len(factors) + 4)))
    
def corruption():
    global df
    data = df[["country", "Perceptions of corruption"]]
    data = data.groupby("country").mean()
    print(data.sort_values("Perceptions of corruption", ascending = False))

def main():
    #entwicklung(["Germany", "Australia", "Afghanistan"])
    einzel()

if __name__ == "__main__":
    main()