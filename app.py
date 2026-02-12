import streamlit as st
import pandas as pd

movies = pd.read_csv("data/movies.csv")
songs = pd.read_csv("data/songs.csv")

st.set_page_config(page_title="Mood Recommender", layout="wide")

st.title("🎭 Mood-Based Recommender")
st.write("Find movies and songs based on your mood 💫")

content_type = st.selectbox("What do you want?", ["Movie", "Song"])
mood = st.selectbox("Select Mood", sorted(movies["mood"].unique()))
energy = st.selectbox("Select Energy", ["low", "medium", "high"])

if content_type == "Movie":
    results = movies[
        (movies["mood"] == mood) &
        (movies["energy"] == energy)
    ]

    st.subheader("🎬 Recommended Movies")

    for _, row in results.iterrows():
        col1, col2 = st.columns([1, 2])
        with col1:
            if "image_url" in movies.columns:
                st.image(row["image_url"], width=200)
        with col2:
            st.write(f"### {row['title']}")
            st.write(f"Genre: {row['genre']}")
            st.write(f"Duration: {row['duration']}")

else:
    language = st.selectbox("Select Language", sorted(songs["language"].unique()))

    results = songs[
        (songs["mood"] == mood) &
        (songs["energy"] == energy) &
        (songs["language"] == language)
    ]

    st.subheader("🎵 Recommended Songs")

    for _, row in results.iterrows():
        st.write(f"### {row['song']}")
        st.write(f"Artist: {row['artist']}")
