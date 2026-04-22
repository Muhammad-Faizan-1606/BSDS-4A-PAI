import pandas as pd
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
import re

df = pd.read_csv('restaurant_data.csv')
df = df.dropna()
print("loaded", len(df), "rows")

def clean(text):
    if isinstance(text, str):
        text = re.sub(r'[^A-Za-z\s]', '', text)
        text = text.lower()
    else:
        text = ''
    return text

df['clean_q'] = df['question'].apply(clean)
print("cleaning done")

model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
print("model loaded")

embeddings = model.encode(df['clean_q'].tolist())
print("embeddings shape:", embeddings.shape)

d = embeddings.shape[1]
index = faiss.IndexFlatL2(d)
index.add(np.array(embeddings))
print("faiss index created with", index.ntotal, "vectors")

faiss.write_index(index, 'restaurant_index.faiss')
df.to_csv('restaurant_clean.csv', index=False)
print("saved index and data")

def find_answer(query, k=1):
    q = clean(query)
    q_vec = model.encode([q])
    distances, indices = index.search(np.array(q_vec), k)
    best = indices[0][0]
    ans = df['answer'].iloc[best]
    return ans

if __name__ == '__main__':
    test_queries = [
        "what food do you have",
        "do you deliver to home",
        "what time are you open",
        "how much is biryani"
    ]
    
    for q in test_queries:
        print("Q:", q)
        print("A:", find_answer(q))
        print()
