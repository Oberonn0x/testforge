"""Synthesis Agent — merges all agent outputs into a unified test suite."""
import json
from backend.agents.base import call_llm

SYSTEM_PROMPT = """You are an expert Solidity test suite architect. You receive outputs from 5 specialized test generators and must merge them into a clean, complete, non-duplicative Foundry test suite.

Rules:
- Remove duplicate tests (same logic, different names)
- Ensure all necessary imports are present and correct
- Fix any compilation issues you can spot (missing semicolons, wrong syntax)
- Organize into logical files:
  - `test/Unit.t.sol` — unit tests
  - `test/Integration.t.sol` — integration tests  
  - `test/Fuzz.t.sol` — fuzz tests
  - `test/EdgeCase.t.sol` — edge case tests
  - `test/mocks/Mocks.sol` — all mock contracts
  - `test/helpers/TestHelpers.sol` — shared helpers
- Return a JSON object with keys being file paths and values being file contents
- Return ONLY valid JSON, no markdown fences
- Format: {"test/Unit.t.sol": "// SPDX-License...", "test/Integration.t.sol": "...", ...}"""


async def generate(solidity_code: str, job_id: str, agent_outputs: dict[str, str]) -> dict[str, str]:
    combined = "\n\n---SEPARATOR---\n\n".join(
        f"=== {name} ===\n{output}" for name, output in agent_outputs.items()
    )
    user = f"Original Solidity code:\n```solidity\n{solidity_code}\n```\n\nAgent outputs:\n{combined}\n\nMerge into a unified test suite. Return JSON."
    result = await call_llm(SYSTEM_PROMPT, user, job_id, "synthesis")
    # Strip markdown fences if present
    result = result.strip()
    if result.startswith("```"):
        result = result.split("\n", 1)[1]
        if result.endswith("```"):
            result = result[:-3]
    return json.loads(result)
