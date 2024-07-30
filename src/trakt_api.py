import requests
import os
import json

def fetch_trakt_data(token):
    # Dopo aver ricevuto il token, puoi procedere con la tua logica
    query = 'popular'  # Sostituisci con la tua query di ricerca
    num_pages = 10  # Modifica il numero di pagine che vuoi recuperare, imposta a -1 per tutte

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token["access_token"]}',
        'trakt-api-version': '2',
        'trakt-api-key': '5ee9b18608f470b3506e0eacfb27331449fbdff77a703bb8d6d74bf777c91fcb'
    }
    
    base_url = 'https://api.trakt.tv/search/show'
    params = {
        'query': query,
        'page': 1,  # Iniziamo dalla prima pagina
        'limit': 1  # Numero di risultati per pagina
    }

    all_results = []

    while True:
        response = requests.get(base_url, headers=headers, params=params)
        if response.status_code != 200:
            raise Exception(f"API request failed with status code {response.status_code}")

        data = response.json()
        print(f"Found title:  {data}")
        all_results.extend(data)
        
        # Controlliamo se ci sono altre pagine
        page_count = int(response.headers.get('X-Pagination-Page-Count', 1))
        current_page = int(response.headers.get('X-Pagination-Page', 1))

        if num_pages != -1 and current_page >= num_pages:
            break

        if current_page >= page_count:
            break

        params['page'] += 1

    return all_results

def fetch_seasons_for_show(imdb_id, token):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token["access_token"]}',
        'trakt-api-version': '2',
        'trakt-api-key': '5ee9b18608f470b3506e0eacfb27331449fbdff77a703bb8d6d74bf777c91fcb'
    }
    
    url = f'https://api.trakt.tv/shows/{imdb_id}/seasons'
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise Exception(f"API request failed with status code {response.status_code}")
    
    return response.json()

def fetch_episodes_for_season(imdb_id, season_number, token):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token["access_token"]}',
        'trakt-api-version': '2',
        'trakt-api-key': '5ee9b18608f470b3506e0eacfb27331449fbdff77a703bb8d6d74bf777c91fcb'
    }
    
    url = f'https://api.trakt.tv/shows/{imdb_id}/seasons/{season_number}/episodes'
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise Exception(f"API request failed with status code {response.status_code}")
    
    return response.json()

def extract_show_titles(data):
    titles = [item['show']['title'] for item in data]
    return titles

def save_data_to_json(data, filename='data.json'):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

if __name__ == "__main__":
    # Assicurati di avere il token di autenticazione corretto
    token = {
        "access_token": "YOUR_ACCESS_TOKEN"
    }

    data = fetch_trakt_data(token)
    titles = extract_show_titles(data)

    complete_data = []

    for item in data:
        imdb_id = item['show']['ids']['imdb']
        show_data = {
            'title': item['show']['title'],
            'imdb_id': imdb_id,
            'seasons': []
        }

        seasons = fetch_seasons_for_show(imdb_id, token)
        
        for season in seasons:
            season_number = season['number']
            season_data = {
                'number': season_number,
                'episodes': []
            }
            
            episodes = fetch_episodes_for_season(imdb_id, season_number, token)
            
            for episode in episodes:
                episode_data = {
                    'season': episode['season'],
                    'number': episode['number'],
                    'title': episode['title'],
                    'imdb_id': episode['ids']['imdb']
                }
                season_data['episodes'].append(episode_data)
            
            show_data['seasons'].append(season_data)
        
        complete_data.append(show_data)

    save_data_to_json(complete_data)
    print(titles)