import pandas as pd
import ast
from nltk.corpus import stopwords

pd.options.mode.chained_assignment = None

movies = pd.read_csv('datasets/tmdb.csv', index_col=0)
movies.rename(columns = {'crew':'director'}, inplace=True)
movies.fillna('', inplace=True)

def change_duplicate_titles():
    title_list = movies['title']
    new_title_list = title_list.copy()
    rel_date_list = movies['release_date']
    unique = set()
    duplicate_titles = [title for title in movies['title'] if title in unique or unique.add(title)]
    for i in range(0, len(movies['title'])):
        rel_date = rel_date_list[i].split('-', 1)
        if movies['title'][i] in duplicate_titles:
            new_title_list[i] = movies['title'][i] + " " + "(" + rel_date[0] + ")"
    return new_title_list

def getLiteral(string_list):
    literal_list = []
    for string in ast.literal_eval(string_list):
        literal_list.append(string)
    return literal_list

def removeStopwords(overviews):
    stopwords_english = set(stopwords.words('english'))
    new_overviews = [overview for overview in overviews if overview not in stopwords_english]
    return new_overviews

movies['title'] = change_duplicate_titles()

movies['keywords'] = movies['keywords'].apply(getLiteral)
movies['genres'] = movies['genres'].apply(getLiteral)
movies['cast'] = movies['cast'].apply(getLiteral)
movies['director'] = movies['director'].apply(getLiteral)

export_movies = movies[['id', 'title', 'overview', 'genres', 'keywords', 'release_date', 'cast', 'director', 'popularity', 'vote_average', 'vote_count']]

movies['overview'] = movies['overview'].apply(lambda x:x.lower())
movies['overview'] = movies['overview'].apply(lambda x:x.split())
movies['overview'] = movies['overview'].apply(removeStopwords)

movies_tags = movies[['id', 'title']]
movies_tags['tags'] = movies['overview'] + movies['genres'] + movies['keywords'] + movies['director'] + movies['cast']
movies_tags['tags'] = movies_tags['tags'].apply(lambda x:" ".join(x))
movies_tags['tags'] = movies_tags['tags'].apply(lambda x:x.lower())
