from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# TMDb API Key
TMDB_API_KEY = '8d018441407794b6f313ebbeb40ee83b'

# TMDb genre mapping
GENRE_MAP = {
    "action": 28,
    "comedy": 35,
    "drama": 18,
    "horror": 27,
    "romance": 10749
}

# Mood to genre mapping
MOOD_TO_GENRE = {
    "happy": "comedy",
    "sad": "drama",
    "excited": "action",
    "relaxed": "romance"
}

def get_movies(genre, rating, language):
    """
    Fetch movie recommendations using TMDb API Discover endpoint.
    """
    try:
        url = f"https://api.themoviedb.org/3/discover/movie"
        params = {
            "api_key": TMDB_API_KEY,
            "with_genres": genre,
            "vote_average.gte": rating,
            "with_original_language": language,
            "sort_by": "popularity.desc"
        }

        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise an error for HTTP issues

        data = response.json()
        movies = []
        for result in data.get('results', [])[:10]:  # Top 10 results
            movies.append({
                'title': result['title'],
                'link': f"https://www.themoviedb.org/movie/{result['id']}",
                'image': f"https://image.tmdb.org/t/p/w500{result['poster_path']}" if result.get('poster_path') else ""
            })
        return movies
    except Exception as e:
        print(f"Error fetching movies: {e}")
        return []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    # Get user inputs from the form
    mood = request.form['mood']
    genre = request.form['genre']
    rating = float(request.form['rating'])  # Convert to float
    language = request.form['language']

    # If a mood is selected, map it to a genre
    if mood:
        genre = MOOD_TO_GENRE.get(mood.lower(), genre)

    # Map genre name to TMDb genre ID
    genre_id = GENRE_MAP.get(genre.lower())
    if not genre_id:
        return render_template('results.html', movies=[])

    # Fetch movie recommendations
    movies = get_movies(genre_id, rating, language)
    return render_template('results.html', movies=movies)

if __name__ == '__main__':
    app.run(debug=True)
