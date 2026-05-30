from clustering import KeywordsExtractor

class WorkspaceLabeler:
    @staticmethod
    def generate_label(titles, urls, cluster_keywords=None):
        """Generates dynamic human-centered labels based on keywords, titles and urls."""
        combined = " ".join(titles + urls).lower()
        
        # 1. Custom High-Fidelity Override Rules
        if 'figma' in combined or 'behance' in combined or 'dribbble' in combined:
            return "🎨 Creative UI Design"
        
        if 'chatgpt' in combined or 'claude' in combined or 'perplexity' in combined or 'deepseek' in combined or 'gemini' in combined:
            return "🔮 AI Research"
        
        if 'python' in combined:
            return "🐍 Python Learning"
        
        if 'react' in combined or 'typescript' in combined or 'github' in combined or 'stackoverflow' in combined:
            return "💻 Software Development"
        
        if 'youtube' in combined or 'spotify' in combined or 'music' in combined or 'song' in combined or 'justin bieber' in combined:
            return "🎵 Music Discovery"
        
        if 'amazon' in combined or 'myntra' in combined or 'flipkart' in combined or 'shop' in combined:
            return "🛍️ Shopping Comparison"
            
        if 'coursera' in combined or 'udemy' in combined or 'learn' in combined or 'lecture' in combined:
            return "📚 Skill Learning"
            
        # 2. Secondary TF-IDF dynamic keywords mapping
        if not cluster_keywords:
            cluster_keywords = KeywordsExtractor.extract_keywords(titles, max_features=2)
            
        if len(cluster_keywords) > 0:
            primary_topic = cluster_keywords[0].capitalize()
            # Dynamic names matching (e.g. "Vite Development", "Astronomy Research")
            if 'tutorial' in combined or 'learn' in combined:
                return f"📖 {primary_topic} Learning"
            if 'code' in combined or 'dev' in combined:
                return f"⚙️ {primary_topic} Development"
            return f"🔬 {primary_topic} Research"
            
        return "🌐 Dynamic Exploration"
