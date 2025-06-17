"""ElevenLabs Agent implementation using ADK and MCPToolset with custom timeout patch."""

import os

from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from mcp import StdioServerParameters

from config import ELEVENLABS_API_KEY
from elevenlabs_agent.prompt import ELEVENLABS_PROMPT
from utils.custom_adk_patches import CustomMCPToolset


def create_elevenlabs_agent() -> Agent:
    return Agent(
        name="elevenlabs_agent_mcp",
        model=LiteLlm(
            model="anthropic/claude-3-5-sonnet-20241022",
            api_key=os.getenv("ANTHROPIC_API_KEY"),
        ),
        description="Specialized agent for converting text to speech using ElevenLabs via MCPToolset.",
        instruction=ELEVENLABS_PROMPT,
        tools=[
            CustomMCPToolset(
                connection_params=StdioServerParameters(
                    command="uvx",
                    args=["elevenlabs-mcp"],
                    env={"ELEVENLABS_API_KEY": ELEVENLABS_API_KEY},
                )
            )
        ],
    )


root_agent = create_elevenlabs_agent()
