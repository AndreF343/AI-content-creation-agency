from agency_swarm.tools import BaseTool
from pydantic import Field
import os
from dotenv import load_dotenv
from googleapiclient.discovery import build

load_dotenv()

youtube = build('youtube', 'v3', developerKey=os.getenv('YOUTUBE_API_KEY'))

class CompetitorAnalyzer(BaseTool):
    """
    Analyzes competitor channels and their content performance.
    """
    keywords: str = Field(..., description="Keyword to search for in the competitor's content")
    max_results: int = Field(default=5, description="Maximum number of channels to analyze")
    videos_per_channel: int = Field(default=5, description="Number of videos to analyze per channel")
    
    def run(self):
        """
        Analyzes competitor channels and their recent videos based on keywords.
        """
        try:
            search_response = youtube.search().list(
                q=self.keywords,
                type='channel',
                part='snippet',
                maxResults=self.max_results
            ).execute()

            result = "Competitor Analysis:\n\n"
            
            for item in search_response['items']:
                channel_id = item['snippet']['channelId']
                channel_title = item['snippet']['title']
                
                # Get channel statistics
                channel_stats = youtube.channels().list(
                    part='statistics,contentDetails',
                    id=channel_id
                ).execute()

                stats = channel_stats['items'][0]['statistics']
                
                # Get channel's recent videos
                playlist_id = channel_stats['items'][0]['contentDetails']['relatedPlaylists']['uploads']
                
                result += f"Channel: {channel_title}\n"
                result += f"ID: {channel_id}\n"
                result += f"Subscribers: {stats.get('subscriberCount', 'N/A')}\n"
                result += f"Total Views: {stats.get('viewCount', 'N/A')}\n"
                result += f"Total Videos: {stats.get('videoCount', 'N/A')}\n\n"
                
                # Get recent videos
                videos_response = youtube.playlistItems().list(
                    part='snippet',
                    playlistId=playlist_id,
                    maxResults=self.videos_per_channel
                ).execute()
                
                result += "Recent Videos:\n"
                
                video_ids = [item['snippet']['resourceId']['videoId'] 
                            for item in videos_response['items']]
                
                # Get video statistics
                if video_ids:
                    videos_stats = youtube.videos().list(
                        part='statistics,snippet',
                        id=','.join(video_ids)
                    ).execute()
                    
                    for video in videos_stats['items']:
                        result += f"Title: {video['snippet']['title']}\n"
                        result += f"Views: {video['statistics'].get('viewCount', 'N/A')}\n"
                        result += f"Likes: {video['statistics'].get('likeCount', 'N/A')}\n"
                        result += f"Comments: {video['statistics'].get('commentCount', 'N/A')}\n\n"
                
                result += "-" * 50 + "\n\n"
            
            return result
            
        except Exception as e:
            return f"Error analyzing competitors: {str(e)}"

if __name__ == "__main__":
    tool = CompetitorAnalyzer(
        keywords="AI technology tutorials",
        max_results=3,
        videos_per_channel=5
    )
    print(tool.run()) 