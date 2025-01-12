from agency_swarm.tools import BaseTool
from pydantic import Field
import os
from dotenv import load_dotenv
from googleapiclient.discovery import build
from textblob import TextBlob
from collections import Counter

load_dotenv()

youtube = build('youtube', 'v3', developerKey=os.getenv('YOUTUBE_API_KEY'))

class SentimentAnalyzer(BaseTool):
    """
    Analyzes sentiment and engagement in video comments.
    """
    video_id: str = Field(..., description="YouTube video ID to analyze comments from")
    max_comments: int = Field(default=100, description="Maximum number of comments to analyze")
    
    def run(self):
        # Get video comments
        comments = []
        next_page_token = None
        
        while len(comments) < self.max_comments:
            request = youtube.commentThreads().list(
                part='snippet',
                videoId=self.video_id,
                maxResults=min(100, self.max_comments - len(comments)),
                pageToken=next_page_token,
                textFormat='plainText'
            )
            
            try:
                response = request.execute()
            except:
                break
                
            for item in response['items']:
                comment = item['snippet']['topLevelComment']['snippet']
                comments.append({
                    'text': comment['textDisplay'],
                    'likes': comment['likeCount'],
                    'date': comment['publishedAt']
                })
            
            next_page_token = response.get('nextPageToken')
            if not next_page_token:
                break
        
        # Analyze sentiment
        sentiments = []
        topics = Counter()
        
        for comment in comments:
            blob = TextBlob(comment['text'])
            sentiment = blob.sentiment.polarity
            sentiments.append(sentiment)
            
            # Extract common phrases (potential topics)
            phrases = blob.noun_phrases
            topics.update(phrases)
        
        analysis = {
            'overall_sentiment': sum(sentiments) / len(sentiments) if sentiments else 0,
            'sentiment_distribution': {
                'positive': len([s for s in sentiments if s > 0.2]),
                'neutral': len([s for s in sentiments if -0.2 <= s <= 0.2]),
                'negative': len([s for s in sentiments if s < -0.2])
            },
            'common_topics': dict(topics.most_common(10)),
            'total_comments_analyzed': len(comments)
        }
        
        return analysis

if __name__ == "__main__":
    tool = SentimentAnalyzer(video_id="VIDEO_ID", max_comments=100)
    print(tool.run()) 