import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
import string

# Inizializza gli strumenti di NLTK
stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

def preprocess_text(text):
    # Tokenizza il testo
    words = word_tokenize(text.lower())
    
    # Rimuove le stop words e punteggiatura, e lemmatizza le parole
    filtered_words = [
        lemmatizer.lemmatize(word) for word in words
        if word not in stop_words and word not in string.punctuation
    ]
    
    return ' '.join(filtered_words)

def generate_keywords(title):
    preprocessed_text = preprocess_text(title)
    
    if not preprocessed_text:
        return []  # Se il testo preprocessato è vuoto, ritorna una lista vuota
    
    # Calcola TF-IDF
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([preprocessed_text])
    
    # Identifica le parole chiave per il titolo
    feature_names = vectorizer.get_feature_names_out()
    tfidf_scores = tfidf_matrix[0]
    sorted_indices = tfidf_scores.toarray().flatten().argsort()[::-1]
    
    # Prendi le prime 5 parole chiave
    top_keywords = [feature_names[idx] for idx in sorted_indices[:5]]
    
    return top_keywords

def generate_keywords_for_titles(titles):
    keywords_list = []
    for title in titles:
        keywords = generate_keywords(title)
        keywords_list.append(keywords)
    return keywords_list
