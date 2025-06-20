import logging
import os

import click
import uvicorn

# A2A server imports
from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore
from a2a.types import AgentCapabilities, AgentCard, AgentSkill

# from dotenv import load_dotenv
# ADK imports
from google.adk.artifacts import InMemoryArtifactService
from google.adk.memory.in_memory_memory_service import InMemoryMemoryService
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService

# from elevenlabs_agent import agent_executor
from elevenlabs_agent.agent import create_elevenlabs_agent
from elevenlabs_agent.agent_executor import ElevenLabsADKAgentExecutor

# Basic logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@click.command()
@click.option(
    "--host",
    "host",
    default=os.getenv("A2A_ELEVENLABS_HOST", "localhost"),
    show_default=True,
    help="Host for the ElevenLabs agent server.",
)
@click.option(
    "--port",
    "port",
    default=int(os.getenv("A2A_ELEVENLABS_PORT", 8003)),  # Adjusted default port
    show_default=True,
    type=int,
    help="Port for the ElevenLabs agent server.",
)
def main(host: str, port: int) -> None:
    if not os.getenv("ELEVENLABS_API_KEY"):
        logger.warning(
            "ELEVENLABS_API_KEY environment variable not set. "
            "The ElevenLabs MCP server might fail to authenticate."
        )

    eleven_skill = AgentSkill(
        id="text_to_speech",
        name="Convert text to speech",
        description="Takes input text and returns an audio file of the spoken text using ElevenLabs.",
        tags=["tts", "audio", "speech", "elevenlabs"],
        examples=[
            "What is the weather like today?",
            "Please read the following text out loud: The quick brown fox jumped over the lazy dog.",
        ],
    )
    agent_card = AgentCard(
        name="ElevenLabs TTS Agent",
        description="Provides text-to-speech services using ElevenLabs.",
        url=f"http://{host}:{port}/",  # URL is dynamically set here
        version="1.0.0",
        defaultInputModes=["text"],  # Agent primarily takes text
        defaultOutputModes=[
            "text",
            "audio",
        ],  # Agent primarily outputs audio (e.g., audio/mpeg)
        capabilities=AgentCapabilities(
            streaming=False, pushNotifications=False
        ),  # TTS is typically not streaming response
        skills=[eleven_skill],
    )

    agent = create_elevenlabs_agent()

    runner = Runner(
        agent=agent,
        app_name=agent_card.name,
        artifact_service=InMemoryArtifactService(),
        session_service=InMemorySessionService(),
        memory_service=InMemoryMemoryService(),
    )

    agent_executor = ElevenLabsADKAgentExecutor(
        agent=agent,
        agent_card=agent_card,
        runner=runner,
    )

    request_handler = DefaultRequestHandler(
        agent_executor=agent_executor,
        task_store=InMemoryTaskStore(),
    )

    a2a_app = A2AStarletteApplication(
        agent_card=agent_card,
        http_handler=request_handler,
    )
    logger.info(f"Starting ElevenLabs Agent server on http://{host}:{port}")
    logger.info(f"Agent Name: {agent_card.name}, Version: {agent_card.version}")

    if agent_card.skills:
        for skill in agent_card.skills:
            logger.info(f"  Skill: {skill.name} (ID: {skill.id}, Tags: {skill.tags})")

    uvicorn.run(a2a_app.build(), host=host, port=port)


if __name__ == "__main__":
    main()
