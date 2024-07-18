from flask import Flask, request, render_template
import pickle
import pandas as pd
import requests 

app = Flask(__name__)

def fetch_poster(movie_id):
    response = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=30d6beef367b858989f9eaffb1eb55df&language=en-US')
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movie_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movies.append(movies.iloc[i[0]].title)
    return recommended_movies, recommended_movie_posters

movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

@app.route('/')
def index():
    return render_template('index.html', movie_list=movies['title'].values)

@app.route('/recommend', methods=['POST'])
def recommend_movies():
    selected_movie_name = request.form['movie']
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie_name)
    
    # Debug prints
    print("Selected movie:", selected_movie_name)
    print("Recommended movie names:", recommended_movie_names)
    print("Recommended movie posters:", recommended_movie_posters)
    
    return render_template('recommend.html', movie_names=recommended_movie_names, movie_posters=recommended_movie_posters, zip=zip)

if __name__ == '__main__':
    app.run(debug=True)
