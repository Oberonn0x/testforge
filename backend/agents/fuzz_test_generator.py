"""Agent 3: Fuzz Test Generator — property-based fuzz tests for Foundry."""
from backend.agents.base import call_llm

SYSTEM_PROMPT = """You are an expert Solidity fuzz testing engineer. Generate Foundry property-based fuzz tests.

Rules:
- Use forge-std/Test.sol imports
- Name test contract `ContractNameFuzzTest`
- Use Foundry's built-in fuzzer: function parameters are automatically fuzzed
- Test invariants: total supply conservation, balance accounting, access control invariants
- Test properties that must ALWAYS hold regardless of input
- Use `vm.assume()` to constrain inputs where needed
- Use `targetContract()` and `targetSelector()` for stateful fuzzing where appropriate
- Test overflow/underflow behavior, rounding, division by zero protection
- Return ONLY valid Solidity code, no markdown fences"""


async def generate(solidity_code: str, job_id: str) -> str:
    user = f"Generate fuzz tests for this Solidity contract(s):\n\n```solidity\n{solidity_code}\n```"
    return await call_llm(SYSTEM_PROMPT, user, job_id, "fuzz_test_generator")
