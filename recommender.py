import pandas as pd

movies = pd.read_csv("data/movies.csv")
songs = pd.read_csv("data/songs.csv")

print("Movies data:")
print(movies)

print("\nSongs data:")
print(songs)

def recommend(content_type, mood, energy):
    if content_type == "movie":
        results = movies[
            (movies["mood"] == mood) &
            (movies["energy"] == energy)
        ]

    elif content_type == "song":
        results = songs[
            (songs["mood"] == mood) &
            (songs["energy"] == energy)
        ]

    if results.empty:
        return "No match found. Try different mood or energy."

    return results.sample(min(2, len(results)))

    
print(recommend("song", "happy", "high"))

content = input("Do you want a movie or song? ")
mood = input("Enter your mood: ")
energy = input("Enter energy level (low/medium/high): ")

print("\nYour recommendations:")
print(recommend(content, mood, energy))


