import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from collections import Counter

# Load the spaCy English NLP model
nlp = spacy.load("en_core_web_sm")

def preprocess_text(text):
    doc = nlp(text.lower())
    result = []
    for token in doc:
        if token.text in nlp.Defaults.stop_words:
            continue
        if token.is_punct:
            continue
        if token.lemma_ == '-PRON-':
            continue
        if len(token.text) < 2:
            continue
        if token.pos_ in ['NOUN', 'PROPN', 'VERB', 'ADJ']:
            result.append(token.lemma_)
    return " ".join(result)

def extract_keywords(text, comparison_text=None, top_n=30):
    preprocessed_text = preprocess_text(text)
    
    if comparison_text:
        preprocessed_comparison = preprocess_text(comparison_text)
        corpus = [preprocessed_text, preprocessed_comparison]
    else:
        corpus = [preprocessed_text]
    
    tfidf = TfidfVectorizer(max_features=100, token_pattern=r'\b\w+\b')
    tfidf_matrix = tfidf.fit_transform(corpus)
    
    feature_names = np.array(tfidf.get_feature_names_out())
    tfidf_scores = tfidf_matrix.toarray()[0]
    
    sorted_indexes = np.argsort(tfidf_scores)[::-1]
    top_keywords = feature_names[sorted_indexes][:top_n]
    
    return list(top_keywords)

def calculate_similarity(text1, text2):
    preprocessed_text1 = preprocess_text(text1)
    preprocessed_text2 = preprocess_text(text2)
    
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([preprocessed_text1, preprocessed_text2])
    return cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]

def extract_entities(text):
    doc = nlp(text)
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    return entities

def analyze_resume(resume_text, job_description):
    similarity = calculate_similarity(resume_text, job_description)

    resume_keywords = extract_keywords(resume_text, job_description)
    job_keywords = extract_keywords(job_description, resume_text)
    matching_keywords = set(resume_keywords).intersection(set(job_keywords))
    missing_keywords = set(job_keywords) - set(resume_keywords)

    resume_entities = extract_entities(resume_text)
    job_entities = extract_entities(job_description)

    feedback = []
    if similarity < 0.3:
        feedback.append("Your resume doesn't seem to match the job description very well. Consider tailoring it more specifically to the role.")
    elif similarity < 0.6:
        feedback.append("Your resume has some relevance to the job description, but there's room for improvement.")
    else:
        feedback.append("Your resume appears to be well-tailored to the job description.")

    if missing_keywords:
        feedback.append(f"Consider adding these keywords to your resume: {', '.join(list(missing_keywords)[:5])}.")

    if len(matching_keywords) < 5:
        feedback.append("Try to include more relevant keywords from the job description in your resume.")

    resume_skills = [ent[0].lower() for ent in resume_entities if ent[1] in ['SKILL', 'ORG', 'PRODUCT']]
    job_skills = [ent[0].lower() for ent in job_entities if ent[1] in ['SKILL', 'ORG', 'PRODUCT']]
    missing_skills = set(job_skills) - set(resume_skills)
    if missing_skills:
        feedback.append(f"The job description mentions these skills or technologies that are missing from your resume: {', '.join(list(missing_skills))}.")

    return {
        "similarity": similarity,
        "matching_keywords": list(matching_keywords),
        "missing_keywords": list(missing_keywords),
        "feedback": feedback
    }