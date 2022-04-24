import numpy as np 
import pandas as pd
from matplotlib import pyplot as plt
from collections import Counter
import seaborn as sns


df = pd.read_csv("netflixData.csv")
df.info()
# shows the release dates description stats
df.describe().T.style.bar()

df.drop_duplicates(inplace=True)
# adding each column of the data's null values and showing percentages
null_values = df.isnull().sum()
null_values
total_null = null_values.sort_values(ascending=False)
perc = (null_values / df.isnull().count()).sort_values(ascending=False)
total = pd.concat([total_null, perc], axis=1, keys=['Total null values', 'Percentages of null values'])
total.T.style.bar()
#col = df._get_numeric_data().columns.tolist()

# Getting rid of hashtags involved with titles
df['Title'] = df['Title'].str.replace('#', '')

# changing imdb scores to numeric 
df['Imdb Score'] = df['Imdb Score'].str.replace('/10', '')
df['Imdb Score'] = df['Imdb Score'].apply(pd.to_numeric)


# showing the difference between Movies and TV shows 
contentType_count = df['Content Type'].value_counts()
contentType_count.plot(kind='pie', legend=True, explode=(0, 0.1), 
                        title = "Comparison of TV Shows vs Movies", colors=["blue", "yellow"],
                        figsize=(10,20))

df.head()
#

genres_compare = df.groupby(["Imdb Score",'Genres'])["Genres"].count()
#genres_compare.columns= ['Title']
genres_compare


genres = ", ".join(df['Genres']).split(", ")
genres
count_genres = Counter()
for genre in genres:
    count_genres[genre] += 1

df.loc[df['language']].value_counts().plot(kind='bar')

high_imdb_ratings = df.loc[df["Imdb Score"] >= '9.0/10', ["Title","Imdb Score","Content Type","count_genres" ]]
high_imdb_ratings = high_imdb_ratings.sort_values(ascending=False, by='Imdb Score').reset_index(drop=True)
high_imdb_ratings


df_topGenres = pd.DataFrame (count_genres, columns = ['Genres','Genres Count'])
df_topGenres.sort_values(ascending=True, by='Genres Count')
df_topGenres

#fig = plt.figure(figsize=(20, 4))
#ax = plt.axes()
#plt.title('Imdb Score')
#sns.histplot(df['Imdb Score'], kde=True)
#plt.xlabel('Imdb Score')
#plt.ylabel('Duration')
#plt.text(3,7, 'Skewness coeff. is:' + str(df['Imdb Score'].skew()))