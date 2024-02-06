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


df.info()
# shows the release dates description stats
df.describe().T.style.bar()

df.head()

# Creating a genre and setting to list
test_genres = df['Genres'].tolist()
# Removing the commas to split movies/tv shows with multiple genres
test = (','.join(test_genres)).split(',')
# Filtering the genres to not have TV Shows or Movies in their name to have a combined genre
filtered_list = [item.replace('TV Shows', '').replace('TV', '').replace('Movies', '').strip() for item in test]

# Iterating through the genre list to count the amount of each Genre
genre = {}
for x in filtered_list:
    if x == ' ' or x == '':
        pass
    elif x in genre:
        genre[x]+=1
    else:
        genre[x]=0

# Sorting the genre to show the top 10
sorted_genre = sorted(genre.items(), key=lambda x:x[1], reverse=True)[:10]
# Extract the top 10 categories and values
top_categories = [item[0] for item in sorted_genre]
top_values = [item[1] for item in sorted_genre]


# Set the figure size
plt.figure(figsize=(10, 6))
# Adding a white grid background and setting a palette
sns.set_style("whitegrid")
palette = sns.color_palette("viridis", len(top_categories))
# Graphing the top 5 Genres in a bar chart
sns.barplot(x=top_values, y=top_categories, palette=palette)


# Adding labels and title
plt.xlabel('Values', fontsize=14)
plt.ylabel('Genres', fontsize=14)
plt.title('Top 10 Genres', fontsize=16)


# Customizing font size
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)


# Adding data values on top of the bars
for i, v in enumerate(top_values):
    plt.text(v + 1, i, str(v), va='center', fontsize=12, fontweight='bold')


# Remove the top and right spines
sns.despine()
# Showing the top 10 Genres by count
plt.tight_layout()
plt.show()


# Viewing Imdb overall in context to years
year_imdb = pd.DataFrame(df.groupby('Release Date')['Imdb Score'].mean()).sort_values(by='Release Date')
year_imdb

year_imdb.plot(kind='line', legend=True, title = 'Imdb Scores over the Years')

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


# Calculating the Release Date count 
release_count = df.loc[:,['Release Date', 'Imdb Score']].groupby('Release Date').count()
release_count = release_count.sort_values(by='Imdb Score', ascending=False).iloc[:10]
release_count = release_count.sort_values(by='Imdb Score', ascending=True)
# Adjusting figure size
plt.figure(figsize=(12, 8))
plt.barh(release_count.index, release_count['Imdb Score'], color='skyblue')
# Adding title
plt.title('Top 10 Highest Number of Release Dates', fontsize=16)
# Adding x and y labels
plt.xlabel('Number of Releases', fontsize=14)
plt.ylabel('Release Date', fontsize=14)
plt.gca().invert_yaxis()  # To have the highest count at the top
plt.grid(axis='x', linestyle='--', alpha=0.6)

# Display the count values on each bar
for index, value in enumerate(release_count['Imdb Score']):
    plt.text(value, index, str(value), fontsize=12, va='center', ha='left', color='darkblue')

plt.show()

# Calculating the Release Date count
release_count = df['Release Date'].value_counts().nlargest(10).reset_index()
release_count.columns = ['Release Date', 'Count']
release_count['Count'] = release_count['Count'].astype(int)  # Ensure 'Count' is treated as an integer

# Ensure 'Count' is treated as an integer
type(release_count['Count'])

# Create a nicer bar chart using Seaborn
plt.figure(figsize=(8, 6))
sns.set(style="whitegrid")  # Set the style to whitegrid
colors = sns.color_palette("viridis", len(release_count))

# Create the barplot
ax = sns.barplot(x='Release Date', y='Count', data=release_count, palette=colors)


# Adding labels and title
plt.xlabel('Release Date', fontsize=14)
plt.ylabel('Count of Movies and TV Shows', fontsize=14)
plt.title('Top 10 Highest Number of Release Dates', fontsize=16)

# Customize the tick labels and font size
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)

# Adding data values inside the bars
for index, value in enumerate(release_count['Count']):
    ax.text(value + 1, index, str(value), va='center', fontsize=12, fontweight='bold')

plt.tight_layout()
plt.show()







