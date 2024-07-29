import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.oauth import authenticate_trakt, refresh_token
from src.trakt_api import fetch_trakt_data, extract_show_titles
from src.ai import generate_keywords

def main():
    token = refresh_token()
    if not token:
        token = authenticate_trakt()

    data = fetch_trakt_data(token)
    print("fetch_trakt_data:", data)
    
    titles = extract_show_titles(data)
    print("extract_show_titles:", titles)

    keywords_list = []
    for title in titles:
        keywords = generate_keywords(title)
        keywords_list.append(keywords)
        print(f"Titolo: {title} - Keywords: {keywords}\n")

    print("Keywords generate:", keywords_list)

if __name__ == "__main__":
    main()
