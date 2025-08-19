from rainflower_ticket_agent.agent import root_agent
import vertexai
from vertexai.preview.reasoning_engines import AdkApp
from vertexai import agent_engines
from dotenv import load_dotenv, set_key
import os

load_dotenv()

vertexai.init(
    project = os.getenv("GOOGLE_CLOUD_PROJECT"),
    location = os.getenv("GOOGLE_CLOUD_LOCATION"),
    staging_bucket = "gs://" + os.getenv("GOOGLE_CLOUD_STORAGE_BUCKET"),
)

print("Vertex AI initialized")

def update_env_file(agent_engine_id, env_file_path):
    """Updates the .env file with the agent engine ID."""
    try:
        set_key(env_file_path, "AGENT_ENGINE_ID", agent_engine_id)
        print(f"Updated AGENT_ENGINE_ID in {env_file_path} to {agent_engine_id}")
    except Exception as e:
        print(f"Error updating .env file: {e}")

app = AdkApp(
    agent=root_agent,
    enable_tracing=True,
)

remote_app = agent_engines.create(
    app,
    display_name="rainflower_ticket_agent",
    requirements = [
        "google-cloud-aiplatform[adk,agent-engines]>=1.100.0,<2.0.0",
        "google-adk>=1.5.0,<2.0.0",
        "python-dotenv",
        "google-generativeai",
        "deprecated",
        "requests",
    ]
)

update_env_file(remote_app.resource_name, ENV_FILE_PATH)