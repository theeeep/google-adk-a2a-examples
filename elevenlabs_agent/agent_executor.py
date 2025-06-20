import logging
from typing import override

from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events import EventQueue
from a2a.types import AgentCard
from google.adk.agents import Agent
from google.adk.runners import Runner

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ElevenLabsADKAgentExecutor(AgentExecutor):
    def __init__(self, agent: Agent, agent_card: AgentCard, runner: Runner):
        ...
        # logger.info(f"Initializing ElevenLabsADKAgentExecutor for agent: {agent.name}")

        # self.agent = agent
        # self.agent_card = agent_card
        # self.runner = runner

        # self.session_service = runner.session_service
        # self.artifact_service = runner.artifact_service

    @override
    def execute(self, context: RequestContext, event_queue: EventQueue) -> None: ...

    @override
    async def cancel(
        self, context: RequestContext, event_queue: EventQueue
    ) -> None: ...
