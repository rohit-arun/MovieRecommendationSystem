import streamlit as st
import pandas as pd
import pickle
import difflib
import requests

movies_df = pd.read_pickle('model/movies.pkl')
vote_count_df = pd.read_pickle('model/vote_count_df.pkl')
similarity = pickle.load(open('model/similarity.pkl', 'rb'))

vote_count_df.sort_values(by=['vote_count'], ascending=False, inplace=True)

st.set_page_config(
    page_title="Movie Recommendation System",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'About': "This app was made by Rohit Arun."
    }
)

st.title('MOVIE RECOMMENDATION SYSTEM')


@st.cache(show_spinner=False)
def get_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    response = requests.get(url)
    data = response.json()
    poster_path = data['poster_path']
    if poster_path:
        path = "http://image.tmdb.org/t/p/original" + poster_path
        return path
    else:
        pass


@st.cache(show_spinner=False)
def recommend(movie_title):
    movie_list = movies_df['title'].tolist()
    movie_match = difflib.get_close_matches(movie_title, movie_list)
    closest_match = movie_match[0]
    movie_index = movies_df[movies_df['title'] == closest_match].index[0]
    distances = similarity[movie_index]
    recommended_id = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:21]
    recommended_title = []
    recommended_title_posters = []
    for i in recommended_id:
        movie_id = movies_df.iloc[i[0]].id
        recommended_title.append(movies_df.iloc[i[0]].title)
        recommended_title_posters.append(get_poster(movie_id))
    return recommended_title, recommended_title_posters


selected_movie = st.selectbox(
        'Find movies similar to',
        vote_count_df['title'], index=0)

if st.button("Recommend"):
    with st.spinner('Recommending...'):
        recommendations, recommendations_posters = recommend(selected_movie)
    st.text('')
    st.subheader(f"Movies like '{selected_movie}'")
    st.text('')
    for j in range(0, 20, 4):
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.text(recommendations[j])
            if recommendations_posters[j]:
                st.image(recommendations_posters[j])
        with col2:
            st.text(recommendations[j + 1])
            if recommendations_posters[j+1]:
                st.image(recommendations_posters[j + 1])
        with col3:
            st.text(recommendations[j + 2])
            if recommendations_posters[j+2]:
                st.image(recommendations_posters[j + 2])
        with col4:
            st.text(recommendations[j + 3])
            if recommendations_posters[j+3]:
                st.image(recommendations_posters[j + 3])
        st.text('')
