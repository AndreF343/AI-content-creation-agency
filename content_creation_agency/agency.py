from agency_swarm import Agency
from agency_swarm.util import set_openai_key
from content_manager.content_manager import ContentManager
from trend_analyzer.trend_analyzer import TrendAnalyzer
from youtube_analyzer.youtube_analyzer import YouTubeAnalyzer
import os
from dotenv import load_dotenv
import nltk

# Load environment variables
load_dotenv()

# Download all required NLTK data
nltk_resources = ['punkt', 'punkt_tab', 'averaged_perceptron_tagger', 'averaged_perceptron_tagger_eng', 'stopwords']
for resource in nltk_resources:
    try:
        nltk.download(resource, quiet=True)
    except Exception as e:
        print(f"Warning: Failed to download {resource}: {str(e)}")

# Set OpenAI API key for agency_swarm
set_openai_key(os.getenv('OPENAI_API_KEY'))

# Initialize agents
content_manager = ContentManager()
trend_analyzer = TrendAnalyzer()
youtube_analyzer = YouTubeAnalyzer()

# Create agency with communication flows
agency = Agency(
    [
        content_manager,  # Content Manager is the entry point
        [content_manager, trend_analyzer],  # Content Manager can communicate with Trend Analyzer
        [content_manager, youtube_analyzer],  # Content Manager can communicate with YouTube Analyzer
    ],
    shared_instructions="agency_manifesto.md",
    temperature=0.7
)

if __name__ == "__main__":
    # agency.run_demo() 
    agency.demo_gradio(height=900)