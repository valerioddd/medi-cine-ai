import openai
import os
from dotenv import load_dotenv
import httpx

# Carica le variabili di ambiente dal file .env
load_dotenv()

def generate_keywords(description):
    print(description)

    openai.api_key = os.getenv("OPENAI_API_KEY")

    if not openai.api_key:
        raise ValueError("L'API key di OpenAI non è stata trovata. Assicurati che il file .env contenga OPENAI_API_KEY.")

    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Sei un assistente che genera keywords."},
            {"role": "user", "content": f"Genera delle keywords per la seguente descrizione: {description}"}
        ]
    )

    print("Response: " + description)

    keywords = response.choices[0].message
    return keywords
