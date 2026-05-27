# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import ast
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.stem.porter import PorterStemmer
ps = PorterStemmer()

# Load datasets
movies = pd.read_csv(r"C:\Users\princ\Downloads\archive (2)\tmdb_5000_movies.csv")
credits = pd.read_csv(r"C:\Users\princ\Downloads\archive (2)\tmdb_5000_credits.csv")

# Merge datasets
movies = movies.merge(credits, on='title')

# Select important columns
movies = movies[['movie_id','title','overview','genres','keywords','cast','crew']]

# Handle missing values
movies.dropna(inplace=True)

# Convert text-based columns from string to list
def convert(obj):
    L = []
    for i in ast.literal_eval(obj):
        L.append(i['name'])
    return L

movies['genres'] = movies['genres'].apply(convert)
movies['keywords'] = movies['keywords'].apply(convert)

# Get only top 3 cast
def convert_cast(obj):
    L = []
    counter = 0
    for i in ast.literal_eval(obj):
        if counter < 3:
            L.append(i['name'])
            counter += 1
    return L

movies['cast'] = movies['cast'].apply(convert_cast)

# Get director name
def fetch_director(obj):
    L = []
    for i in ast.literal_eval(obj):
        if i['job'] == 'Director':
            L.append(i['name'])
            break
    return L

movies['crew'] = movies['crew'].apply(fetch_director)

# Remove spaces between words
def remove_space(L):
    return [i.replace(" ", "") for i in L]

movies['cast'] = movies['cast'].apply(remove_space)
movies['crew'] = movies['crew'].apply(remove_space)
movies['genres'] = movies['genres'].apply(remove_space)
movies['keywords'] = movies['keywords'].apply(remove_space)

# Create a new combined column (tags)
movies['overview'] = movies['overview'].apply(lambda x: x.split())
movies['tags'] = movies['overview'] + movies['genres'] + movies['keywords'] + movies['cast'] + movies['crew']
# Keep only necessary columns
new_df = movies[['movie_id','title','tags']].copy()
new_df['title_lower'] = new_df['title'].str.lower()

new_df['tags'] = new_df['tags'].apply(lambda x: " ".join(x))  # converts list → string
new_df['tags'] = new_df['tags'].str.lower()                    # lowercase everything

new_df['tags'] = new_df['tags'].apply(lambda x: " ".join([ps.stem(i) for i in x.split()]))


# Text vectorization
cv = CountVectorizer(max_features=5000, stop_words='english')
vectors = cv.fit_transform(new_df['tags']).toarray()

# Calculate similarity
similarity = cosine_similarity(vectors)

# Recommendation function
def recommend(movie):
    movie = movie.lower().strip()   # ✅ makes input case-insensitive

    if movie not in new_df['title_lower'].values:
        print("\n❌ Movie not found in database. Try another one.\n")
        return

    movie_index = new_df[new_df['title_lower'] == movie].index[0]
    distances = similarity[movie_index]

    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    original_title = new_df.iloc[movie_index].title
    print(f"\n🎬 Top 5 Recommendations for '{original_title}':\n")

    for i in movies_list:
        print("✅", new_df.iloc[i[0]].title)


while True:
    user_movie = input("\n👉 Enter a movie name (or type 'stop' to exit): ").strip()

    if user_movie.lower() == "stop":
        print("\n👋 Thanks for using the Movie Recommendation System!")
        break

    recommend(user_movie)
import pickle

pickle.dump(new_df, open('movies.pkl', 'wb'))
pickle.dump(similarity, open('similarity.pkl', 'wb'))

print("✅ Pickle files created successfully!")
