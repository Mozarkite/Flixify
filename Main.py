import requests
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.io as pio
import random


API_KEY = "7da0188c1da7e6d0b2dd8b7950cf57f1"
BASE_URL = "https://api.themoviedb.org/3"

# -------------------------
# API Functions
# -------------------------

def search_movie(movie_name):
    url = f"{BASE_URL}/search/movie"
    params = {"api_key": API_KEY, "query": movie_name}
    response = requests.get(url, params=params)
    data = response.json()

    if data["results"]:
        movie = data["results"][0]
        genre_names = [all_genres.get(gid) for gid in movie.get("genre_ids", [])]
        movie["genre_names"] = genre_names

        movie_id = movie["id"]
        movie["cast_names"] = get_actors(movie_id)
        return movie
    else:
        return None
    
def search_movie_by_id(movie_name):
    url = f"{BASE_URL}/search/movie"
    params = {"api_key": API_KEY, "query": movie_name}
    response = requests.get(url, params=params)
    data = response.json()

    if data["results"]:
        movie_id = movie["id"]
        return movie_id
    else:
        return None


def get_genres():
    url = f"{BASE_URL}/genre/movie/list"
    params = {"api_key": API_KEY}
    response = requests.get(url, params=params)
    data = response.json()
    return {genre["id"]: genre["name"] for genre in data["genres"]}


def get_actors(movie_id):
    url = f"{BASE_URL}/movie/{movie_id}/credits"
    params = {"api_key": API_KEY}
    response = requests.get(url, params=params)
    data = response.json()
    
    cast = data.get("cast", [])
    actor_names = [actor["name"] for actor in cast[:5]]
    return actor_names

def get_reccomendations(movie_id) :
    
    rec_url= f"{BASE_URL}/movie/{movie_id}/recommendations"
    params = {"api_key": API_KEY}
    response = requests.get(rec_url, params=params)
    data = response.json()

    rec_response = requests.get(rec_url, params = params)
    df = pd.DataFrame(rec_response.json()["results"])

    top10_recommendations= df['original_title'].value_counts()[:6].index
    top10_reccomendations_posters = df['poster_path'].value_counts()[:6].index


    #st.write(top10_recommendations)
    #st.write(top10_reccomendations_posters)


    cols = st.columns(3)
    cols2 = st.columns(3)

    
    #Displaying first recommendations
    for col, posters in zip(cols, top10_reccomendations_posters[:3]):
        with col :
            poster_url_1 = f"https://image.tmdb.org/t/p/w500{posters}" if posters else "https://via.placeholder.com/200x300?text=No+Poster"

            st.image(poster_url_1, width=200)

   

    #Displaying the other 3 reccomendations
    for col, posters in zip(cols, top10_reccomendations_posters[3:]):
        with col :
            poster_url_1 = f"https://image.tmdb.org/t/p/w500{posters}" if posters else "https://via.placeholder.com/200x300?text=No+Poster"

            st.image(poster_url_1, width=200)

    #st.divider()

    #Configs for the graph : sorting a dataframe by title, popularity and vote average
    top_df = df[df["original_title"].isin(top10_recommendations)][["original_title","popularity","vote_average","vote_count"]]

    top_df = top_df.sort_values("popularity",ascending=True)
    top_df_2 = top_df.sort_values("vote_count",ascending=True)


    graph_df = pd.DataFrame(

        {
            "Movies Reccomended" : top_df["original_title"],
            "popularity" : top_df["popularity"],
            "Average Vote": top_df["vote_average"]

        }
    
    )

    st.divider()
    st.markdown("<h3 style='text-align: center; color: lightblue;'>Statistics</h3>", unsafe_allow_html=True)
    st.write("")
    

    st.write(f"**Average Vote and popularity by Reccomendation**")
    #Display the graph
    st.bar_chart(

        graph_df,
        x = "Movies Reccomended",
        y = ["popularity","Average Vote"],
        color = ["#2C3E50","#87CEEB"] # Dark Slate 

    )

    fig = px.pie(
        top_df_2,
        values ="vote_count",
        names = "original_title",
        title = "Vote Count by Reccomendation",
        color_discrete_sequence = [
            "#2F4F4F",  # Dark Slate Gray
            "#708090",  # Slate Gray
            "#778899",  # Light Slate Gray
            "#1E3A5F",  # Dark Blue Slate
            "#3B5998",  # Classic Slate Blue
            "#6A5ACD" ] # Slate Blue

    )

    st.plotly_chart(fig)

    #st.dataframe(df)



def get_new_movies() :

    url = "https://api.themoviedb.org/3/movie/upcoming?language=en-US&page=1"

    params = {"api_key": API_KEY}

    response = requests.get(url, params = params)

    df_new_movies = pd.DataFrame(response.json()["results"])

    top10_recommendations= df_new_movies['original_title'].value_counts()[:6].index
    top10_reccomendations_posters = list(df_new_movies['poster_path'].value_counts()[:100].index)

    cols = st.columns(4)
    
    random_posters = random.sample(top10_reccomendations_posters, 4)


    #Displaying first recommendations
    for col, posters in zip(cols, random_posters):
        with col :
            poster_url_1 = f"https://image.tmdb.org/t/p/w500{posters}" if posters else "https://via.placeholder.com/200x300?text=No+Poster"

            st.image(poster_url_1, width=200)


all_genres = get_genres()

# -------------------------
# Streamlit Config
# -------------------------


hide_decoration_bar_style = '''<style>header {visibility: hidden;}</style>'''
st.markdown(hide_decoration_bar_style, unsafe_allow_html=True)
# Design hide "made with streamlit" footer menu area
hide_streamlit_footer = """<style>#MainMenu {visibility: hidden;}
                        footer {visibility: hidden;}</style>"""
st.markdown(hide_streamlit_footer, unsafe_allow_html=True)


st.set_page_config(page_title="Flixify", page_icon="🎬", layout="centered")

#title and banner
st.image("Assets/TheWorld.gif", width=800)
st.title(":blue[_Flixify_] - Where Movies Find You.")
st.divider()

#Setting up columns
col1, col2 = st.columns([1, 2], vertical_alignment="top")

with col1:
    movie_name = st.text_input("Enter a movie name:", width=200)
    poster_ph = st.empty()

with col2:
    title_ph = st.empty()
    release_ph = st.empty()
    genres_ph = st.empty()
    actors_ph = st.empty()
    overview_ph = st.empty()

# Default placeholders
poster_ph.image("Assets/placeholder.jpg", width=200)
title_ph.subheader("Movie Title --")
release_ph.write("📅 Release Date: ---")
actors_ph.write("🎭 Actors ---")
genres_ph.write("📕 Genres: ---")

# When user searches
selected_title = None
searched_movie = None

if movie_name:
    movie = search_movie(movie_name)
    if movie:
        selected_title = movie.get('title')
        searched_movie = movie  # Save searched movie for later
        movie_id = movie.get('id')
        release_date = movie.get("release_date", "NA")
        overview = movie.get("overview", "NA")
        poster_path = movie.get("poster_path")
        genres = movie.get("genre_names", [])
        actors = get_actors(movie_id)

        poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else "https://via.placeholder.com/200x300?text=No+Poster"

        poster_ph.image(poster_url, width=200)
        title_ph.subheader(selected_title)
        release_ph.write(f"📅 Release Date - {release_date}")
        genres_ph.write("📕 Genres - " + (" - ".join(genres) if genres else "NA"))
        actors_ph.write(f"🎭 Actors - {', '.join(actors) if actors else 'NA'}")
        overview_ph.write(overview)
    else:
        poster_ph.image("Assets/placeholder.jpg", width=200)
        title_ph.subheader("Movie Title --")
        release_ph.write("📅 Release Date: ---")
        actors_ph.write("🎭 Actors ---")
        genres_ph.write("📕 Genres: ---")

#Divider for the next section
st.divider()


if movie_name :

    option = st.selectbox(
        "What would you like to view?",
        ("Reccomendations","Upcoming Movies"),
        index=None,
    placeholder="Select options available..."

    )
    if option == "Reccomendations":

        st.markdown("<h2 style='text-align: center; color: lightblue;'>Reccomendations </h2>", unsafe_allow_html=True)
        movie_identity = search_movie_by_id(movie_name)
        get_reccomendations(movie_identity)
        st.divider()


    elif option == "Upcoming Movies" :
        st.markdown("<h2 style='text-align: center; color: lightblue;'>Upcoming Movies </h2>", unsafe_allow_html=True)
        get_new_movies()
        st.divider()

    
    

