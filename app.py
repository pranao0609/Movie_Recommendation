import streamlit as st
import pickle
import pandas as pd
import requests
import os

def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={os.getenv('TMDB_API_KEY', '83d09bdf8b934823853ec996d6df72e9')}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if "poster_path" in data and data["poster_path"]:
            return f"https://image.tmdb.org/t/p/w500/{data['poster_path']}"
    return "https://via.placeholder.com/500"

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommend_movies = []
    recommend_movies_poster = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommend_movies.append(movies.iloc[i[0]].title)
        recommend_movies_poster.append(fetch_poster(movie_id))
    return recommend_movies, recommend_movies_poster

# Load precomputed data
movies_list = pickle.load(open('movies.pkl', 'rb'))
movies = pd.DataFrame(movies_list)
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Streamlit UI
st.title('Movie Recommendation System')

option = st.selectbox(
    'Select a Movie to Get Recommendations:',
    movies['title'].values
)

if st.button('Recommend'):
    try:
        names, posters = recommend(option)
        cols = st.columns(5)
        for idx, col in enumerate(cols):
            with col:
                st.text(names[idx])
                st.image(posters[idx])
    except Exception as e:
        st.error("Something went wrong! Please try again.")
