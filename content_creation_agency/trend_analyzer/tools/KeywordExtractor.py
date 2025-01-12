from agency_swarm.tools import BaseTool
from pydantic import Field
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.tag import pos_tag
from collections import Counter

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('stopwords')

class KeywordExtractor(BaseTool):
    """
    Extracts keywords from news articles using NLTK.
    """
    text: str = Field(..., description="Article text to analyze")
    
    def run(self):
        # Tokenize and tag parts of speech
        tokens = word_tokenize(self.text.lower())
        tagged = pos_tag(tokens)
        
        # Filter for nouns and adjectives
        stop_words = set(stopwords.words('english'))
        keywords = [word for word, tag in tagged 
                   if word not in stop_words 
                   and word.isalnum() 
                   and tag in ['NN', 'NNS', 'NNP', 'NNPS', 'JJ']]
        
        # Count frequencies
        keyword_freq = Counter(keywords).most_common(10)
        
        return dict(keyword_freq)

if __name__ == "__main__":
    tool = KeywordExtractor(
        text="AI agents are revolutionizing content creation..."
    )
    print(tool.run()) 