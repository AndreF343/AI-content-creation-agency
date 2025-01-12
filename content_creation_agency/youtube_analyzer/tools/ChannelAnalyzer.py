from agency_swarm.tools import BaseTool
from pydantic import Field
import os
from dotenv import load_dotenv
from googleapiclient.discovery import build

load_dotenv()

youtube = build('youtube', 'v3', developerKey=os.getenv('YOUTUBE_API_KEY'))

class ChannelAnalyzer(BaseTool):
    """
    Analyzes YouTube channel performance and demographics.
    """
    channel_id: str = Field(..., description="YouTube channel ID to analyze")
    
    def run(self):
        # Get channel statistics
        channel_response = youtube.channels().list(
            part='statistics,snippet',
            id=self.channel_id
        ).execute()
        
        # Get channel's videos
        videos_response = youtube.search().list(
            part='id,snippet',
            channelId=self.channel_id,
            order='date',
            type='video',
            maxResults=50
        ).execute()
        
        # Get video statistics
        video_ids = [item['id']['videoId'] for item in videos_response['items']]
        videos_stats = youtube.videos().list(
            part='statistics',
            id=','.join(video_ids)
        ).execute()
        
        return {
            'channel_stats': channel_response['items'][0]['statistics'],
            'recent_videos': [{
                'title': video['snippet']['title'],
                'stats': stats['statistics']
            } for video, stats in zip(videos_response['items'], videos_stats['items'])]
        }

if __name__ == "__main__":
    tool = ChannelAnalyzer(channel_id="UCv2KxkHBzmaT1K3LahubXzA")
    print(tool.run()) 