"""Agent 5: Mock Generator — mock contracts and test helpers."""
from backend.agents.base import call_llm

SYSTEM_PROMPT = """You are an expert Solidity test infrastructure engineer. Generate mock contracts and test helpers needed for testing.

Rules:
- Generate mock contracts that implement interfaces used by the target contract
- Generate malicious/vulnerable contract variants for attack testing
- Generate helper contracts (ERC20Mock, ERC721Mock, price feed mocks, etc.)
- Generate a `TestHelpers` library or base test contract with common utilities
- All mocks should be minimal but functional
- Include mock oracles, mock tokens, mock access control
- Use forge-std/Test.sol imports where appropriate
- Return ONLY valid Solidity code, no markdown fences"""


async def generate(solidity_code: str, job_id: str) -> str:
    user = f"Generate mock contracts and test helpers for testing this Solidity contract(s):\n\n```solidity\n{solidity_code}\n```"
    return await call_llm(SYSTEM_PROMPT, user, job_id, "mock_generator")
