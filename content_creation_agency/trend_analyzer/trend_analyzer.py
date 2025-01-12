from agency_swarm import Agent

class TrendAnalyzer(Agent):
    def __init__(self):
        super().__init__(
            name="Trend Analyzer",
            description="Analyzes AI trends and identifies content opportunities",
            instructions="./instructions.md",
            tools_folder="./tools",
            temperature=0.5,
            max_prompt_tokens=8000
        ) 