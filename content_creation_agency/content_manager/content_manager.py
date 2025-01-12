from agency_swarm import Agent

class ContentManager(Agent):
    def __init__(self):
        super().__init__(
            name="Content Manager",
            description="Manages content ideation and script creation process",
            instructions="./instructions.md",
            tools_folder="./tools",
            temperature=0.7,
            max_prompt_tokens=8000
        ) 