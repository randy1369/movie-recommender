import streamlit as st
import pickle
import requests

movies = pickle.load(open("movies_list.pkl", "rb"))
similarity = pickle.load(open("similarity.pkl", "rb"))
movies_list = movies['title'].values

st.header("Movie Recommender System")
selectvalue = st.selectbox("Select Movie from Dropdown", movies_list)


def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=".format(movie_id)
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if 'poster_path' in data:
            poster = data['poster_path']
            full_path = "https://image.tmdb.org/t/p/w500/" + poster
            return full_path
        else:
            return None  # Poster path not available
    else:
        return None  # Error in API request

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distance = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda vector:vector[1])
    recommend_movies = []
    recommend_poster = []
    for i in distance[1:6]:
        movies_id = movies.iloc[i[0]].id
        poster_url = fetch_poster(movies_id)
        if poster_url:
            recommend_movies.append(movies.iloc[i[0]].title)
            recommend_poster.append(poster_url)
    return recommend_movies, recommend_poster



if st.button("Show Recommend"):
    movie_name, movie_poster = recommend(selectvalue)
    col1,col2,col3,col4,col5 = st.columns(5)
    with col1:
        st.text(movie_name[0])
        st.image(movie_poster[0])
    with col2:
        st.text(movie_name[1])
        st.image(movie_poster[1])
    with col3:
        st.text(movie_name[2])
        st.image(movie_poster[2])
    with col4:
        st.text(movie_name[3])
        st.image(movie_poster[3])
    with col5:
        st.text(movie_name[4])
        st.image(movie_poster[4])
  
