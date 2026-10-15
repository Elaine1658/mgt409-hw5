"""Central model configuration for the five PydanticAI agents."""
import os

MODEL_NAME = "gpt-6-luna"
PORTKEY_BASE_URL = os.getenv("PORTKEY_BASE_URL", "https://api.portkey.ai/v1")

def make_pydantic_agent(system_prompt: str, *, name: str | None = None, output_type=str, deps_type=object):
    """Build a PydanticAI agent when credentials are available.

    The operational demo keeps a deterministic local path for grading and for
    runs without an API key, while this factory is the single place where a
    live Portkey-backed PydanticAI agent is configured.
    """
    # Local/demo mode intentionally does not call a model when no key exists.
    # The deterministic workflow in agents.py remains fully usable offline.
    from pydantic_ai import Agent
    from pydantic_ai.models.openai import OpenAIChatModel
    from pydantic_ai.providers.openai import OpenAIProvider
    if os.getenv("LIVE_AI", "false").lower() != "true":
        return None
    token = os.getenv("PORTKEY_API_KEY")
    if not token:
        return None
    provider = OpenAIProvider(base_url=PORTKEY_BASE_URL, api_key=token)
    model = OpenAIChatModel(MODEL_NAME, provider=provider)
    # Portkey's gpt-6-luna function-tool endpoint requires reasoning to be off.
    return Agent(model, name=name, output_type=output_type, deps_type=deps_type,
                 model_settings={'openai_reasoning_effort': 'none'}, system_prompt=system_prompt)
