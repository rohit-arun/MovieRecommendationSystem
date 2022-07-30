import streamlit as st
import difflib
import requests
from similarity_calculator import similarity, export_movies

vote_count_df = export_movies[['title', 'vote_count']]
vote_count_sorted = vote_count_df.sort_values(by=['vote_count'], ascending=False)

st.set_page_config(
    page_title="Movie Recommendation System",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'About': 'A content-based movie recommendation system, built on Python using Streamlit and the TMDb API.'
    }
)

st.title('MOVIE RECOMMENDATION SYSTEM')

@st.cache(show_spinner=False, suppress_st_warning=True)
def get_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    response = requests.get(url)
    data = response.json()
    poster_path = data['poster_path']
    if poster_path:
        path = "https://image.tmdb.org/t/p/original" + poster_path
        return path
    else:
        pass

def recommend(movie_title):
    movie_list = export_movies['title'].tolist()
    movie_match = difflib.get_close_matches(movie_title, movie_list)
    closest_match = movie_match[0]
    movie_index = export_movies[export_movies['title'] == closest_match].index[0]
    distances = similarity[movie_index]
    recommended_id = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:11]
    title = []
    title_posters = []
    tagline = []
    rating = []
    genres = []
    plot = []
    directors = []
    cast = []
    release_date = []
    for i in recommended_id:
        movie_id = export_movies.iloc[i[0]].id
        title.append(export_movies.iloc[i[0]].title)
        title_posters.append(get_poster(movie_id))
        tagline.append(export_movies.iloc[i[0]].tagline)
        rating.append(export_movies.iloc[i[0]].vote_average)
        genres.append(export_movies.iloc[i[0]].genres)
        plot.append(export_movies.iloc[i[0]].overview)
        directors.append(export_movies.iloc[i[0]].director)
        cast.append(export_movies.iloc[i[0]].cast)
        release_date.append(export_movies.iloc[i[0]].release_date)
    details = [title, title_posters, tagline, rating, genres, plot, directors, cast, release_date]
    return details

selected_movie = st.selectbox('Find movies similar to', vote_count_sorted['title'], index=0)

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
            else:
                pass
        with col2:
            with st.expander('About', expanded=True):
                st.header(recommendations[0][j])

                st.write(recommendations[2][j])

                st.metric(label='TMDb Score', value=f'{recommendations[3][j]}')

                st.subheader('Genres')
                genres = ''
                for movie_genre in recommendations[4][j]:
                    genres = genres + ', ' + movie_genre
                st.write(genres[2:])

                st.subheader('Plot')
                st.write(recommendations[5][j])

                st.subheader('Crew')
                st.caption('- Director(s)')
                job = ''
                for movie_job in recommendations[6][j]:
                    job = job + ', ' + movie_job
                st.write(job[2:])

                st.caption('- Cast')
                job = ''
                for movie_job in recommendations[7][j]:
                    job = job + ', ' + movie_job
                st.write(job[2:])

                st.subheader('Release Date')
                st.write(recommendations[8][j])
        st.write('')