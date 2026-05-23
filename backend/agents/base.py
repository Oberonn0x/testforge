"""Shared base LLM caller with retry and token tracking."""
import os
import asyncio
from openai import AsyncOpenAI
from backend.token_tracker import record_usage

_client: AsyncOpenAI | None = None


def get_client() -> AsyncOpenAI:
    global _client
    if _client is None:
        _client = AsyncOpenAI(
            api_key=os.getenv("OPENAI_API_KEY", ""),
            base_url=os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1"),
        )
    return _client


async def call_llm(system_prompt: str, user_prompt: str, job_id: str, agent_name: str, max_retries: int = 3) -> str:
    """Call LLM with retry logic and automatic token tracking."""
    client = get_client()
    model = os.getenv("OPENAI_MODEL", "gpt-4o")
    last_err = None
    for attempt in range(max_retries):
        try:
            resp = await client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=0.2,
                max_tokens=16000,
            )
            usage = resp.usage
            if usage:
                await record_usage(
                    agent=agent_name,
                    job_id=job_id,
                    prompt_tokens=usage.prompt_tokens,
                    completion_tokens=usage.completion_tokens,
                    model=model,
                )
            return resp.choices[0].message.content or ""
        except Exception as e:
            last_err = e
            if attempt < max_retries - 1:
                await asyncio.sleep(2 ** attempt)
    raise RuntimeError(f"LLM call failed after {max_retries} retries: {last_err}")
