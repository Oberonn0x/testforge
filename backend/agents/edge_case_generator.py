"""Agent 4: Edge Case Generator — boundary conditions and attack vectors."""
from backend.agents.base import call_llm

SYSTEM_PROMPT = """You are an expert Solidity security engineer. Generate Foundry tests covering edge cases and potential attack vectors.

Rules:
- Use forge-std/Test.sol imports
- Name test contract `ContractNameEdgeCaseTest`
- Test boundary values: 0, 1, type(uint256).max, type(uint256).max - 1
- Test reentrancy scenarios using a malicious receiver contract
- Test front-running resistance, sandwich attack scenarios
- Test empty inputs, empty arrays, single-element arrays
- Test self-calls, calls from the contract to itself
- Test with multiple users interacting simultaneously
- Test paused/unpaused state transitions
- Return ONLY valid Solidity code, no markdown fences"""


async def generate(solidity_code: str, job_id: str) -> str:
    user = f"Generate edge-case tests for this Solidity contract(s):\n\n```solidity\n{solidity_code}\n```"
    return await call_llm(SYSTEM_PROMPT, user, job_id, "edge_case_generator")
