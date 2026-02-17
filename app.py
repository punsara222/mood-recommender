# app.py
import streamlit as st
import pandas as pd
from recommender import recommend, movies, songs

st.set_page_config(page_title="Mood Recommender", page_icon="🎭", layout="wide")

# ---------------- THEME ----------------
theme_mode = st.toggle("🌙 Dark Mode", value=True)

if theme_mode:
    bg_gradient = "linear-gradient(135deg, #0b1f3f, #1c2a50, #162336)"
    main_text = "#E0E0E0"
    secondary_text = "#B0B0B0"
    card_bg = "rgba(255,255,255,0.05)"
    button_gradient = "linear-gradient(90deg, #6a11cb, #2575fc)"
    navbar_bg = "rgba(10,10,30,0.8)"
else:
    bg_gradient = "linear-gradient(135deg, #a1c4fd, #c2e9fb)"
    main_text = "#111111"
    secondary_text = "#333333"
    card_bg = "rgba(255,255,255,0.3)"
    button_gradient = "linear-gradient(90deg, #ff9a9e, #fad0c4)"
    navbar_bg = "rgba(255,255,255,0.8)"

# ---------------- CSS ----------------
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;800&display=swap');

.stApp {{
    background: {bg_gradient};
    background-size: 400% 400%;
    animation: gradient 25s ease infinite;
    font-family: 'Montserrat', sans-serif;
}}

@keyframes gradient {{
    0% {{ background-position: 0% 50%; }}
    50% {{ background-position: 100% 50%; }}
    100% {{ background-position: 0% 50%; }}
}}

/* ---------------- NAVBAR ---------------- */
.navbar {{
    width: 100%;
    padding: 16px 40px;
    position: sticky;
    top: 0;
    z-index: 99;
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: {navbar_bg};
    backdrop-filter: blur(10px);
    box-shadow: 0 2px 10px rgba(0,0,0,0.3);
}}

.navbar-logo {{
    font-weight: 800;
    font-size: 28px;
    color: {main_text};
}}

.navbar-links a {{
    margin-left: 24px;
    text-decoration: none;
    color: {main_text};
    font-weight: 600;
    transition: 0.3s;
}}

.navbar-links a:hover {{
    color: #ff416c;
}}

/* ---------------- HERO ---------------- */
.hero-title {{
    font-size: 56px;
    font-weight: 800;
    text-align: center;
    color: {main_text};
    margin-top: 20px;
}}

.hero-sub {{
    text-align: center;
    font-size: 20px;
    color: {secondary_text};
    margin-bottom: 40px;
}}

/* ---------------- INPUT ROW ---------------- */
.stSelectbox > div > div {{
    background-color: rgba(255,255,255,0.1) !important;
    color: {main_text} !important;
    border-radius: 12px;
    padding-left: 12px;
}}

.stButton>button {{
    background: {button_gradient};
    color: white;
    font-size: 18px;
    border-radius: 16px;
    padding: 16px 32px;
    border: none;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}}

.stButton>button:hover {{
    transform: scale(1.08);
    box-shadow: 0 15px 35px rgba(0,0,0,0.35);
}}

/* ---------------- RESULT CARDS ---------------- */
.result-card {{
    width: 240px;
    border-radius: 18px;
    background: {card_bg};
    backdrop-filter: blur(12px);
    box-shadow: 0 10px 25px rgba(0,0,0,0.25);
    margin-right: 20px;
    padding: 16px;
    color: {main_text};
    display: inline-block;
    vertical-align: top;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}}

.result-card:hover {{
    transform: translateY(-6px) scale(1.02);
    box-shadow: 0 25px 50px rgba(0,0,0,0.4);
}}

.card-image {{
    width: 100%;
    height: 320px;
    object-fit: cover;
    border-radius: 12px;
    margin-bottom: 12px;
    transition: transform 0.3s ease;
}}

.card-image:hover {{
    transform: scale(1.05);
}}

/* ---------------- CAROUSEL ---------------- */
.horizontal-scroll {{
    overflow-x: auto;
    white-space: nowrap;
    padding-bottom: 20px;
    margin-left: 20px;
    margin-right: 20px;
}}
.horizontal-scroll::-webkit-scrollbar {{
    height: 10px;
}}
.horizontal-scroll::-webkit-scrollbar-thumb {{
    background: #888;
    border-radius: 10px;
}}
.horizontal-scroll::-webkit-scrollbar-thumb:hover {{
    background: #555;
}}

/* ---------------- FOOTER ---------------- */
.footer {{
    text-align: center;
    padding: 20px;
    color: {secondary_text};
    margin-top: 50px;
    border-top: 1px solid rgba(255,255,255,0.2);
}}
</style>
""", unsafe_allow_html=True)

# ---------------- NAVBAR ----------------
st.markdown(f"""
<div class="navbar">
    <div class="navbar-logo">🎭 MoodRecs</div>
    <div class="navbar-links">
        <a href="#">Home</a>
        <a href="#">About</a>
        <a href="#">Contact</a>
    </div>
</div>
""", unsafe_allow_html=True)

# ---------------- HERO ----------------
st.markdown('<div class="hero-title">Find Your Perfect Mood Match</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-sub">Movies & Songs tailored to your vibe ✨</div>', unsafe_allow_html=True)

# ---------------- INPUT ROW ----------------
col1, col2, col3, col4 = st.columns([1.2, 1.2, 1, 1])
with col1:
    content_type = st.selectbox("Content", ["Movie", "Song"])
with col2:
    mood = st.selectbox("Mood", sorted(movies["mood"].unique()))
with col3:
    energy = st.selectbox("Energy", ["low", "medium", "high"])
with col4:
    language = st.selectbox("Language", sorted(songs["language"].unique())) if content_type=="Song" else None

st.write("")
center_btn = st.columns([3,1,3])
with center_btn[1]:
    get_btn = st.button("✨ Get Recommendations")
st.write("")

# ---------------- MOOD ICONS ----------------
mood_emoji = {
    "happy": "😄", "sad": "😢", "romantic": "💖",
    "motivated": "💪", "excited": "🤩", "calm": "😌",
    "bored": "😴", "thoughtful": "🤔"
}

# ---------------- RESULTS ----------------
if get_btn:
    st.markdown(f"<h3 style='color:{main_text}; margin-left:20px;'>Results for {mood.capitalize()} {mood_emoji.get(mood,'')} | {energy.capitalize()} Energy</h3>", unsafe_allow_html=True)
    
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
        st.markdown('<div class="horizontal-scroll">', unsafe_allow_html=True)
        for _, row in results.iterrows():
            image_url = row.get("image_url") if content_type=="Movie" else None
            st.markdown('<div class="result-card">', unsafe_allow_html=True)
            if image_url:
                st.markdown(f'<img class="card-image" src="{image_url}">', unsafe_allow_html=True)
            if content_type == "Movie":
                st.markdown(f"### 🎬 {row['title']}")
                st.write(f"**Genre:** {row['genre']}")
                st.write(f"**Duration:** {row['duration']}")
            else:
                st.markdown(f"### 🎵 {row['song']}")
                st.write(f"**Artist:** {row['artist']}")
                st.write(f"**Language:** {row['language']}")
            st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ---------------- FOOTER ----------------
st.markdown(f"""
<div class="footer">
    © 2026 MoodRecs • Designed by You • Data-driven Recommendations
</div>
""", unsafe_allow_html=True)
