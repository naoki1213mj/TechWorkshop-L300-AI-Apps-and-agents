import os
import sys

sys.path.append(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)
from agent_initializer import initialize_agent
from agent_processor import create_function_tool_for_agent
from azure.ai.agents.models import ToolSet
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv

load_dotenv()

INV_PROMPT_TARGET = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    "prompts",
    "InventoryAgentPrompt.txt",
)
with open(INV_PROMPT_TARGET, "r", encoding="utf-8") as file:
    INV_PROMPT = file.read()

project_endpoint = os.environ["AZURE_AI_AGENT_ENDPOINT"]

project_client = AIProjectClient(
    endpoint=project_endpoint,
    credential=DefaultAzureCredential(),
)

# Define the set of user-defined callable functions to use as tools (from MCP client)
functions = create_function_tool_for_agent("inventory")
toolset = ToolSet()
toolset.add(functions)
project_client.agents.enable_auto_function_calls(tools=functions)

initialize_agent(
    project_client=project_client,
    model=os.environ["AZURE_AI_AGENT_MODEL_DEPLOYMENT_NAME"],
    env_var_name="inventory_agent",
    name="Zava Inventory Agent",
    instructions=INV_PROMPT,
    toolset=toolset,
)
