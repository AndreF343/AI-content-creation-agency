from agency_swarm.tools import BaseTool
from pydantic import Field
import os
from dotenv import load_dotenv
from googleapiclient.discovery import build
from datetime import datetime, timedelta

load_dotenv()

youtube = build('youtube', 'v3', developerKey=os.getenv('YOUTUBE_API_KEY'))

class ChannelPerformanceAnalyzer(BaseTool):
    """
    Analyzes channel demographics and video performance.
    """
    channel_id: str = Field(..., description="YouTube channel ID to analyze")
    video_limit: int = Field(default=10, description="Number of recent videos to analyze")
    
    def run(self):
        try:
            # Get channel statistics
            channel_response = youtube.channels().list(
                part='statistics,snippet,contentDetails',
                id=self.channel_id
            ).execute()
            
            if not channel_response.get('items'):
                return f"No channel found with ID: {self.channel_id}"
            
            channel_info = channel_response['items'][0]
            
            # Get channel's recent videos
            playlist_id = channel_info['contentDetails']['relatedPlaylists']['uploads']
            
            # Get video IDs from uploads playlist
            video_ids = []
            next_page_token = None
            
            while len(video_ids) < self.video_limit:
                playlist_response = youtube.playlistItems().list(
                    part='snippet',
                    playlistId=playlist_id,
                    maxResults=min(50, self.video_limit - len(video_ids)),
                    pageToken=next_page_token
                ).execute()
                
                video_ids.extend([item['snippet']['resourceId']['videoId'] 
                                for item in playlist_response['items']])
                
                next_page_token = playlist_response.get('nextPageToken')
                if not next_page_token:
                    break
            
            # Get detailed video statistics
            videos_stats = youtube.videos().list(
                part='statistics,snippet',
                id=','.join(video_ids)
            ).execute()
            
            # Compile report
            report = "Channel Performance Analysis\n\n"
            
            # Channel Overview
            report += "Channel Overview:\n"
            report += f"Title: {channel_info['snippet']['title']}\n"
            report += f"Total Subscribers: {channel_info['statistics']['subscriberCount']}\n"
            report += f"Total Views: {channel_info['statistics']['viewCount']}\n"
            report += f"Total Videos: {channel_info['statistics']['videoCount']}\n\n"
            
            # Recent Videos Performance
            report += "Recent Videos Performance:\n\n"
            
            video_performances = []
            for video in videos_stats['items']:
                stats = video['statistics']
                video_performances.append({
                    'title': video['snippet']['title'],
                    'views': int(stats.get('viewCount', 0)),
                    'likes': int(stats.get('likeCount', 0)),
                    'comments': int(stats.get('commentCount', 0))
                })
            
            # Sort videos by views
            video_performances.sort(key=lambda x: x['views'], reverse=True)
            
            for video in video_performances:
                report += f"Title: {video['title']}\n"
                report += f"Views: {video['views']:,}\n"
                report += f"Likes: {video['likes']:,}\n"
                report += f"Comments: {video['comments']:,}\n\n"
            
            # Performance Summary
            avg_views = sum(v['views'] for v in video_performances) / len(video_performances)
            avg_engagement = sum(v['likes'] + v['comments'] for v in video_performances) / len(video_performances)
            
            report += "Performance Summary:\n"
            report += f"Average Views: {avg_views:,.0f}\n"
            report += f"Average Engagement (Likes + Comments): {avg_engagement:,.0f}\n"
            
            return report
            
        except Exception as e:
            return f"Error analyzing channel performance: {str(e)}"

if __name__ == "__main__":
    tool = ChannelPerformanceAnalyzer(
        channel_id="UCv2KxkHBzmaT1K3LahubXzA",
        video_limit=10
    )
    print(tool.run()) 