import pandas as pd
import ast
from nltk.corpus import stopwords

pd.options.mode.chained_assignment = None

movies_df = pd.read_csv('datasets/tmdb_5000_movies.csv')
credits_df = pd.read_csv("datasets/tmdb_5000_credits.csv")

credits_df.rename(columns={'movie_id':'id'}, inplace=True)
credits_df.drop(columns='title', inplace=True)

movies = movies_df.merge(credits_df, on='id')
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

def getWord(dict_list):
    name_list = []
    for item in ast.literal_eval(dict_list):
        name_list.append(item['name'])
    return name_list

def getCast(dict_list):
    cast_list = []
    count = 0
    for item in ast.literal_eval(dict_list):
        if count != 10:
            cast_list.append(item['name'])
            count += 1
    return cast_list

def getCrew(dict_list, job):
    crew_list = []
    for item in ast.literal_eval(dict_list):
        if item['job']==job:
            crew_list.append(item['name'])
    return crew_list

def removeStopwords(sentences):
    stopwords_english = set(stopwords.words('english'))
    new_sentences = [sentence for sentence in sentences if sentence not in stopwords_english]
    return new_sentences

movies['genres'] = movies['genres'].apply(getWord)
movies['keywords'] = movies['keywords'].apply(getWord)
movies['production_companies'] = movies['production_companies'].apply(getWord)
movies['spoken_languages'] = movies['spoken_languages'].apply(getWord)
movies['cast'] = movies['cast'].apply(getCast)
movies['director'] = movies['crew'].apply(getCrew, job='Director')
movies['DOP'] = movies['crew'].apply(getCrew, job='Director of Photography')
movies['producer'] = movies['crew'].apply(getCrew, job='Producer')
movies['editor'] = movies['crew'].apply(getCrew, job='Editor')
movies['screenplay'] = movies['crew'].apply(getCrew, job='Screenplay')
movies['original_music_composer'] = movies['crew'].apply(getCrew, job='Original Music Composer')
movies['title'] = change_duplicate_titles()

export_movies = movies[['id', 'title', 'tagline', 'vote_average', 'vote_count', 'genres', 'overview', 'director', 'cast', 'release_date']]

movies['overview'] = movies['overview'].apply(lambda x:x.lower())
movies['tagline'] = movies['tagline'].apply(lambda x:x.lower())
movies['overview'] = movies['overview'].apply(lambda x:str(x))
movies['overview'] = movies['overview'].apply(lambda x:x.split())
movies['overview'] = movies['overview'].apply(removeStopwords)
movies['tagline'] = movies['tagline'].apply(lambda x:str(x))
movies['tagline'] = movies['tagline'].apply(lambda x:x.split())
movies['tagline'] = movies['tagline'].apply(removeStopwords)

movies_tags = movies[['id', 'title']]
movies_tags['tags'] = movies['overview'] + movies['genres'] + movies['keywords'] + movies['tagline'] + movies['director'] + movies['cast'] + movies['producer'] + movies['production_companies'] + movies['screenplay'] + movies['DOP']

movies_tags['tags'] = movies_tags['tags'].apply(lambda x:" ".join(x))
movies_tags['tags'] = movies_tags['tags'].apply(lambda x:x.lower())

export_movies.to_pickle("model/export_movies.pkl")
movies_tags.to_pickle("model/movies_tags.pkl")
