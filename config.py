"""Configuration settings for the ADK A2A Notion-ElevenLabs integration."""

import os
from typing import Final

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Keys
GOOGLE_API_KEY: Final[str] = os.getenv("GOOGLE_API_KEY", "")
NOTION_API_KEY: Final[str] = os.getenv("NOTION_API_KEY", "")
ELEVENLABS_API_KEY: Final[str] = os.getenv("ELEVENLABS_API_KEY", "")

# A2A Service URLs
ELEVENLABS_AGENT_A2A_URL: Final[str] = os.getenv(
    "ELEVENLABS_AGENT_A2A_URL", "http://localhost:8003"
)
NOTION_AGENT_A2A_URL: Final[str] = os.getenv(
    "NOTION_AGENT_A2A_URL", "http://localhost:8002"
)
HOST_AGENT_A2A_URL: Final[str] = os.getenv(
    "HOST_AGENT_A2A_URL", "http://localhost:8001"
)

# MCP Server Configurations
NOTION_MCP_PORT: Final[int] = int(os.getenv("NOTION_MCP_PORT", "50051"))
ELEVENLABS_MCP_PORT: Final[int] = int(os.getenv("ELEVENLABS_MCP_PORT", "50052"))

# MCP Server References (for ADK MCPToolset)
NOTION_MCP_REFERENCE: Final[str] = "notionApi"
ELEVENLABS_MCP_REFERENCE: Final[str] = "elevenLabsApi"

# ADK Configuration
ADK_MODEL: Final[str] = os.getenv("ADK_MODEL", "gemini-2.0-flash")
