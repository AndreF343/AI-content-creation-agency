from agency_swarm.tools import BaseTool
from pydantic import Field
import os
from dotenv import load_dotenv
from tavily import TavilyClient

load_dotenv()

tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

class TavilySearchTool(BaseTool):
    """
    Searches the web for AI trends using Tavily API.
    """
    query: str = Field(..., description="Search query for AI trends")
    
    def run(self):
        response = tavily_client.search(
            query=self.query,
            search_depth="advanced",
            include_answer=True,
            include_raw_content=True
        )
        
        return response

if __name__ == "__main__":
    tool = TavilySearchTool(query="latest developments in AI agents")
    print(tool.run()) 