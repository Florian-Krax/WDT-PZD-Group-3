import pandas as pd
import numpy as np
import itertools
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

df = pd.read_excel("WHR2018Chapter2OnlineData.xls")
pd.options.display.max_columns = None
    
def rankingLifeLadder(start: int):
    global df
    data = df.loc[df["year"] >= start]
    data = df.groupby("country").mean().sort_values("Life Ladder", ascending = False)
    print(data)

def entwicklung(country: list):
    global df
    lr = LinearRegression()
    xp = np.linspace(2005,2017,24)
    color = ["blue", "green", "red", "yellow", "black"]
    #LogisticRegression funktioniert nur mit Float-Werten?
    for index, land in enumerate(country):
        data = df.loc[df["country"] == land]
        jahr = np.array(data["year"])
        ladder = np.array(data["Life Ladder"])
        lr.fit(jahr.reshape(-1,1), ladder.reshape(-1,1))
        plt.plot(data["year"], lr.predict(jahr.reshape(-1,1)), c=color[index], label = land)
        p = np.poly1d(np.polyfit(jahr, ladder, 3))
        plt.plot(jahr, ladder, "o", xp, p(xp), c=color[index])
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
        length = length + len(loes) if len(loes) > len(key) else length + len(key)
    keys = list(facCoun.keys())
        
    def trennlinie(fertig = False):
        print("".join(c for c in itertools.repeat("#", length + 1 + 3*len(factors))))
        if fertig == False:
            print("# ", end ="")
            
    trennlinie()
    for key in facCoun:
        if len(facCoun[key]) > len(key):
            zusatz = "".join(c for c in itertools.repeat(" ", len(facCoun[key]) - len(key)))
        else:
            zusatz=""
        print(str(key + zusatz), "| ", end = "") if key != keys[-1] else print(key + zusatz, end="")
    print(" #")
    trennlinie()
    for key in facCoun:
        if len(key) > len(facCoun[key]):
            zusatz = "".join(c for c in itertools.repeat(" ", len(key) - len(facCoun[key])))
        else:
            zusatz=""
        print(str(facCoun[key] + zusatz), "| ", end ="") if key != keys[-1] else print(str(facCoun[key] + zusatz), end="")
    print(" #")
    trennlinie(True)
    
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
            xerr = dfTemp.iloc[:,2]-dfTemp.iloc[:,3] if i == 10 else None
            ar = np.char.mod('%d', dfTemp.index.values + 1)
            dfTemp["Label"] = [value + '. ' + c + '(' + str(round(h,3)) + ')' for value, c, h in zip(ar, dfTemp["Country"], dfTemp["Happiness score"])] 
            #stac = True -> erspart For-Schleife
            plt.barh(dfTemp["Label"], data, color=color, left=left, xerr=xerr, label = col[i])
            plt.gca().invert_yaxis()
            plt.legend(ncol = int(len(colorList)/2), bbox_to_anchor=(0,1), loc="lower left", fontsize="small")
            left+=data
        plt.show()

def whereToGo():
    df = pd.read_excel("WHR2018Chapter2OnlineData.xls", sheet_name = "Figure2.4")
    col = df.columns.values
    df = df.drop(columns=col[5:])
    col = col[:5]
    col = list(map(lambda x: str.replace(x, "Average happiness of", "happiness"), col))
    df.columns = col
    df["Diff"] = df.iloc[:,1] - df.iloc[:,4]
    df = df.loc[((df[col[1]] + df[col[-2]])/2) > 6.5]
    df = df.sort_values("Diff", ascending = False)
    print(df.head())

def entwicklungV2(country: list):
    global df
    color = ["blue", "green", "red", "yellow", "black"]
    for index, land in enumerate(country):
        data = df.loc[df["country"] == land]
        xp = np.linspace(2005, 2020, 30)
        jahr = np.array(data["year"])
        ladder = np.array(data["Life Ladder"])
        plt.scatter(jahr, ladder, c=color[index])
        for i in range(1,4):
            p = np.poly1d(np.polyfit(jahr, ladder, i))
            plt.plot(jahr, ladder, "o", xp, p(xp), c=color[index])
    plt.show()

def main():
    entwicklung(["Germany", "Finland", "Denmark"])
    #entwicklungV2(["Germany", "Finland"])
    #rankingDetail()
    einzel()
    #whereToGo()
    #rankingLifeLadder(2013)
    
if __name__ == "__main__":
    main()