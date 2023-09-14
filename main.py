import streamlit as st
import pickle
import string
from nltk.corpus import stopwords
import nltk
from nltk.stem.porter import PorterStemmer
nltk.download('punkt')
nltk.download('stopwords')

ps = PorterStemmer()


def transform_text(text):
    text = text.lower()
    text = nltk.word_tokenize(text)

    y = []
    for i in text:
        if i.isalnum():
            y.append(i)

    text = y[:]
    y.clear()

    for i in text:
        if i not in stopwords.words('english') and i not in string.punctuation:
            y.append(i)

    text = y[:]
    y.clear()

    for i in text:
        y.append(ps.stem(i))

    return " ".join(y)

tfidf = pickle.load(open('vectorizer.pkl','rb'))
model = pickle.load(open('model.pkl','rb'))

# st.title("Email/SMS Spam Classifier")

# input_sms = st.text_area("Enter the message")

# if st.button('Predict', type = 'primary'):

#     # 1. preprocess
#       transformed_sms = transform_text(input_sms)
#     # 2. vectorize
#       vector_input = tfidf.transform([transformed_sms])
#     # 3. predict
#       result = model.predict(vector_input)[0]
#     # 4. Display
#       if result == 1:
#           st.header("Spam")
#       else:
#           st.header("Not Spam")
# elif st.button('Clear'):
#     input_sms.empty()
def main():
    st.title("Spam Classification App")
    st.sidebar.header("User Input")

    # Create a text input field for the user to enter SMS text
input_sms = st.text_area("Enter SMS text here:", "")

empty_str = ''

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

        # Clear the content of the text_area widget by assigning an empty string
        elif st.button('Clear'):
        input_sms = "empty_str"

if __name__ == '__main__':
    main()
