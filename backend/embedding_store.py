from sentence_transformers import SentenceTransformer
import numpy as np
import faiss
import os
import pickle

MODEL_NAME = "all-MiniLM-L6-v2"
EMBEDDINGS_FILE = os.path.join(os.path.dirname(__file__), "embeddings.pkl")
INDEX_FILE = os.path.join(os.path.dirname(__file__), "faiss.index")


class EmbeddingStore:
    def __init__(self):
        self.model = SentenceTransformer(MODEL_NAME)
        self.embeddings = []
        self.texts = []
        self.index = None
        self.load()

    def clear(self):
        self.embeddings = []
        self.texts = []
        self.index = None
        if os.path.exists(EMBEDDINGS_FILE):
            os.remove(EMBEDDINGS_FILE)
        if os.path.exists(INDEX_FILE):
            os.remove(INDEX_FILE)

    def add_texts(self, texts):
        print(f"[Embedding] Adding {len(texts)} chunks:")
        for t in texts:
            print(f"  - {repr(t[:100])}")
        vectors = self.model.encode(texts)
        self.embeddings.extend(vectors)
        self.texts.extend(texts)
        self._update_index()
        self.save()

    def _update_index(self):
        if self.embeddings:
            arr = np.array(self.embeddings).astype('float32')
            self.index = faiss.IndexFlatL2(arr.shape[1])
            self.index.add(arr)

    def search(self, query, top_k=3):
        if not self.index:
            return []
        q_vec = self.model.encode([query]).astype('float32')
        D, I = self.index.search(q_vec, top_k)
        return [self.texts[i] for i in I[0] if i < len(self.texts)]

    def save(self):
        with open(EMBEDDINGS_FILE, "wb") as f:
            pickle.dump((self.embeddings, self.texts), f)
        if self.index:
            faiss.write_index(self.index, INDEX_FILE)

    def load(self):
        if os.path.exists(EMBEDDINGS_FILE):
            with open(EMBEDDINGS_FILE, "rb") as f:
                self.embeddings, self.texts = pickle.load(f)
            if self.embeddings:
                arr = np.array(self.embeddings).astype('float32')
                self.index = faiss.IndexFlatL2(arr.shape[1])
                self.index.add(arr)

embedding_store = EmbeddingStore()
