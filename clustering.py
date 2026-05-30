import numpy as np

class KMeansClusterer:
    def __init__(self, n_clusters=2):
        self.n_clusters = n_clusters
        self.kmeans = None

    def cluster_embeddings(self, embeddings):
        """Partitions embedding vectors into K distinct clusters via KMeans."""
        try:
            from sklearn.cluster import KMeans
            # Constrain K dynamically based on tab counts
            k = min(self.n_clusters, len(embeddings))
            if k <= 0:
                return []
            self.kmeans = KMeans(n_clusters=k, random_state=42, n_init='auto')
            assignments = self.kmeans.fit_predict(embeddings)
            return list(assignments)
        except ImportError:
            # Fallback simple partition algorithm
            print("Warning: scikit-learn not available. Running basic vector clustering.")
            k = min(self.n_clusters, len(embeddings))
            if k <= 0:
                return []
            # Simulated centroid assignments based on dimensions
            assignments = []
            for emb in embeddings:
                # Group by dominant index values
                first_half = np.sum(emb[:len(emb)//2])
                second_half = np.sum(emb[len(emb)//2:])
                assignments.append(0 if first_half >= second_half else 1)
            return assignments

class KeywordsExtractor:
    @staticmethod
    def extract_keywords(texts, max_features=3):
        """Extracts top words using TF-IDF weighting models."""
        try:
            from sklearn.feature_extraction.text import TfidfVectorizer
            vectorizer = TfidfVectorizer(stop_words='english', max_features=10)
            tfidf_matrix = vectorizer.fit_transform(texts)
            feature_names = vectorizer.get_feature_names_out()
            
            # Sum scores across all documents
            scores = np.asarray(tfidf_matrix.sum(axis=0)).ravel()
            top_indices = scores.argsort()[::-1][:max_features]
            
            keywords = [feature_names[i] for i in top_indices]
            return keywords
        except Exception:
            # Basic fallback text word tokenizer
            all_words = []
            stopwords = {'and', 'the', 'for', 'with', 'your', 'from', 'this', 'that', 'our', 'what'}
            for text in texts:
                words = [w.strip('.,()-\"').lower() for w in text.split()]
                all_words.extend([w for w in words if len(w) > 3 and w not in stopwords])
            
            from collections import Counter
            counts = Counter(all_words)
            return [w for w, _ in counts.most_common(max_features)]
