from flask import Flask, render_template, request
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from textblob import TextBlob
from collections import Counter

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger')
nltk.download('punkt_tab')
nltk.download('averaged_perceptron_tagger_eng')

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    text = request.form['text']

    word_tokens = word_tokenize(text)
    sentences = sent_tokenize(text)

    sw = stopwords.words('english')
    filtered = []
    for w in word_tokens:
        if w.lower() not in sw and w.isalpha():
            filtered.append(w.lower())

    ps = PorterStemmer()
    stems = []
    for w in filtered:
        stems.append(ps.stem(w))

    word_counts = Counter(filtered)
    top_words = word_counts.most_common(5)

    blob = TextBlob(text)
    polarity = round(blob.sentiment.polarity, 2)
    subjectivity = round(blob.sentiment.subjectivity, 2)

    if polarity > 0.1:
        sentiment = "Positive"
    elif polarity < -0.1:
        sentiment = "Negative"
    else:
        sentiment = "Neutral"

    total_words = len(word_tokens)
    total_sentences = len(sentences)
    unique_words = len(set(filtered))

    return render_template('index.html',
        result=True,
        original=text,
        total_words=total_words,
        total_sentences=total_sentences,
        unique_words=unique_words,
        sentiment=sentiment,
        polarity=polarity,
        subjectivity=subjectivity,
        top_words=top_words,
        tokens=word_tokens[:20]
    )

if __name__ == '__main__':
    app.run(debug=True)
