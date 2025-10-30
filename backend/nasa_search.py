import json
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.tokenize import sent_tokenize
import nltk

nltk.download("punkt", quiet=True)

def load_articles(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

class SimpleSearchIndex:
    def __init__(self, articles):
        self.articles = articles
        self.vectorizer = TfidfVectorizer(stop_words="english")
        self.vectors = self.vectorizer.fit_transform([a["text"] for a in articles])

    def query(self, q, top_k=3):
        q_vec = self.vectorizer.transform([q])
        sims = cosine_similarity(q_vec, self.vectors).flatten()
        top_idx = sims.argsort()[::-1][:top_k]
        return [{"score": sims[i], "article": self.articles[i]} for i in top_idx]

def summarize_text(text, num_sentences=3):
    sents = sent_tokenize(text)
    sents = [re.sub(r"\s+", " ", s) for s in sents]
    return " ".join(sents[:num_sentences])
