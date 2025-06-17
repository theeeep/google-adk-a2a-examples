import json

from google.adk.agents.llm_agent import Agent

# from google.adk.models.lite_llm import LiteLlm
from mcp.client.stdio import StdioServerParameters

# from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioServerParameters
from config import NOTION_API_KEY
from notion_agent.prompt import NOTION_PROMPT
from utils.custom_adk_patches import CustomMCPToolset


def create_notion_agent() -> Agent:
    return Agent(
        name="notion_agent_mcp",
        model="gemini-2.0-flash",
        description="Specialized agent for retrieving information from Notion workspace via MCPToolset.",
        instruction=NOTION_PROMPT,
        tools=[
            CustomMCPToolset(
                connection_params=StdioServerParameters(
                    command="npx",
                    args=["-y", "@notionhq/notion-mcp-server"],
                    env={
                        "OPENAPI_MCP_HEADERS": json.dumps(
                            {
                                "Authorization": f"Bearer {NOTION_API_KEY}",
                                "Notion-Version": "2022-06-28",
                            }
                        )
                    },
                )
            )
        ],
    )


root_agent = create_notion_agent()
