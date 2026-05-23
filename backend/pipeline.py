"""Pipeline — orchestrates fan-out to 5 agents and synthesis."""
import asyncio
import uuid
import time
from backend.agents import unit_test_generator, integration_test_generator, fuzz_test_generator, edge_case_generator, mock_generator, synthesis

# In-memory job store (replace with Redis for production)
jobs: dict[str, dict] = {}


def chunk_source(code: str, max_chars: int = 12000) -> list[str]:
    """Split Solidity source into chunks by contract boundaries."""
    if len(code) <= max_chars:
        return [code]
    chunks = []
    lines = code.split("\n")
    current = []
    current_len = 0
    for line in lines:
        if current_len + len(line) > max_chars and current:
            chunks.append("\n".join(current))
            current = []
            current_len = 0
        current.append(line)
        current_len += len(line) + 1
    if current:
        chunks.append("\n".join(current))
    return chunks


async def run_pipeline(solidity_code: str) -> str:
    """Run the full multi-agent pipeline. Returns job_id."""
    job_id = str(uuid.uuid4())[:8]
    jobs[job_id] = {"status": "running", "started_at": time.time(), "files": {}, "agents": {}}

    try:
        code_chunks = chunk_source(solidity_code)
        combined_code = "\n\n".join(code_chunks)

        # Fan-out to 5 agents in parallel
        agents = [
            ("unit_tests", unit_test_generator),
            ("integration_tests", integration_test_generator),
            ("fuzz_tests", fuzz_test_generator),
            ("edge_case_tests", edge_case_generator),
            ("mocks", mock_generator),
        ]

        jobs[job_id]["status"] = "generating_agents"
        results = await asyncio.gather(
            *(agent.generate(combined_code, job_id) for _, agent in agents),
            return_exceptions=True,
        )

        agent_outputs = {}
        for (name, _), result in zip(agents, results):
            if isinstance(result, Exception):
                agent_outputs[name] = f"// Error in {name}: {result}"
                jobs[job_id]["agents"][name] = f"error: {result}"
            else:
                agent_outputs[name] = result
                jobs[job_id]["agents"][name] = "completed"

        # Synthesis
        jobs[job_id]["status"] = "synthesizing"
        files = await synthesis.generate(combined_code, job_id, agent_outputs)

        jobs[job_id]["status"] = "completed"
        jobs[job_id]["files"] = files
        jobs[job_id]["completed_at"] = time.time()
        jobs[job_id]["elapsed"] = jobs[job_id]["completed_at"] - jobs[job_id]["started_at"]

    except Exception as e:
        jobs[job_id]["status"] = "failed"
        jobs[job_id]["error"] = str(e)

    return job_id
