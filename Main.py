import requests
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.io as pio
import random


API_KEY = st.secrets["API_KEY"]
BASE_URL = st.secrets["BASE_URL"]

# -------------------------
# API Functions##
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

#Function that searches by 
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

#Function that gets the genres of that movie 
def get_genres():
    url = f"{BASE_URL}/genre/movie/list"
    params = {"api_key": API_KEY}
    response = requests.get(url, params=params)
    data = response.json()
    return {genre["id"]: genre["name"] for genre in data["genres"]}

#Function that returns the actors in the movie
def get_actors(movie_id):
    url = f"{BASE_URL}/movie/{movie_id}/credits"
    params = {"api_key": API_KEY}
    response = requests.get(url, params=params)
    data = response.json()
    
    cast = data.get("cast", [])
    actor_names = [actor["name"] for actor in cast[:5]]
    return actor_names

#Function that gets the reccomendation
def get_reccomendations(movie_id):
    rec_url = f"{BASE_URL}/movie/{movie_id}/recommendations"
    params = {"api_key": API_KEY}
    response = requests.get(rec_url, params=params)
    data = response.json()
    df = pd.DataFrame(data.get("results", []))

    if df.empty:
        st.markdown("<h4 style='text-align: center; color: White;'>No recommendations found.</h4>", unsafe_allow_html=True)
        return

    # Take top 6 recommendations
    top6 = df.head(6)

    titles = top6['original_title'].tolist()
    posters = top6['poster_path'].tolist()

    # Display posters in two rows of 3
    cols1 = st.columns(3)
    cols2 = st.columns(3)

    #iterate up until 3
    for col, poster in zip(cols1, posters[:3]):
        poster_url = f"https://image.tmdb.org/t/p/w500{poster}" if poster else "https://via.placeholder.com/200x300?text=No+Poster"
        col.image(poster_url, width=200)

    #iterate from 3 onwards
    for col, poster in zip(cols2, posters[3:]):
        poster_url = f"https://image.tmdb.org/t/p/w500{poster}" if poster else "https://via.placeholder.com/200x300?text=No+Poster"
        col.image(poster_url, width=200)

    # Statistics gathered as a df
    top_df = top6[["original_title", "popularity", "vote_average", "vote_count","original_language"]]
    top_df_sorted = top_df.sort_values("popularity", ascending=True)
    top_df_sorted_count = top_df.sort_values("vote_count", ascending=True)

    #dataframe of the 3 columns
    graph_df = pd.DataFrame({
        "Movies Reccomended": top_df_sorted["original_title"],
        "popularity": top_df_sorted["popularity"],
        "Average Vote": top_df_sorted["vote_average"]
    })

    #bar chart configs
    st.divider()
    st.markdown("<h3 style='text-align: center; color: lightblue;'>Statistics</h3>", unsafe_allow_html=True)
    st.write("**Average Vote and popularity by Reccomendation**")
    st.bar_chart(graph_df, x="Movies Reccomended", y=["popularity", "Average Vote"], color=["#2C3E50","#87CEEB"])

    #pie chart configs
    fig = px.pie(
        top_df_sorted_count,
        values="vote_count",
        names="original_title",
        title="Vote Count by Reccomendation",
        color_discrete_sequence=["#2F4F4F","#708090","#778899","#1E3A5F","#3B5998","#6A5ACD"]
    )
    st.plotly_chart(fig)

        
    #dataframe for debugging
    #st.dataframe(df)
    st.write(top_df[['original_title', 'original_language']])



def get_new_movies():
    url = "https://api.themoviedb.org/3/movie/upcoming?language=en-US&page=1"
    params = {"api_key": API_KEY}
    response = requests.get(url, params=params)

    #dataframe to hold new movies
    df_new_movies = pd.DataFrame(response.json()["results"])

    # Get top 100 posters and randomly pick 4
    top_posters = df_new_movies[df_new_movies['poster_path'].notna()].head(100)
    random_upcoming= top_posters.sample(4)
    
    #creates a list of all 4 random posters
    top4_posters = list(random_upcoming['poster_path'].head(4))

    # Create 4 columns for display
    cols = st.columns(4)

    

    # Display the posters
    for col, poster in zip(cols, top4_posters):
        poster_url = f"https://image.tmdb.org/t/p/w500{poster}" if poster else "https://via.placeholder.com/200x300?text=No+Poster"
        with col:
            st.image(poster_url, width=200)
        
    
    st.divider()

    #Dataframe of the title, release date and the original language
    st.dataframe(random_upcoming[['original_title',"release_date",'original_language']])



    graph_df = pd.DataFrame({
        "Movies": random_upcoming["original_title"],
        "popularity": random_upcoming["popularity"],
        "Average Vote": random_upcoming["vote_average"],
    })
    
    #pie chart configs
    fig = px.pie(
       graph_df,
        values="Average Vote",
        names="Movies",
        title="Vote Count For Upcoming Movies",
        color_discrete_sequence=["#708090","#1E3A5F","#3B5998","#6A5ACD"]
    )
    st.plotly_chart(fig)


    st.write("**Popularity of Upcoming Movies**")
    st.bar_chart(graph_df, x="Movies", y=["popularity"], color=["#2C3E50"])



    
#List of all of the genres
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
st.divider()

# When user searches
selected_title = None
searched_movie = None

if movie_name:
    movie = search_movie(movie_name)
    
    #if the movie does exist in the database
    if movie:

        selected_title = movie.get('title')
        searched_movie = movie  # Save searched movie for later
        movie_id = movie.get('id')
        release_date = movie.get("release_date", "NA")
        overview = movie.get("overview", "NA")
        poster_path = movie.get("poster_path")
        genres = movie.get("genre_names", [])
        actors = get_actors(movie_id)

        #change image of th poster to placeholder
        poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else "https://via.placeholder.com/200x300?text=No+Poster"

        poster_ph.image(poster_url, width=200)
        title_ph.subheader(selected_title)
        release_ph.write(f"📅 Release Date - {release_date}")
        genres_ph.write("📕 Genres - " + (" - ".join(genres) if genres else "NA"))
        actors_ph.write(f"🎭 Actors - {', '.join(actors) if actors else 'NA'}")
        overview_ph.write(overview)
    
    #placeholders
    else:
        poster_ph.image("Assets/placeholder.jpg", width=200)
        title_ph.subheader("Movie Title --")
        release_ph.write("📅 Release Date: ---")
        actors_ph.write("🎭 Actors ---")
        genres_ph.write("📕 Genres: ---")

    #if the movie does not exist 
    if movie is None :
        
        #Warning if the movie is invalid
        st.warning("Movie Not Found in Database, Plase Enter Valid Movie.")
        
        
    else :
        
        if movie_name :

            #selection box configs
            option = st.selectbox(
                "What would you like to view?",
                ("Reccomendations","Upcoming Movies"),
                index=None,
            placeholder="Select options available..."

            )
            
            #checks if option is reccomendation
            if option == "Reccomendations":

                st.markdown("<h2 style='text-align: center; color: lightblue;'>Reccomendations </h2>", unsafe_allow_html=True)
                movie_identity = search_movie_by_id(movie_name)
                get_reccomendations(movie_identity)
                st.divider()


            #checks if option is upcoming movies
            elif option == "Upcoming Movies" :

                st.markdown("<h2 style='text-align: center; color: lightblue;'>Upcoming Movies </h2>", unsafe_allow_html=True)
                get_new_movies()
                st.divider()




    
    

