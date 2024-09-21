import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.stem import WordNetLemmatizer
from nltk import pos_tag, word_tokenize
import nltk

# Initialize the WordNet Lemmatizer for keyword normalization
lemmatizer = WordNetLemmatizer()

def clean_and_lemmatize(text):
    """
    Cleans and lemmatizes the input text.
    """
    # Convert to lowercase, remove punctuation, and lemmatize words
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)  # Remove punctuation
    words = text.split()
    lemmatized_words = [lemmatizer.lemmatize(word) for word in words]
    return ' '.join(lemmatized_words)

def filter_keywords_by_pos(keywords):
    """
    Filters keywords to only include relevant nouns, verbs, and technical terms using POS tagging.
    """
    filtered_keywords = []
    pos_tagged = pos_tag(keywords)

    # Retain only nouns, verbs, or significant terms
    for word, tag in pos_tagged:
        if tag.startswith('NN') or tag.startswith('VB'):  # Nouns and Verbs
            filtered_keywords.append(word)
    
    return set(filtered_keywords)

def extract_special_keywords(text, max_features=20):
    """
    Extracts the top keywords from a given text using TF-IDF with POS filtering.
    """
    vectorizer = TfidfVectorizer(stop_words='english', max_features=max_features)
    tfidf_matrix = vectorizer.fit_transform([text])
    
    feature_array = vectorizer.get_feature_names_out()
    filtered_keywords = filter_keywords_by_pos(feature_array)
    
    return filtered_keywords

def summarize_text(keywords, text_type="job description"):
    """
    Summarizes the key focus areas of the job description or resume based on extracted keywords.
    """
    if not keywords:
        return f"The {text_type} does not provide enough specific details."
    
    summary = f"The main focus areas in the {text_type} are related to: {', '.join(keywords[:10])}."
    
    return summary

def generate_comparison_feedback(matching_keywords, missing_keywords, resume_summary, job_summary):
    """
    Generates feedback comparing the resume and job description based on similarities and differences.
    """
    feedback = []
    
    # Summarize the job description
    feedback.append("Job Description Summary: " + job_summary)
    
    # Summarize the resume
    feedback.append("Resume Summary: " + resume_summary)
    
    # Highlight similarities
    if matching_keywords:
        feedback.append(f"Similarities: Your resume matches important areas mentioned in the job description, such as {', '.join(matching_keywords[:5])}. This shows that you have relevant experience in key areas.")
    else:
        feedback.append("Similarities: There are no significant overlaps between your resume and the job description in terms of keywords.")
    
    # Highlight differences
    if missing_keywords:
        feedback.append(f"Differences: However, the job description emphasizes some areas that are missing from your resume, including {', '.join(missing_keywords[:5])}. Consider adding more details about these topics to better align with the job requirements.")
    
    return feedback

def analyze_resume(resume_text, job_description):
    # Clean and lemmatize both resume text and job description
    cleaned_resume = clean_and_lemmatize(resume_text)
    cleaned_job_description = clean_and_lemmatize(job_description)

    # Extract keywords from cleaned and lemmatized texts
    job_keywords = extract_special_keywords(cleaned_job_description)
    #resume_keywords = extract_special_keywords(cleaned_resume)
    resume_keywords = set(cleaned_resume.split(" "))
    resume_keywords2 = extract_special_keywords(cleaned_resume)
    
    # Find matching and missing keywords
    matching_keywords = job_keywords.intersection(resume_keywords)
    missing_keywords = job_keywords.difference(resume_keywords)
    
    # Calculate similarity score using cleaned text
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform([cleaned_resume, cleaned_job_description])
    
    """
    if tfidf_matrix.shape[1] > 0:
        similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
    else:
        similarity = 0.0  # Set similarity to 0 if no meaningful comparison is possible
    """
    similarity = len(matching_keywords) / len(job_keywords)
    feedback = []
    if len(missing_keywords) > 0:
        feedback.append(f"Your resume is missing important keywords: {', '.join(missing_keywords)}")
    if len(matching_keywords) == 0:
        feedback.append("None of the job description keywords are present in your resume.")

    # Generate summaries of the job description and resume
    job_summary = summarize_text(list(job_keywords), "job description")
    resume_summary = summarize_text(list(resume_keywords2), "resume")

    # Generate comparison feedback
    comparison_feedback = generate_comparison_feedback(list(matching_keywords), list(missing_keywords), resume_summary, job_summary)

    return {
        "similarity": similarity,
        "matching_keywords": list(matching_keywords),
        "missing_keywords": list(missing_keywords),
        "feedback": comparison_feedback,
    }
