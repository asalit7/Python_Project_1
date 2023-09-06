import numpy as np 
import pandas as pd
from matplotlib import pyplot as plt
import plotly.express as px
import seaborn as sns

df = pd.read_csv("netflixData.csv")

# changing the release dates from float to int
df['Release Date'] = df['Release Date'].astype('Int64')

# adding each column of the data's null values and showing percentages
null_values = df.isnull().sum()
total_null = null_values.sort_values(ascending=False).astype('Int64')
perc = (null_values / df.isnull().count()).sort_values(ascending=False)
total = pd.concat([total_null, perc], axis=1, keys=['Total null values', 'Percentages of null values'])

# Getting rid of hashtags involved with titles
df['Title'] = df['Title'].str.replace('#', '')

# Changing imdb scores to numeric 
df['Imdb Score'] = df['Imdb Score'].str.replace('/10', '')
df['Imdb Score'] = df['Imdb Score'].apply(pd.to_numeric)

# Changed text of date to a datetime format
df['Date Added'] = pd.to_datetime(df['Date Added'])

# Creating a year column
df['Year'] = df['Date Added'].dt.year.astype('Int64')

df['Genres']
genre = {}


for x in df['Genres']:
    print(x)
    if x in genre:
        genre[x]+=1
    else:
        genre[x]=0
print(genre)


df.info()
# shows the release dates description stats
df.describe().T.style.bar()

df.head()
df[['Content Type']]
# Viewing Imdb overall in context to years
year_imdb = pd.DataFrame(df.groupby('Year')['Imdb Score'].mean()).sort_values(by='Year')
year_imdb

sns.lineplot(data=year_imdb')

year_imdb.plot(kind='line', legend=True, title = 'Imdb Scores over the Years', color='Content Type')

# Create dataframe looking at mean of TV Shows vs Movies
Content_imdb = pd.DataFrame(df.groupby('Content Type')['Imdb Score'].mean() ).sort_values(ascending=False, by='Imdb Score')
Content_imdb

# Create a pie chart looking at 
Content_imdb.plot(kind='pie', legend=True, explode=(0, 0.1), 
                        title = "Comparison of TV Shows vs Movies", colors=["red", "yellow"],
                        figsize=(10,20), subplots=True)

# Showing the difference between Movies and TV shows 
contentType_count = df['Content Type'].value_counts()
contentType_count.plot(kind='pie', legend=True, explode=(0, 0.1), 
                        title = "Comparison of TV Shows vs Movies",
                        figsize=(10,20))

# This code will apply a dataframe from the movie content type and split the genres
# stack the genres and use the mean imdb scores to plot this on a bar chart
movie_genres_df = df[df['Content Type']== 'Movie']
movie_genres_df = (movie_genres_df['Genres'].str.split(',', expand=True)
            .stack()
            .to_frame(name='Genres'))
movie_genres_df['Genres'] = (movie_genres_df['Genres'].str.strip())
movie_genres_df.index = movie_genres_df.index.droplevel(1)
movie_genres_df = movie_genres_df.join(df['Imdb Score'])
movie_genres_df = movie_genres_df.groupby('Genres').mean().sort_values(by='Imdb Score')
movie_genres_df.plot(kind='barh', figsize=(10,20), title='Top Genres for IMDb Scores in Movies')

# This will split up the multiple genres in the tv show Content Type and create a bar graph
# based on imdb score
tv_genres_df = (df['Genres'].str.split(',', expand=True)
            .stack()
            .to_frame(name='Genres'))
tv_genres_df['Genres'] = (tv_genres_df['Genres'].str.strip())
tv_genres_df.index = tv_genres_df.index.droplevel(1)
tv_genres_df = tv_genres_df.join(df.loc[:,['Imdb Score','Content Type']])
tv_genres_df = tv_genres_df[df['Content Type'] == 'TV Show']
tv_genres_df = tv_genres_df.groupby('Genres').mean().sort_values(by='Imdb Score')
tv_genres_df.plot(kind='barh', figsize=(10,20), title='Top Genres for IMDb Scores in TV Shows', color = 'Purple')

# Calculating the production country locations means in respect to imdb score
production_df_mean = df.loc[:,['Production Country', 'Imdb Score']].groupby('Production Country').mean()
production_df_mean = production_df_mean.sort_values(by='Imdb Score', ascending=False).iloc[:10]
production_df_mean = production_df_mean.sort_values(by='Imdb Score', ascending=True)
production_df_mean.plot(kind='barh', figsize=(10,20), title='Top 10 Number of Production Location Means')

# Calculating the production country locations counts
production_df_count = df.loc[:,['Production Country', 'Imdb Score']].groupby('Production Country').count()
production_df_count = production_df_count.sort_values(by='Imdb Score', ascending=False).iloc[:10]
production_df_count= production_df_count.sort_values(by='Imdb Score', ascending=True)
production_df_count.plot(kind='barh', figsize=(10,20), title='Top 10 Number of Production Locations of TV Shows and Movies', color='red')


# Calculating the Release Date means in respect to imdb score
release_mean = df.loc[:,['Release Date', 'Imdb Score']].groupby('Release Date').mean()
release_mean = release_mean.sort_values(by='Imdb Score', ascending=False).iloc[:10]
release_mean = release_mean.sort_values(by='Imdb Score', ascending=True)
release_mean.plot(kind='barh', figsize=(10,20), title='Top 10 Means Based on Release Dates')

# Calculating the Release Date count 
release_count = df.loc[:,['Release Date', 'Imdb Score']].groupby('Release Date').count()
release_count = release_count.sort_values(by='Imdb Score', ascending=False).iloc[:10]
release_count = release_count.sort_values(by='Imdb Score', ascending=True)
release_count.plot(kind='barh', figsize=(10,20), title='Top 10 Highest Number of Release Dates', color='red')











