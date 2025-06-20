# google-adk-a2a-examples

A collection of example implementations and learning exercises for building agents with the Google Agent Development Kit (ADK) and integrating them using the Agent-to-Agent (A2A) framework.

## Project Setup

This project uses `uv` for dependency management. If you don't have `uv` installed, you can install it using pip:

### Homebrew

If you're on macOS and use Homebrew, you can install `uv` with:

```bash
brew install uv
```

However, pip can also be used:
```bash
pip install uv
```

### 1. Clone the repository:

```bash
git clone https://github.com/theeeep/google-adk-a2a-examples
cd google-adk-a2a-examples
```

### 2. Install Dependencies:

First, ensure you have a Python version compatible with `uv` (>=3.8). Then, sync the project dependencies:

```bash
uv sync
```

### 3. Environment Variables:

Create a `.env` file in the root of the project to store your API keys and other sensitive information. For the Notion agent, you will need your Notion API Key:

```
NOTION_API_KEY="your_notion_api_key_here"
```

Replace `"your_notion_api_key_here"` with your actual Notion integration token.

## Running the Agents

Detailed instructions on how to run each agent will be provided here.

### Notion Agent

The Notion agent is designed to retrieve information from your Notion workspace.

To run the Notion agent, you might use a command similar to this (depending on how the ADK agent is exposed):

```bash
# This is a placeholder. Actual command will depend on your ADK application setup.
# Example: uv run python -m your_app.main
```

## Project Structure

*   `main.py`: Main entry point for the application (if applicable).
*   `pyproject.toml`: Project metadata and dependency management.
*   `notion_agent/`: Contains the Notion agent implementation.
    *   `agent.py`: Defines the Notion ADK agent.
    *   `prompt.py`: Stores the prompt used by the Notion agent.
*   `elevenlabs_agent/`: Contains the ElevenLabs agent implementation.
    *   `agent_executor.py`: Implements the `AgentExecutor` for the ElevenLabs agent.
    *   `agent.py`: Defines the ElevenLabs ADK agent.
