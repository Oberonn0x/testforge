# Example Run

## Input

A simple ERC20-like counter contract:

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

contract Counter {
    uint256 public count;
    address public owner;
    
    event Incremented(address indexed by, uint256 newCount);
    event Decremented(address indexed by, uint256 newCount);
    
    constructor() {
        owner = msg.sender;
    }
    
    modifier onlyOwner() {
        require(msg.sender == owner, "Not owner");
        _;
    }
    
    function increment() external {
        count++;
        emit Incremented(msg.sender, count);
    }
    
    function decrement() external {
        require(count > 0, "Cannot go below zero");
        count--;
        emit Decremented(msg.sender, count);
    }
    
    function reset() external onlyOwner {
        count = 0;
    }
}
```

## API Call

```bash
curl -X POST http://localhost:8000/api/generate \
  -H "Content-Type: application/json" \
  -d '{"solidity_code": "<contract code above>"}'
```

## Response

```json
{
  "job_id": "a1b2c3d4",
  "status": "accepted"
}
```

## Polling

```bash
curl http://localhost:8000/api/generate/a1b2c3d4
```

## Output

The system generates 6 test files:

- `test/Unit.t.sol` — Tests for `increment()`, `decrement()`, `reset()` including revert cases
- `test/Integration.t.sol` — Multi-user interaction sequences
- `test/Fuzz.t.sol` — Property: count never underflows, ownership invariant
- `test/EdgeCase.t.sol` — Reset by non-owner, decrement at zero, max operations
- `test/mocks/Mocks.sol` — Malicious reentrancy contract
- `test/helpers/TestHelpers.sol` — Shared setup utilities

## Token Usage

```bash
curl http://localhost:8000/api/stats
```

```json
{
  "agents": [
    {"agent": "unit_test_generator", "calls": 1, "total": 3200},
    {"agent": "synthesis", "calls": 1, "total": 4100}
  ],
  "grand_total_tokens": 22500,
  "total_api_calls": 6
}
```
