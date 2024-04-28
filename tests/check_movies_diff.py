import json

with open('../movies.json', 'rb') as file:
    new_movies_raw = file.read().decode('utf-8')
    new_movies_raw = json.loads(new_movies_raw)

with open('../movies_old.json', 'rb') as file:
    old_movies_raw = file.read().decode('utf-8')
    old_movies_raw = json.loads(old_movies_raw)

new_movies = new_movies_raw.get('Movies')
new_movies = sorted(new_movies, key=lambda x: x['name'])

old_movies = old_movies_raw.get('Movies')
old_movies = sorted(old_movies, key=lambda x: x['name'])

new_movies_names = [movie['name'] for movie in new_movies]
old_movies_names = [movie['name'] for movie in old_movies]

for movie in new_movies_names:
    if movie not in old_movies_names:
        print(f"New movie: {movie}")

for movie in old_movies_names:
    if movie not in new_movies_names:
        print(f"Old movie: {movie}")
