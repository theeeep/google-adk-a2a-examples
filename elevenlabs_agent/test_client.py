import asyncio
import os
import traceback
from typing import Any, Dict
from uuid import uuid4

import httpx
from a2a.client import A2AClient
from a2a.types import (
    GetTaskRequest,
    GetTaskResponse,
    GetTaskSuccessResponse,
    MessageSendParams,
    SendMessageRequest,
    SendMessageResponse,
    SendMessageSuccessResponse,
    TaskQueryParams,
)
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

AGENT_URL = os.getenv("ELEVENLABS_AGENT_A2A_URL", "http://localhost:8003")


def create_send_message_payload(
    text: str, task_id: str | None = None, context_id: str | None = None
) -> Dict[str, Any]:
    payload: Dict[str, Any] = {
        "message": {
            "role": "user",
            "parts": [{"text": text}],
            "messageId": uuid4().hex,
        },
    }
    if task_id:
        payload["message"]["taskId"] = task_id
    if context_id:
        payload["message"]["contextId"] = context_id
    return payload


def print_json_response(response: Any, description: str) -> None:
    print(f"--- {description} ---")
    try:
        if hasattr(response, "model_dump_json"):
            print(response.model_dump_json(exclude_none=True))
        elif hasattr(response, "root") and hasattr(response.root, "model_dump_json"):
            print(response.root.model_dump_json(exclude_none=True))
        elif hasattr(response, "dict"):
            print(response.dict(exclude_none=True))
        else:
            print(str(response))
        print()  # Add a newline after the JSON
    except Exception as e:
        print(f"Error printing response: {e}")
        print(str(response))
        print()


async def run_elevenlabs_tts_test(client: A2AClient) -> None:
    test_query = "Convert 'Hello from the ADK A2A client, this is a test!' to speech."
    print(f"Test Query: {test_query}")

    send_payload = create_send_message_payload(text=test_query)
    request = SendMessageRequest(
        id=str(uuid4()), params=MessageSendParams(**send_payload)
    )

    print()  # Newline for separation
    print("--- Sending Task ---")
    send_response: SendMessageResponse = await client.send_message(request)
    print_json_response(send_response, "Send Task Response")

    if (
        not isinstance(send_response, SendMessageSuccessResponse)
        or not send_response.result
    ):
        print("Received non-success or empty result from send_message. Aborting.")
        return

    # The agent's reply (send_response.result) is a Message-like structure
    # containing the taskId, not an A2A Task object itself.
    agent_reply_data = send_response.result

    extracted_task_id: str | None = None

    # Attempt to get taskId, checking for attribute (Pydantic model) or key (dict)
    if hasattr(agent_reply_data, "taskId"):  # Handles Pydantic models
        task_id_value = getattr(agent_reply_data, "taskId", None)
        if isinstance(task_id_value, str):
            extracted_task_id = task_id_value

    if not extracted_task_id and isinstance(agent_reply_data, dict):  # Handles dicts
        task_id_value = agent_reply_data.get("taskId")
        if isinstance(task_id_value, str):
            extracted_task_id = task_id_value

    if not extracted_task_id:
        print("Could not extract taskId from the agent's reply. Aborting.")
        print_json_response(
            agent_reply_data, "Agent's reply (send_response.result) for debugging"
        )
        return

    task_id: str = extracted_task_id
    print(f"Task ID (from agent reply): {task_id}")
    print()  # Newline for separation
    print("--- Querying Task Status ---")

    max_retries = 10
    retry_delay = 2  # seconds
    task_status = "unknown"  # Initialize task_status

    for attempt in range(max_retries):
        get_request = GetTaskRequest(
            id=str(uuid4()), params=TaskQueryParams(id=task_id)
        )
        get_response: GetTaskResponse = await client.get_task(get_request)
        print_json_response(get_response, f"Get Task Response (Attempt {attempt + 1})")

        if isinstance(get_response, GetTaskSuccessResponse) and get_response.result:
            actual_task_result = get_response.result
            if actual_task_result.status:
                task_status = actual_task_result.status.state
                print(f"Task State: {task_status}")
                if task_status in ["completed", "failed"]:
                    if task_status == "completed" and actual_task_result.artifacts:
                        print()  # Newline for separation
                        print("--- Artifacts ---")
                        for i, artifact_item in enumerate(actual_task_result.artifacts):
                            # Assuming artifact_item is a dict due to custom server structure
                            if isinstance(artifact_item, dict):
                                parts_list = artifact_item.get("parts")
                                if isinstance(parts_list, list):
                                    for j, part_data in enumerate(parts_list):
                                        # Assuming part_data is a dict
                                        if isinstance(part_data, dict):
                                            print(f"  Artifact {i}, Part {j}:")
                                            text = part_data.get("text")
                                            audio_url = part_data.get("audio_url")
                                            if text:
                                                print(f"    Text: {text}")
                                            if audio_url:
                                                print(f"    Audio URL: {audio_url}")
                                        else:
                                            print(
                                                f"  Artifact {i}, Part {j} (unexpected item type): {part_data}"
                                            )
                                else:
                                    print(
                                        f"  Artifact {i} (no 'parts' list or not a list): {artifact_item}"
                                    )
                            else:
                                print(
                                    f"  Artifact {i} (unexpected type, not a dict): {artifact_item}"
                                )

                    elif task_status == "failed" and actual_task_result.status.message:
                        print(
                            f"Task Failed Message: {actual_task_result.status.message}"
                        )
                    break  # Exit loop once task is completed or failed
            else:
                print("GetTaskResponse result did not contain status.")
        else:
            print(
                "GetTaskResponse was not successful or did not contain expected result structure."
            )

        if attempt < max_retries - 1 and task_status not in ["completed", "failed"]:
            print(f"Task not final, retrying in {retry_delay}s...")
            await asyncio.sleep(retry_delay)
        elif task_status in ["completed", "failed"]:
            break  # Already handled and broke from inner if
        else:  # Max retries reached and task not completed/failed
            print("Max retries reached, task did not complete.")
            break


async def main() -> None:
    print(f"Connecting to ElevenLabs Agent at {AGENT_URL}...")
    try:
        async with httpx.AsyncClient(timeout=30.0) as httpx_client:
            client = await A2AClient.get_client_from_agent_card_url(
                httpx_client, AGENT_URL
            )
            print("Connection successful.")
            await run_elevenlabs_tts_test(client)

    except httpx.ConnectError as e:
        print(
            f"Connection error: Could not connect to agent at {AGENT_URL}. Ensure the server is running."
        )
        print(f"Details: {e}")
        traceback.print_exc()
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
