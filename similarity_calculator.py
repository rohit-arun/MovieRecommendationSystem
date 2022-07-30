import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity 

export_movies = pd.read_pickle('model/export_movies.pkl')
movies_tags = pd.read_pickle('model/movies_tags.pkl')

vectorizer = CountVectorizer()
feature_vectors = vectorizer.fit_transform(movies_tags['tags'])
similarity = cosine_similarity(feature_vectors)