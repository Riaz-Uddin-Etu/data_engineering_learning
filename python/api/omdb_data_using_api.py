# ===============================================================
print(f'\nWorking with API\n{"="*50}')

'''
Note: OMDb requires an API key, which is read from the OMDB_API_KEY
environment variable.
'''

# Import requests package
import os
import requests
import pandas as pd
from pathlib import Path

api_key = os.getenv('OMDB_API_KEY')
if not api_key:
    raise RuntimeError('Set the OMDB_API_KEY environment variable before running this script.')


# Creating file path
script_dir = Path(__file__).resolve().parent
titles_path = script_dir/'100_movies_of_2025.txt'
output_path = script_dir/'movies.csv'

#Extracting Data
movie_rows = []
count = 0
with open(titles_path) as titleFile:
    for line in titleFile:
        movie_name = line.strip()
        movie_name = movie_name.split(':')
        movie_name = ' :'.join(movie_name)
        movie_name = movie_name.replace(' ', '+')

        response = requests.get(
            'https://www.omdbapi.com/',
            params={'apikey': api_key, 't': movie_name, 'r': 'json'},
            timeout=10
        )
        response.raise_for_status()
        # Decode the JSON data into a dictionary:
        json_data = response.json()

        try:
            title = json_data['Title']
            year = json_data['Year']
            genre = json_data['Genre']
            director = json_data['Director']
            imdbRating = json_data['imdbRating']
            boxOffice = json_data['BoxOffice']
        except KeyError:
            print(f'{movie_name} not found')
            continue

        movie_rows.append({
            'title': title,
            'Year': year,
            'Genre': genre,
            'Director': director,
            'IMDB Rating': imdbRating,
            'Box Office': boxOffice
        })

# print(movie_rows)
df = pd.DataFrame(movie_rows)

# Load to a csv file
with open(output_path, 'w') as csvFile:
    df.to_csv(csvFile, index=False)
    print('\n\nDataframe Successfully Created')
