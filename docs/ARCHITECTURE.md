# Architecture

## Overview

TestForge is a multi-agent system for automated Solidity test generation. It uses a fan-out/fan-in pipeline pattern where 5 specialized AI agents analyze Solidity source code in parallel, then a synthesis agent merges their outputs into a unified, deduplicated test suite.

## Agents

### 1. Unit Test Generator
Generates basic unit tests covering every public/external function. Includes happy path, zero-value inputs, and expected revert cases.

### 2. Integration Test Generator
Creates cross-contract interaction tests, multi-step workflows, and role-based access pattern tests.

### 3. Fuzz Test Generator
Produces Foundry property-based fuzz tests with invariant checking, automatic parameter fuzzing, and stateful fuzzing where appropriate.

### 4. Edge Case Generator
Targets boundary conditions: zero values, max uint256, reentrancy attacks, front-running scenarios, and state transition edge cases.

### 5. Mock Generator
Creates mock contracts implementing required interfaces, malicious contract variants for attack testing, and shared test helpers.

### 6. Synthesis Agent
Receives all 5 agent outputs and merges them into a clean Foundry test suite. Removes duplicates, fixes compilation issues, organizes into logical files.

## Pipeline Flow

```
1. User submits Solidity source code
2. Code is chunked if necessary (12K char limit per chunk)
3. Chunks are sent to all 5 agents in parallel (asyncio.gather)
4. Each agent independently generates its test artifacts
5. All outputs are passed to the synthesis agent
6. Synthesis returns a JSON dict of {filepath: content}
7. Results are stored in-memory and returned to the user
```

## Token Tracking

Every LLM call records: agent name, job ID, prompt tokens, completion tokens, model name, and timestamp. All data is persisted in SQLite and queryable via `/api/stats`.

## Technology Stack

- **Backend**: Python 3.12, FastAPI, AsyncOpenAI
- **Database**: SQLite (via aiosqlite)
- **Frontend**: Vanilla HTML/CSS/JS
- **Containerization**: Docker, Docker Compose
