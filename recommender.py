# recommender.py
import pandas as pd

movies = pd.read_csv("data/movies.csv")
songs = pd.read_csv("data/songs.csv")

def recommend(content_type, mood, energy, n=2):
    if content_type.lower() == "movie":
        results = movies[
            (movies["mood"] == mood) &
            (movies["energy"] == energy)
        ]
    elif content_type.lower() == "song":
        results = songs[
            (songs["mood"] == mood) &
            (songs["energy"] == energy)
        ]
    else:
        return pd.DataFrame()  # empty if unknown type

    if results.empty:
        return "No match found. Try different mood or energy."

    return results.sample(min(n, len(results)))
