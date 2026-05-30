import numpy as np

class EmbeddingsEngine:
    def __init__(self, model_name='all-MiniLM-L6-v2'):
        self.model_name = model_name
        self.model = None

    def load_model(self):
        """Loads sentence-transformers model inside Python ML worker context."""
        if self.model is not None:
            return True
        try:
            from sentence_transformers import SentenceTransformer
            self.model = SentenceTransformer(self.model_name)
            return True
        except ImportError:
            print("Warning: sentence-transformers library not installed. Loading mock embedding coordinates.")
            return False

    def get_embeddings(self, texts):
        """Computes MiniLM text embeddings. Falls back to normalized vectors if offline/mock."""
        if self.load_model() and self.model is not None:
            embeddings = self.model.encode(texts)
            return np.array(embeddings)
        
        # Mock/Offline Fallback Vector Space
        print("Executing fallback vector calculations locally.")
        dims = 384  # MiniLM dimension
        vectors = []
        for text in texts:
            t = text.lower()
            vec = np.zeros(dims)
            # Seed deterministic variations based on keyword distributions
            if 'figma' in t or 'dribbble' in t or 'behance' in t or 'design' in t:
                vec[0:50] = 0.8
            if 'code' in t or 'developer' in t or 'github' in t or 'python' in t:
                vec[50:100] = 0.8
            if 'chatgpt' in t or 'claude' in t or 'openai' in t or 'ai' in t:
                vec[100:150] = 0.8
            if 'amazon' in t or 'buy' in t or 'shopping' in t or 'cart' in t:
                vec[150:200] = 0.8
            if 'music' in t or 'song' in t or 'lyrics' in t or 'spotify' in t:
                vec[200:250] = 0.8
            
            # Add small noise for clustering stability
            vec += np.random.normal(0, 0.05, dims)
            norm = np.linalg.norm(vec)
            vectors.append(vec / (norm if norm > 0 else 1))
            
        return np.array(vectors)
