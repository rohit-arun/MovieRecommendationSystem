import streamlit as st
import difflib
import requests
from preprocessing import export_movies
from similarity import similarity_score

vote_count_df = export_movies[['title', 'vote_count']]
vote_count_df.sort_values(by=['vote_count'], ascending=False, inplace=True)

st.set_page_config(
    page_title="Movie Recommendation System",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'About': 'A content-based movie recommendation system, built on Python using Streamlit and the TMDb API.'
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

def recommend(movie_title):
    movie_list = export_movies['title'].tolist()
    movie_match = difflib.get_close_matches(movie_title, movie_list)
    closest_match = movie_match[0]
    movie_index = export_movies[export_movies['title'] == closest_match].index[0]
    distances = similarity_score[movie_index]
    recommended_id = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:11]
    recommended_title = []
    recommended_title_posters = []
    recommended_plot = []
    recommended_release_date = []
    recommended_genres = []
    recommended_director = []
    recommended_cast = []
    recommended_rating = []
    for i in recommended_id:
        movie_id = export_movies.iloc[i[0]].id
        recommended_title.append(export_movies.iloc[i[0]].title)
        recommended_title_posters.append(get_poster(movie_id))
        recommended_rating.append(export_movies.iloc[i[0]].vote_average)
        recommended_plot.append(export_movies.iloc[i[0]].overview)
        recommended_release_date.append(export_movies.iloc[i[0]].release_date)
        recommended_genres.append(export_movies.iloc[i[0]].genres)
        recommended_director.append(export_movies.iloc[i[0]].director)
        recommended_cast.append(export_movies.iloc[i[0]].cast)
    flattened_recommended_director = [director_name for directors in recommended_director for director_name in directors]
    return [recommended_title, recommended_title_posters, recommended_rating, recommended_plot, recommended_release_date, recommended_genres, flattened_recommended_director, recommended_cast]

selected_movie = st.selectbox('Find movies similar to', vote_count_df['title'], index=0)

if st.button("Recommend"):
    with st.spinner('Recommending...'):
        recommendations = recommend(selected_movie)
    st.text('')
    st.subheader(f"Movies like '{selected_movie}'")
    st.text('')
    for j in range(0, 10):
        col1, col2 = st.columns(2)
        with col1:
            if recommendations[1][j]:
                st.image(recommendations[1][j])
        with col2:
            with st.expander('About', expanded=True):
                st.header(recommendations[0][j])

                st.metric(label='TMDb Score', value=f'{recommendations[2][j]}')

                st.subheader('Plot')
                st.write(recommendations[3][j])

                st.subheader('Release Date')
                st.write(recommendations[4][j])

                st.subheader('Genres')
                genres = ''
                for movie_genre in recommendations[5][j]:
                    genres = genres + ', ' + movie_genre
                st.write(genres[2:])

                st.subheader('Director')
                st.write(recommendations[6][j])

                st.subheader('Cast')
                cast = ''
                for movie_cast in recommendations[7][j]:
                    cast = cast + ', ' + movie_cast
                st.write(cast[2:])
        st.write('')