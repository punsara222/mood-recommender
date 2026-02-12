# app.py
import streamlit as st
import pandas as pd

from recommender import recommend, movies, songs  # import data and function

st.set_page_config(page_title="Mood Recommender", layout="wide")

st.title("🎭 Mood-Based Recommender")
st.write("Find movies and songs based on your mood 💫")

# User selects content type
content_type = st.selectbox("What do you want?", ["Movie", "Song"])

# Mood and energy
mood = st.selectbox("Select Mood", sorted(movies["mood"].unique()))
energy = st.selectbox("Select Energy", ["low", "medium", "high"])

# For songs, let user select language
language = None
if content_type == "Song":
    language = st.selectbox("Select Language", sorted(songs["language"].unique()))

# Button to get recommendations
if st.button("Get Recommendations"):
    if content_type == "Movie":
        results = recommend("movie", mood, energy)
        st.subheader("🎬 Recommended Movies")
        if isinstance(results, str):
            st.write(results)
        else:
            for _, row in results.iterrows():
                col1, col2 = st.columns([1, 2])
                with col1:
                    if "image_url" in row and pd.notna(row["image_url"]):
                        st.image(row["image_url"], width=200)
                with col2:
                    st.write(f"### {row['title']}")
                    st.write(f"Genre: {row['genre']}")
                    st.write(f"Duration: {row['duration']}")
    else:  # Song
        results = songs[
            (songs["mood"] == mood) &
            (songs["energy"] == energy) &
            (songs["language"] == language)
        ]
        st.subheader("🎵 Recommended Songs")
        if results.empty:
            st.write("No match found. Try different mood, energy, or language.")
        else:
            for _, row in results.iterrows():
                st.write(f"### {row['song']}")
                st.write(f"Artist: {row['artist']}")
