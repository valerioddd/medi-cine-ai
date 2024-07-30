import requests

def fetch_subtitles(imdb_id):
    print(f'Trying to get subtitles from imdb_id = {imdb_id}')
    url = f'https://api.opensubtitles.com/api/v1/subtitles?imdb_id={imdb_id}'
    headers = {
        #'Content-Type': 'application/json',
        'Api-Key': 'JunVd2RWz2SomcDFZJxId4oGD4qCyqqG',
        'UserAgent': 'MediCine 1.0'
    }
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"API request failed with status code: {response.status_code} and content: {response.json}")
    else:
        return response.json()
