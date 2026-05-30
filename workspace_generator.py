from embeddings import EmbeddingsEngine
from clustering import KMeansClusterer, KeywordsExtractor
from workspace_labeler import WorkspaceLabeler

class WorkspaceGenerator:
    def __init__(self, n_clusters=2):
        self.embeddings_engine = EmbeddingsEngine()
        self.clusterer = KMeansClusterer(n_clusters=n_clusters)

    def generate_workspaces(self, tabs):
        """Processes raw tabs, clusters them, and outputs dynamically labeled workspace dictionaries."""
        if not tabs:
            return []

        # Extract features/text signals
        texts = [f"{tab.get('title', '')} {tab.get('url', '')}" for tab in tabs]
        
        # 1. Compute Embeddings
        embeddings = self.embeddings_engine.get_embeddings(texts)
        
        # 2. KMeans Clustering (Stage 4)
        cluster_assignments = self.clusterer.cluster_embeddings(embeddings)
        
        # Group tabs by cluster assignments
        clusters = {}
        for idx, assignment in enumerate(cluster_assignments):
            if assignment not in clusters:
                clusters[assignment] = []
            clusters[assignment].append(tabs[idx])
            
        # 3. Workspace Labeling (Stage 5)
        workspaces = []
        for cluster_id, cluster_tabs in clusters.items():
            c_titles = [t.get('title', '') for t in cluster_tabs]
            c_urls = [t.get('url', '') for t in cluster_tabs]
            
            # TF-IDF Keywords extraction
            keywords = KeywordsExtractor.extract_keywords(c_titles, max_features=2)
            
            # Generate premium, dynamic label
            label = WorkspaceLabeler.generate_label(c_titles, c_urls, keywords)
            
            # Form dynamic workspace coordinates
            workspaces.append({
                "label": label,
                "tabs": cluster_tabs,
                "keywords": keywords
            })
            
        return workspaces
