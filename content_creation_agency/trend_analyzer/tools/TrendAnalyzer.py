from agency_swarm.tools import BaseTool
from pydantic import Field
from pytrends.request import TrendReq
import pandas as pd
import time

class TrendAnalyzer(BaseTool):
    """
    Analyzes keywords using Google Trends via pytrends.
    """
    keywords: list = Field(..., description="List of keywords to analyze")
    
    def run(self):
        try:
            # Initialize with backoff
            pytrends = TrendReq(hl='en-US', tz=360, retries=2, backoff_factor=1)
            results = {
                'interest_over_time': {},
                'related_queries': {}
            }
            
            # Process each keyword with delay between requests
            for keyword in self.keywords[:5]:
                try:
                    # Add delay between requests
                    time.sleep(2)
                    
                    # Build payload for single keyword
                    pytrends.build_payload(
                        [keyword],
                        cat=0,
                        timeframe='today 3-m'
                    )
                    
                    # Get interest over time
                    interest_df = pytrends.interest_over_time()
                    if not interest_df.empty:
                        results['interest_over_time'][keyword] = interest_df[keyword].to_dict()
                    
                    # Add delay before next request
                    time.sleep(2)
                    
                    # Get related queries
                    related = pytrends.related_queries()
                    if related and keyword in related and related[keyword]:
                        results['related_queries'][keyword] = related[keyword]
                        
                except Exception as e:
                    print(f"Error processing keyword '{keyword}': {str(e)}")
                    continue
            
            return results
            
        except Exception as e:
            return f"Error in trend analysis: {str(e)}"

if __name__ == "__main__":
    tool = TrendAnalyzer(keywords=["ChatGPT"])
    print(tool.run()) 