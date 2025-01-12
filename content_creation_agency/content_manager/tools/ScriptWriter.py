from agency_swarm.tools import BaseTool
from pydantic import Field
import os
from pathlib import Path

class ScriptWriter(BaseTool):
    """
    Writes and saves script drafts in Markdown format.
    """
    title: str = Field(..., description="Title of the content")
    outline: str = Field(..., description="Detailed outline of the script")
    target_audience: str = Field(..., description="Target audience for the content")
    
    def run(self):
        script_content = f"""# {self.title}

## Target Audience
{self.target_audience}

## Script
{self.outline}
"""
        
        # Create scripts directory if it doesn't exist
        scripts_dir = Path("scripts")
        scripts_dir.mkdir(exist_ok=True)
        
        # Save script to file
        filename = f"scripts/{self.title.lower().replace(' ', '_')}.md"
        with open(filename, 'w') as f:
            f.write(script_content)
            
        return f"Script saved to {filename}"

if __name__ == "__main__":
    tool = ScriptWriter(
        title="Understanding AI Agents",
        outline="Introduction to AI agents...",
        target_audience="Tech enthusiasts and developers"
    )
    print(tool.run()) 