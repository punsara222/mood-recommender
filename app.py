# app.py
import streamlit as st
import pandas as pd
from recommender import recommend, movies, songs

st.set_page_config(page_title="Mood Recommender", page_icon="🎭", layout="wide")

# ---------- Theme Toggle (Top Right) ----------
theme_mode = st.toggle("🌙 Dark Mode", value=True)

# ---------- Background Styling ----------
if theme_mode:
    background_style = """
    background: linear-gradient(-45deg, #141e30, #243b55, #1f1c2c, #928DAB);
    background-size: 400% 400%;
    animation: gradient 12s ease infinite;
    """
    text_color = "white"
    box_bg = "rgba(30,30,30,0.9)"
    card_bg = "#1e1e1e"
else:
    background_style = """
    background: linear-gradient(-45deg, #667eea, #764ba2, #6dd5ed, #2193b0);
    background-size: 400% 400%;
    animation: gradient 12s ease infinite;
    """
    text_color = "black"
    box_bg = "rgba(255,255,255,0.9)"
    card_bg = "white"

# ---------- Custom CSS ----------
st.markdown(f"""
<style>

@keyframes gradient {{
    0% {{ background-position: 0% 50%; }}
    50% {{ background-position: 100% 50%; }}
    100% {{ background-position: 0% 50%; }}
}}

.stApp {{
    {background_style}
}}

.main-title {{
    font-size: 45px;
    font-weight: bold;
    text-align: center;
    color: {text_color};
}}

.sub-text {{
    text-align: center;
    font-size: 18px;
    color: {text_color};
    margin-bottom: 30px;
}}

/* -------- TOP INPUT BOX -------- */

.top-box {{
    width: 85%;
    margin: auto;
    padding: 30px;
    border-radius: 20px;
    background: {box_bg};
    box-shadow: 0 15px 40px rgba(0,0,0,0.3);
    margin-bottom: 40px;
}}

/* -------- POSTER ROW -------- */

.poster-row {{
    display: flex;
    justify-content: center;
    gap: 25px;
    margin-bottom: 40px;
}}

.poster-row img {{
    width: 180px;
    border-radius: 18px;
    transition: all 0.4s ease;
    box-shadow: 0 15px 35px rgba(0,0,0,0.4);
}}

.poster-row img:hover {{
    transform: scale(1.1) translateY(-10px);
    box-shadow: 0 25px 50px rgba(0,0,0,0.6);
}}

/* -------- RESULT CARD -------- */

.card {{
    padding: 20px;
    border-radius: 15px;
    background-color: {card_bg};
    box-shadow: 0px 6px 18px rgba(0,0,0,0.3);
    margin-bottom: 20px;
}}

.stButton>button {{
    background-color: #ff4b4b;
    color: white;
    font-size: 16px;
    border-radius: 10px;
    padding: 10px 20px;
    border: none;
}}

</style>
""", unsafe_allow_html=True)

# ---------- Title ----------
st.markdown('<div class="main-title">🎭 Mood-Based Recommender</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-text">Find movies and songs based on your mood 💫</div>', unsafe_allow_html=True)

# ---------- TOP INPUT BOX ----------
st.markdown('<div class="top-box">', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    content_type = st.selectbox("What do you want?", ["Movie", "Song"])

with col2:
    mood = st.selectbox("Select Mood", sorted(movies["mood"].unique()))

with col3:
    energy = st.selectbox("Select Energy", ["low", "medium", "high"])

language = None
if content_type == "Song":
    language = st.selectbox("Select Language", sorted(songs["language"].unique()))

st.write("")
get_btn = st.button("✨ Get Recommendations")

st.markdown('</div>', unsafe_allow_html=True)

# ---------- POSTER ROW (Below Box) ----------
st.markdown("""
<div class="poster-row">
    <img src="https://image.tmdb.org/t/p/w500/uDO8zWDhfWwoFdKS4fzkUJt0Rf0.jpg">
    <img src="https://image.tmdb.org/t/p/w500/rAiYTfKGqDCRIIqoNMq72uFHeDv.jpg">
    <img src="https://image.tmdb.org/t/p/w500/qJ2tW6WMUDux911r6m7haRef0WH.jpg">
    <img src="https://image.tmdb.org/t/p/w500/udDclJoHjfjb8Ekgsd4FDteOkCU.jpg">
    <img src="https://image.tmdb.org/t/p/w500/6DrHO1jr3qVrViUO6s6kFiAGM7.jpg">
</div>
""", unsafe_allow_html=True)

# ---------- Results ----------
if get_btn:

    st.write(f"### Showing results for: **{mood.capitalize()} | {energy.capitalize()} Energy**")
    st.write("")

    if content_type == "Movie":
        results = recommend("movie", mood, energy)
    else:
        results = songs[
            (songs["mood"] == mood) &
            (songs["energy"] == energy) &
            (songs["language"] == language)
        ]

    if isinstance(results, str) or results.empty:
        st.warning("No matching results found.")
    else:
        for _, row in results.iterrows():
            st.markdown('<div class="card">', unsafe_allow_html=True)
            col1, col2 = st.columns([1, 2])

            with col1:
                if "image_url" in row and pd.notna(row["image_url"]):
                    st.image(row["image_url"], use_column_width=True)

            with col2:
                if content_type == "Movie":
                    st.markdown(f"### 🎬 {row['title']}")
                    st.write(f"Genre: {row['genre']}")
                    st.write(f"Duration: {row['duration']}")
                else:
                    st.markdown(f"### 🎵 {row['song']}")
                    st.write(f"Artist: {row['artist']}")
                    st.write(f"Language: {row['language']}")

            st.markdown('</div>', unsafe_allow_html=True)
