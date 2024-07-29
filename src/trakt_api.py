import requests
import os
from dotenv import load_dotenv

load_dotenv()

def fetch_trakt_data(token):
    # Dopo aver ricevuto il token, puoi procedere con la tua logica
    query = 'popular'  # Sostituisci con la tua query di ricerca
    num_pages = 10  # Modifica il numero di pagine che vuoi recuperare, imposta a -1 per tutte

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token["access_token"]}',
        'trakt-api-version': '2',
        'trakt-api-key': os.getenv("TRAKT_API_KEY")
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

def extract_show_titles(data):
    titles = [item['show']['title'] for item in data]
    return titles
