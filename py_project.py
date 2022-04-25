import numpy as np 
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns


df = pd.read_csv("netflixData.csv")
df.info()
# shows the release dates description stats
df.describe().T.style.bar()

# adding each column of the data's null values and showing percentages
null_values = df.isnull().sum()
null_values
total_null = null_values.sort_values(ascending=False)
perc = (null_values / df.isnull().count()).sort_values(ascending=False)
total = pd.concat([total_null, perc], axis=1, keys=['Total null values', 'Percentages of null values'])
total.T.style.bar()

# Getting rid of hashtags involved with titles
df['Title'] = df['Title'].str.replace('#', '')

# showing the difference between Movies and TV shows 
contentType_count = df['Content Type'].value_counts()
contentType_count.plot(kind='pie', legend=True, explode=(0, 0.1), 
                        title = "Comparison of TV Shows vs Movies", colors=["blue", "yellow"],
                        figsize=(10,20))

# changing imdb scores to numeric 
df['Imdb Score'] = df['Imdb Score'].str.replace('/10', '')
df['Imdb Score'] = df['Imdb Score'].apply(pd.to_numeric)
df['Imdb Score']

# create dataframe looking at mean of TV Shows vs Movies
Content_imdb = pd.DataFrame(df.groupby('Content Type')['Imdb Score'].mean()).sort_values(ascending=False, by='Imdb Score')
Content_imdb

#Create a pie chart looking at 
Content_imdb.plot(kind='pie', legend=True, explode=(0, 0.1), 
                        title = "Comparison of TV Shows vs Movies", colors=["red", "yellow"],
                        figsize=(10,20), subplots=True)


# This chunk of code will apply a dataframe from the movie content type and split the genres
# afterwards I stack the genres and use the mean imdb scores to plot this on a bar cahrt
movie_genres_df = df[df['Content Type']== 'Movie']
movie_genres_df = (movie_genres_df['Genres'].str.split(',', expand=True)
            .stack()
            .to_frame(name='Genres'))
#movie_genres_df.index = movie_genres_df.index.droplevel(1)

((movie_genres_df.join(df['Imdb Score']).groupby('Genres')
       .mean())
       .sort_values(by='Imdb Score')
       .plot(kind='barh', figsize=(10,20)))





tv_genres_df = df[df['Content Type']== 'TV Show']
tv_genres_df = (tv_genres_df['Genres'].str.split(',', expand=True)
            .stack()
            .to_frame(name='Genre'))

tv_genres_df.index = tv_genres_df.index.droplevel(1)
tv_genres_df

((tv_genres_df.join(df['Imdb Score'])
       .groupby('Genre')
       .mean())
       .sort_values(by='Imdb Score')
       .plot(kind='barh', figsize=(10,20)))

























movie_ratings = df[df['Content Type'] == 'Movie'].groupby('Date added')['averageRating'].mean()









movies_imdb = df.groupby(df['Content Type' == 'Movies'])
movies_imdb = pd.DataFrame(movies_imdb)
movies_imdb.describe()

df.head()















