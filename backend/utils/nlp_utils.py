import spacy

# Load the spaCy English NLP model
nlp = spacy.load("en_core_web_sm")

# Function to extract keywords (nouns, proper nouns, and verbs) from text
def extract_keywords(text):
    doc = nlp(text)
    keywords = [token.text for token in doc if token.pos_ in ['NOUN', 'PROPN', 'VERB'] and not token.is_stop]
    return keywords
