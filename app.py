# app.py
import streamlit as st
import pandas as pd
from recommender import recommend, movies, songs

st.set_page_config(page_title="Mood Recommender", layout="wide")

# ---------------- CSS ----------------
st.markdown("""
<style>
/* App Background */
.stApp {
    background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    color: #1e1e1e;
}

/* Headings */
h2, h3 {
    font-weight: 600;
}

/* Buttons */
.stButton>button {
    background: linear-gradient(90deg, #ff758c 0%, #ff7eb3 100%);
    color: white;
    font-weight: bold;
    border-radius: 12px;
    padding: 8px 20px;
    border: none;
    transition: all 0.3s ease;
}

.stButton>button:hover {
    background: linear-gradient(90deg, #ff7eb3 0%, #ff758c 100%);
    transform: scale(1.05);
}

/* Inputs */
.css-1n76uvr, .css-1d391kg {
    border-radius: 10px;
    border: 1px solid rgba(255, 255, 255, 0.3);
    background: rgba(255, 255, 255, 0.2);
    backdrop-filter: blur(5px);
    padding-left: 10px;
    margin-bottom: 15px;
}

/* Result Cards */
.result-card {
    border-radius: 15px;
    padding: 15px 20px;
    margin-bottom: 15px;
    background: rgba(255, 255, 255, 0.15);
    box-shadow: 0 8px 24px rgba(0,0,0,0.08);
    backdrop-filter: blur(8px);
    transition: transform 0.2s;
}

.result-card:hover {
    transform: scale(1.02);
}

/* Placeholder Box */
.placeholder-box {
    border: 2px solid rgba(255,255,255,0.5);
    border-radius: 15px;
    padding: 25px;
    background: rgba(255,255,255,0.15);
    backdrop-filter: blur(8px);
    box-shadow: 0 8px 24px rgba(0,0,0,0.08);
    text-align: center;
    margin-bottom: 20px;
}

/* Scrollbar Styling */
::-webkit-scrollbar {
    width: 8px;
}
::-webkit-scrollbar-thumb {
    background: rgba(0, 0, 0, 0.2);
    border-radius: 4px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- LAYOUT ----------------
left, right = st.columns([1, 1.3], gap="large")

# ---------------- LEFT SIDE ----------------
with left:
    st.markdown("##  Mood Recommender")
    st.markdown("Find movies or songs that match your vibe ")
    st.markdown("---")

    # Inputs
    content_type = st.selectbox("Content Type", ["Movie", "Song"])
    mood = st.selectbox("Mood", sorted(movies["mood"].unique()))
    energy = st.selectbox("Energy Level", ["low", "medium", "high"])

    if content_type == "Song":
        language = st.selectbox("Language", sorted(songs["language"].unique()))
    else:
        language = None

    st.markdown("<br>", unsafe_allow_html=True)
    get_btn = st.button(" Get Recommendations")

# ---------------- RIGHT SIDE ----------------
with right:
    if not get_btn:
        st.markdown("""
        <div class="placeholder-box">
            <h3> Your Recommendations Will Appear Here</h3>
            <p>Select your mood<br>
            Choose your energy level<br>
            Click the button</p>
            <p>Sit back and discover something amazing 🎧🍿</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("## 🔥 Recommended For You")
        st.markdown("---")

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
                if content_type == "Movie":
                    st.markdown(f"""
                    <div class="result-card">
                        <h4>🎬 {row['title']}</h4>
                        <p><b>Genre:</b> {row['genre']} | <b>Duration:</b> {row['duration']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="result-card">
                        <h4>🎵 {row['song']}</h4>
                        <p><b>Artist:</b> {row['artist']} | <b>Language:</b> {row['language']}</p>
                    </div>
                    """, unsafe_allow_html=True)

        # ✅ Posters INSIDE right column
    st.markdown("<br>", unsafe_allow_html=True)

    poster_data = [
        {"image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRCNPyPvfVv6zG6gmwRr6FzB2c2NG3Za8t5lA&s"},  # Charitha Attalage
        {"image": "https://image.tmdb.org/t/p/w500/2H1TmgdfNtsKlU9jKdeNyYL5y8T.jpg"},  # Inside Out
        {"image": "https://image.tmdb.org/t/p/w500/or06FN3Dka5tukK1e9sl16pB3iy.jpg"},  # Avengers Endgame
        {"image": "https://storage.googleapis.com/pod_public/750/263676.jpg"},  # TS
        {"image": "https://image.tmdb.org/t/p/w500/q719jXXEzOoYaps6babgKnONONX.jpg"}   # Your name
    ]

    # 🔥 5 equal columns
    cols = st.columns(5, gap="small")

    for col, poster in zip(cols, poster_data):
        with col:
            st.image(poster["image"], width=120)

