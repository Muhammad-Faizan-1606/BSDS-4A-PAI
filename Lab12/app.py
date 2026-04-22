from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
import re
import os

app = Flask(__name__)

# ── Constants ────────────────────────────────────────────────────────────────
RAW_CSV      = 'restaurant_data.csv'
CLEAN_CSV    = 'restaurant_clean.csv'
FAISS_INDEX  = 'restaurant_index.faiss'
MODEL_NAME   = 'paraphrase-MiniLM-L6-v2'

# ── Text cleaning ─────────────────────────────────────────────────────────────
def clean(text):
    if isinstance(text, str):
        text = re.sub(r'[^A-Za-z\s]', '', text)
        text = text.lower().strip()
    else:
        text = ''
    return text

# ── Build index from scratch if files are missing ────────────────────────────
def build_index():
    print("[INFO] Building FAISS index from raw data...")
    df = pd.read_csv(RAW_CSV).dropna()
    df['clean_q'] = df['question'].apply(clean)

    m = SentenceTransformer(MODEL_NAME)
    embeddings = m.encode(df['clean_q'].tolist(), show_progress_bar=True)
    embeddings = np.array(embeddings).astype('float32')

    idx = faiss.IndexFlatL2(embeddings.shape[1])
    idx.add(embeddings)

    faiss.write_index(idx, FAISS_INDEX)
    df.to_csv(CLEAN_CSV, index=False)
    print(f"[INFO] Index built with {idx.ntotal} vectors and saved.")
    return m, idx, df

# ── Load or build on startup ──────────────────────────────────────────────────
if os.path.exists(FAISS_INDEX) and os.path.exists(CLEAN_CSV):
    print("[INFO] Loading existing index and data...")
    model = SentenceTransformer(MODEL_NAME)
    df    = pd.read_csv(CLEAN_CSV)
    faiss_index = faiss.read_index(FAISS_INDEX)
    print(f"[INFO] Loaded {faiss_index.ntotal} vectors.")
else:
    model, faiss_index, df = build_index()

# ── Answer retrieval ──────────────────────────────────────────────────────────
def get_answer(question: str) -> str:
    q_vec = model.encode([clean(question)]).astype('float32')
    distances, indices = faiss_index.search(q_vec, 1)
    best_idx = indices[0][0]
    return df['answer'].iloc[best_idx]

# ── Routes ────────────────────────────────────────────────────────────────────
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    if not data or 'question' not in data:
        return jsonify({'error': 'No question provided'}), 400
    answer = get_answer(data['question'])
    return jsonify({'answer': str(answer)})

# ── Run ───────────────────────────────────────────────────────────────────────
if __name__ == '__main__':
    app.run(debug=True)
