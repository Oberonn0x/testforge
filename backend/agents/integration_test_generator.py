"""Agent 2: Integration Test Generator — cross-contract interaction tests."""
from backend.agents.base import call_llm

SYSTEM_PROMPT = """You are an expert Solidity test engineer specializing in integration tests. Generate Foundry tests that verify cross-contract interactions, multi-step workflows, and stateful sequences.

Rules:
- Use forge-std/Test.sol imports
- Name test contract `ContractNameIntegrationTest`
- Test interactions between multiple contracts or multi-step user flows
- Test role-based access patterns, approval flows, callback patterns
- Use `vm.startPrank`/`vm.stopPrank`, `vm.recordLogs`, snapshot/restore
- Test realistic user journeys: deploy → configure → use → upgrade
- Return ONLY valid Solidity code, no markdown fences"""


async def generate(solidity_code: str, job_id: str) -> str:
    user = f"Generate integration tests for this Solidity contract(s):\n\n```solidity\n{solidity_code}\n```"
    return await call_llm(SYSTEM_PROMPT, user, job_id, "integration_test_generator")
