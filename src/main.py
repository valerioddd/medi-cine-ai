import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.oauth import authenticate_trakt, refresh_token
from src.trakt_api import fetch_trakt_data, extract_show_titles, save_data_to_json, fetch_seasons_for_show, fetch_episodes_for_season
from src.opensubtitles import fetch_subtitles
from src.ai import generate_keywords

def main():
    token = refresh_token()
    if not token:
        token = authenticate_trakt()

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

                # Recupera i sottotitoli per ogni episodio
                if(episode['ids']['imdb']):
                    subtitles = fetch_subtitles(episode['ids']['imdb'])
                    episode_data['subtitles'] = subtitles
                
                season_data['episodes'].append(episode_data)
            
            show_data['seasons'].append(season_data)
        
        complete_data.append(show_data)

    save_data_to_json(complete_data)  # Salva i dati in un file JSON

    keywords_list = []
    for title in titles:
        keywords = generate_keywords(title)
        keywords_list.append(keywords)
        print(f"Titolo: {title}\nKeywords: {keywords}\n")

if __name__ == "__main__":
    main()