import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from textblob import TextBlob

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('punkt_tab')

texts = [
    "The movie was absolutely amazing and I loved every moment of it",
    "This product is terrible and I wasted my money on it",
    "The weather today is okay nothing special"
]

ps = PorterStemmer()
sw = stopwords.words('english')

for text in texts:
    print("---")
    print("Text:", text)
    
    tokens = word_tokenize(text)
    print("Tokens:", tokens)
    
    filtered = []
    for w in tokens:
        if w not in sw:
            filtered.append(w)
    print("Without stopwords:", filtered)
    
    stemmed = []
    for w in filtered:
        stemmed.append(ps.stem(w))
    print("Stemmed:", stemmed)
    
    b = TextBlob(text)
    p = b.sentiment.polarity
    print("Polarity:", p)
    
    if p > 0:
        print("Sentiment: Positive")
    elif p < 0:
        print("Sentiment: Negative")
    else:
        print("Sentiment: Neutral")
    
    print()
