# app.py
import streamlit as st
import pandas as pd
from recommender import recommend, movies, songs

st.set_page_config(page_title="Mood Recommender", page_icon="🎭", layout="wide")
theme_mode = st.sidebar.toggle("🌙 Dark Mode", value=True)

# ---------- Custom Styling ----------
if theme_mode:
    background_style = """
    background: linear-gradient(-45deg, #141e30, #243b55, #1f1c2c, #928DAB);
    background-size: 400% 400%;
    animation: gradient 12s ease infinite;
    """
    text_color = "white"
    card_bg = "#1e1e1e"
else:
    background_style = """
    background: linear-gradient(-45deg, #667eea, #764ba2, #6dd5ed, #2193b0);
    background-size: 400% 400%;
    animation: gradient 12s ease infinite;
    """
    text_color = "black"
    card_bg = "white"

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
    font-size: 42px;
    font-weight: bold;
    text-align: center;
    color: {text_color};
}}

.sub-text {{
    text-align: center;
    font-size: 18px;
    color: {text_color};
}}

/* ----------- CAROUSEL STYLE ----------- */

.carousel {{
    position: relative;
    width: 100%;
    height: 400px;
    margin-top: 40px;
    perspective: 1000px;
}}

.carousel-track {{
    position: relative;
    width: 100%;
    height: 100%;
}}

.carousel img {{
    position: absolute;
    top: 50%;
    left: 50%;
    width: 250px;
    border-radius: 15px;
    transform: translate(-50%, -50%);
    transition: all 1s ease;
    opacity: 0;
}}

/* Center */
.carousel img:nth-child(3) {{
    transform: translate(-50%, -50%) scale(1.2);
    z-index: 3;
    opacity: 1;
}}

/* Left */
.carousel img:nth-child(2) {{
    transform: translate(-120%, -50%) scale(0.9);
    z-index: 2;
    opacity: 0.7;
}}

/* Right */
.carousel img:nth-child(4) {{
    transform: translate(20%, -50%) scale(0.9);
    z-index: 2;
    opacity: 0.7;
}}

/* Hidden sides */
.carousel img:nth-child(1),
.carousel img:nth-child(5) {{
    transform: translate(-50%, -50%) scale(0.8);
    opacity: 0;
}}

/* ----------- CARD STYLE ----------- */

.card {{
    padding: 20px;
    border-radius: 15px;
    background-color: {card_bg};
    box-shadow: 0px 6px 18px rgba(0,0,0,0.3);
    margin-bottom: 20px;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}}

.card:hover {{
    transform: scale(1.03);
    box-shadow: 0px 10px 25px rgba(0,0,0,0.4);
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
st.write("")

# ---------- Carousel Section ----------
st.markdown("""
<div class="carousel">
    <div class="carousel-track">
        <img src="https://image.tmdb.org/t/p/w500/uDO8zWDhfWwoFdKS4fzkUJt0Rf0.jpg">
        <img src="https://image.tmdb.org/t/p/w500/rAiYTfKGqDCRIIqoNMq72uFHeDv.jpg">
        <img src="https://image.tmdb.org/t/p/w500/qJ2tW6WMUDux911r6m7haRef0WH.jpg">
        <img src="https://image.tmdb.org/t/p/w500/udDclJoHjfjb8Ekgsd4FDteOkCU.jpg">
        <img src="https://image.tmdb.org/t/p/w500/6DrHO1jr3qVrViUO6s6kFiAGM7.jpg">
    </div>
</div>
""", unsafe_allow_html=True)


# ---------- Sidebar ----------
st.sidebar.header("🎯 Choose Your Preferences")

content_type = st.sidebar.selectbox("What do you want?", ["Movie", "Song"])
mood = st.sidebar.selectbox("Select Mood", sorted(movies["mood"].unique()))
energy = st.sidebar.selectbox("Select Energy", ["low", "medium", "high"])

language = None
if content_type == "Song":
    language = st.sidebar.selectbox("Select Language", sorted(songs["language"].unique()))

st.sidebar.write("---")
get_btn = st.sidebar.button("✨ Get Recommendations")

# Mood Emojis
mood_emoji = {
    "happy": "😄",
    "sad": "😢",
    "romantic": "💖",
    "motivated": "💪",
    "excited": "🤩",
    "calm": "😌",
    "bored": "😴",
    "thoughtful": "🤔"
}

# ---------- Results ----------
if get_btn:
    st.write(f"### Showing results for: **{mood.capitalize()} {mood_emoji.get(mood,'')} | {energy.capitalize()} Energy**")
    st.write("")

    if content_type == "Movie":
        results = recommend("movie", mood, energy)
        st.subheader("🎬 Recommended Movies")

        if isinstance(results, str):
            st.warning(results)
        else:
            for _, row in results.iterrows():
                st.markdown('<div class="card">', unsafe_allow_html=True)
                col1, col2 = st.columns([1, 2])

                with col1:
                    if "image_url" in row and pd.notna(row["image_url"]):
                        st.image(row["image_url"], use_column_width=True)

                with col2:
                    st.markdown(f"### {row['title']}")
                    st.write(f"**Genre:** {row['genre']}")
                    st.write(f"**Duration:** {row['duration']}")

                st.markdown('</div>', unsafe_allow_html=True)

    else:
        results = songs[
            (songs["mood"] == mood) &
            (songs["energy"] == energy) &
            (songs["language"] == language)
        ]

        st.subheader("🎵 Recommended Songs")

        if results.empty:
            st.warning("No match found. Try different mood, energy, or language.")
        else:
            for _, row in results.iterrows():
                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.markdown(f"### 🎵 {row['song']}")
                st.write(f"**Artist:** {row['artist']}")
                st.write(f"**Language:** {row['language']}")
                st.markdown('</div>', unsafe_allow_html=True)
