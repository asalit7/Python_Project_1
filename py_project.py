import numpy as np 
import pandas as pd



df = pd.read_csv("netflixData.csv")
df.info()
df.describe().T.style.bar()