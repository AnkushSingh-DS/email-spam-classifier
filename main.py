import streamlit as st
import pickle
import string
from nltk.stem.porter import PorterStemmer

# Define a simple stopwords list (so we don't need nltk.download)
stopwords = set([
    "i","me","my","myself","we","our","ours","ourselves","you","your","yours",
    "yourself","yourselves","he","him","his","himself","she","her","hers",
    "herself","it","its","itself","they","them","their","theirs","themselves",
    "what","which","who","whom","this","that","these","those","am","is","are",
    "was","were","be","been","being","have","has","had","having","do","does",
    "did","doing","a","an","the","and","but","if","or","because","as","until",
    "while","of","at","by","for","with","about","against","between","into",
    "through","during","before","after","above","below","to","from","up",
    "down","in","out","on","off","over","under","again","further","then",
    "once","here","there","when","where","why","how","all","any","both","each",
    "few","more","most","other","some","such","no","nor","not","only","own",
    "same","so","than","too","very","s","t","can","will","just","don","should",
    "now"
])

ps = PorterStemmer()

def transform_text(text):
    # Lowercase
    text = text.lower()

    # Simple tokenization (split by spaces and punctuation removal)
    tokens = []
    for ch in text.split():
        word = ch.strip(string.punctuation)
        if word:
            tokens.append(word)

    # Remove stopwords + stemming
    filtered = []
    for w in tokens:
        if w not in stopwords and w.isalnum():
            filtered.append(ps.stem(w))

    return " ".join(filtered)


# Load saved vectorizer and model
tfidf = pickle.load(open('vectorizer.pkl','rb'))
model = pickle.load(open('model.pkl','rb'))

# Streamlit UI
st.title("Email/SMS Spam Classifier")

input_sms = st.text_area("Enter the message")

if st.button('Predict', type='primary'):

    # 1. Preprocess
    transformed_sms = transform_text(input_sms)

    # 2. Vectorize
    vector_input = tfidf.transform([transformed_sms])

    # 3. Predict
    result = model.predict(vector_input)[0]

    # 4. Display
    if result == 1:
        st.header("Spam")
    else:
        st.header("Not Spam")
