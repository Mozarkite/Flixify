# Flixify 🎬

Flixify is a Streamlit web app that recommends movies to users using the TMDB API.  
Search for a movie, see its details, and get recommendations or explore upcoming films. 

You can access this Web App at : https://flixify.streamlit.app/

---

## ❓ Why use TMDB API?

Originally, I planned on using the Spotify API and applying cosine similarity to create a recommendation system based on vectors.
Unfortunately, Spotify removed features from songs such as danceability, tone, mood, etc.  

Because of this, I decided to go with **TMDB**, which allows me to fetch information such as:  
Movie titles •  Actors •  Overviews •  Genres •  Recommendations •  Upcoming movies  

---

## 🚀 Features

- 🔍 Search for a movie by name  
- 🎞️ View movie details: poster, release date, genres, cast, overview  
- 🤝 Get top recommendations based on the selected movie  
- 🔮 Explore a random selection of upcoming films  
- 📊 Interactive charts (bar, pie) to display popularity, average votes, vote counts  

---

## 🧰 Tech Stack & Dependencies

- 🐍 Python  
- 🎈 Streamlit (frontend / UI)  
- 🌐 Requests (for TMDB API calls)  
- 🗂️ Pandas (data handling)  
- 📊 Plotly (for interactive visualizations)  
- 🎬 TMDB API (source of movie data)  

Your `requirements.txt` should include:
- streamlit
- pandas
- plotly
- requests

---

## 🎯 Project Purpose  

- 🔑 Showcase usability and implementation of APIs  
- 📡 Fetch data and display it in a clean UI  
- 📊 Use fetched data to create meaningful visualisations  

---
