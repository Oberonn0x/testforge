"""Agent 1: Unit Test Generator — basic tests for every public function."""
from backend.agents.base import call_llm

SYSTEM_PROMPT = """You are an expert Solidity test engineer. Generate comprehensive Foundry unit tests (using forge-std) for every public/external function in the provided Solidity contract(s).

Rules:
- Use `import "forge-std/Test.sol";` style imports
- Name test contract `ContractNameUnitTest`
- Test every public function with at least: happy path, zero input, and expected revert cases
- Use `vm.prank`, `vm.expectRevert`, `deal` as needed
- Emit clear test names: `test_functionName_description`
- Add a `setUp()` that deploys the contract
- Return ONLY valid Solidity code, no markdown fences"""


async def generate(solidity_code: str, job_id: str) -> str:
    user = f"Generate comprehensive unit tests for this Solidity contract(s):\n\n```solidity\n{solidity_code}\n```"
    return await call_llm(SYSTEM_PROMPT, user, job_id, "unit_test_generator")
