from agency_swarm.tools import BaseTool
from pydantic import Field
import os
from dotenv import load_dotenv
import openai

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

class ContentIdeaGenerator(BaseTool):
    """
    Generates content ideas using OpenAI's latest model based on trends and performance data.
    """
    trends_data: str = Field(..., description="Trend analysis data from the Trend Analyzer")
    youtube_data: str = Field(..., description="YouTube performance data from the YouTube Analyzer")
    
    def run(self):
        prompt = f"""Based on the following data:
        
        Trends Analysis:
        {self.trends_data}
        
        YouTube Performance:
        {self.youtube_data}
        
        Generate 5 compelling content ideas that fill identified content gaps and align with current trends.
        For each idea, provide:
        1. Title
        2. Brief description
        3. Target audience
        4. Expected impact
        """
        
        response = openai.chat.completions.create(
            model="gpt-4-0125-preview",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        
        return response.choices[0].message.content

if __name__ == "__main__":
    tool = ContentIdeaGenerator(
        trends_data="AI trends in Q1 2024...",
        youtube_data="Channel performance metrics..."
    )
    print(tool.run()) 