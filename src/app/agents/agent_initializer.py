import os

from azure.ai.agents.models import ToolSet
from azure.ai.projects import AIProjectClient
from dotenv import load_dotenv

load_dotenv()


def initialize_agent(
    project_client: AIProjectClient,
    model: str,
    env_var_name: str,
    name: str,
    instructions: str,
    toolset: ToolSet,
):
    with project_client:
        agent_id = os.getenv(env_var_name)
        if agent_id:
            agent = project_client.agents.get_agent(agent_id)
            agent = project_client.agents.update_agent(
                agent_id,
                model=model,
                name=name,
                instructions=instructions,
                toolset=toolset,
            )
            print(f"Updated {env_var_name} agent, ID: {agent.id}")
        else:
            agent = project_client.agents.create_agent(
                model=model, name=name, instructions=instructions, toolset=toolset
            )
            print(f"Created {env_var_name} agent, ID: {agent.id}")
            print(f"Created {env_var_name} agent, ID: {agent.id}")
