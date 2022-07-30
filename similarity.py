from preprocessing import movies_tags
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity 

vectorizer = CountVectorizer()
feature_vectors = vectorizer.fit_transform(movies_tags['tags'])
similarity_score = cosine_similarity(feature_vectors)
