import pandas as pd
import numpy as np
import re
data = {
    'Zeichen' : ['abc' , 'dev', 'cV', 'ajg'],
    'Wert' : [1,2,3,4]
}

df = pd.DataFrame(data)


df['new'] = (df.Zeichen.str.contains('v', flags=re.IGNORECASE) * 1.54 + 1 )* df.Wert
print(df)