import os
import json
import faiss
import numpy as np
from typing import List, Dict, Any, Optional
from .embeddings import NomicEmbeddingProvider, EMBEDDING_DIM

class TravelVectorStore:
    """
    FAISS Vector Store for Travel Information.
    Uses nomic-embed-text embeddings (768-dim) and Inner Product index (Cosine Similarity).
    """
    def __init__(self, index_path: str = None, embedding_provider: Optional[NomicEmbeddingProvider] = None):
        self.embedding_provider = embedding_provider or NomicEmbeddingProvider()
        self.index_path = index_path or os.path.join(os.path.dirname(__file__), "..", "data", "faiss_index.bin")
        self.meta_path = os.path.join(os.path.dirname(__file__), "..", "data", "faiss_metadata.json")
        
        self.documents: List[Dict[str, Any]] = []
        self.index: Optional[faiss.Index] = None
        self._init_or_load()

    def _init_or_load(self):
        os.makedirs(os.path.dirname(self.index_path), exist_ok=True)
        if os.path.exists(self.index_path) and os.path.exists(self.meta_path):
            try:
                self.index = faiss.read_index(self.index_path)
                with open(self.meta_path, "r", encoding="utf-8") as f:
                    self.documents = json.load(f)
                print(f"[TravelVectorStore] Loaded {self.index.ntotal} vectors from {self.index_path}")
                return
            except Exception as e:
                print(f"[TravelVectorStore] Error loading existing index: {e}. Creating new.")

        # Create fresh Inner Product index (with normalized vectors => cosine similarity)
        self.index = faiss.IndexFlatIP(EMBEDDING_DIM)
        self.documents = []

    def add_documents(self, docs: List[Dict[str, Any]], persist: bool = True):
        """
        Adds list of travel documents to FAISS index.
        Each doc should have:
        {
           'id': '...',
           'destination': 'Tokyo',
           'day': 1, # or None for general
           'category': 'Attraction' | 'Dining' | 'Hotel' | 'Transport' | 'Tip',
           'title': '...',
           'content': '...',
           'cost_usd': 25,
           'tags': ['cultural', 'budget', 'shrine']
        }
        """
        if not docs:
            return

        texts_to_embed = [
            f"{d.get('destination', '')} {d.get('title', '')}: {d.get('content', '')} (Tags: {', '.join(d.get('tags', []))})"
            for d in docs
        ]

        embeddings = self.embedding_provider.embed_texts(texts_to_embed)
        self.index.add(embeddings)
        self.documents.extend(docs)

        if persist:
            self.save()

    def search(self, query: str, top_k: int = 5, destination_filter: str = None) -> List[Dict[str, Any]]:
        """
        Search documents by query string.
        """
        if self.index is None or self.index.ntotal == 0:
            return []

        query_vec = self.embedding_provider.embed_query(query).reshape(1, -1)
        
        # Retrieve slightly more than top_k if filtering by destination
        fetch_k = min(self.index.ntotal, top_k * 3 if destination_filter else top_k)
        scores, indices = self.index.search(query_vec, fetch_k)

        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx < 0 or idx >= len(self.documents):
                continue
            doc = dict(self.documents[idx])
            doc["score"] = float(score) # Cosine similarity (typically 0.0 to 1.0)
            
            if destination_filter:
                doc_dest = doc.get("destination", "").lower()
                filter_dest = destination_filter.lower()
                if filter_dest not in doc_dest and doc_dest not in filter_dest:
                    continue

            results.append(doc)
            if len(results) >= top_k:
                break

        return results

    def save(self):
        """
        Persist FAISS index and documents metadata.
        """
        try:
            faiss.write_index(self.index, self.index_path)
            with open(self.meta_path, "w", encoding="utf-8") as f:
                json.dump(self.documents, f, indent=2, ensure_ascii=False)
            print(f"[TravelVectorStore] Successfully saved {self.index.ntotal} items to disk.")
        except Exception as e:
            print(f"[TravelVectorStore] Failed to save FAISS index: {e}")

    def total_documents(self) -> int:
        return self.index.ntotal if self.index else 0
