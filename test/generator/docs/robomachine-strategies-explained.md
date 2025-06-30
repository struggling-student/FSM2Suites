# RoboMachine Test Generation Strategies

## Overview

RoboMachine is a test data generator for Robot Framework that uses finite state machine (FSM) models to automatically generate test cases. It supports three different strategies for test generation, each with its own approach to exploring the state space and generating test paths.

This document explains how each of the three strategies works: **Depth First Search (DFS)**, **Random**, and **AllPairs-Random**.

## Strategy Architecture

All strategies inherit from the base `_Strategy` class which provides:
- Machine reference (`_machine`): The state machine model
- Maximum actions (`_max_actions`): Limit on test case length  
- Target state (`_to_state`): Optional end state for generated tests

Each strategy implements a `tests()` generator method that yields tuples of `(test_actions, variable_values)`.

---

## 1. Depth First Search Strategy (DFS)

**Class:** `DepthFirstSearchStrategy`

### Algorithm Overview

The DFS strategy systematically explores all possible paths through the state machine using a depth-first traversal approach. It aims for **complete coverage** by exhaustively generating all valid test sequences.

### How It Works

1. **Variable Value Generation:**
   - Generates all possible combinations of variable values
   - Uses Cartesian product of all variable value sets
   - Filters combinations using machine rules (`rules_are_ok()`)

2. **Path Generation:**
   - For each variable combination, explores all paths from the start state
   - Uses recursive depth-first traversal (`_generate_all_from()`)
   - Generates paths up to the maximum action limit
   - Ensures paths end in the target state (if specified)

3. **Recursive Exploration:**
   ```python
   def _generate_all_from(self, state, max_actions):
       if not state.actions or max_actions == 0:
           yield []  # Base case: empty path
       else:
           for action in state.actions:
               for test in self._generate_all_from(action.next_state, max_actions-1):
                   yield [action] + test  # Recursive path building
   ```

### Characteristics

- **Coverage:** Highest - attempts to cover all possible paths
- **Deterministic:** Yes - always generates the same tests in the same order
- **Performance:** Can be slow for large state spaces due to exponential growth
- **Use Case:** When you need comprehensive testing and state space is manageable

### Example

For a simple Login → Browsing → CartEditing state machine:
```
Test 1: [login_valid] 
Test 2: [login_valid, add_to_cart]
Test 3: [login_valid, add_to_cart, checkout]
Test 4: [login_invalid]
Test 5: [login_invalid, retry_login, login_valid]
... (all possible combinations)
```

---

## 2. Random Strategy

**Class:** `RandomStrategy`

### Algorithm Overview

The Random strategy generates test paths by making random choices at each state transition. It provides a **probabilistic approach** to test generation that can quickly generate diverse test cases.

### How It Works

1. **Variable Value Generation:**
   ```python
   def _generate_variable_values(self):
       while True:
           candidate = [random.choice(v.values) for v in self._machine.variables]
           if self._machine.rules_are_ok(candidate):
               return candidate
   ```
   - Randomly selects values for each variable
   - Retries until rule constraints are satisfied

2. **Path Generation:**
   ```python
   def _generate_test(self, values):
       test = []
       current_state = self._machine.start_state
       while self._max_actions > len(test) and current_state.actions:
           action = random.choice(current_state.actions)  # Random choice
           current_state = action.next_state
           test.append(action)
       # Trim path to match target state if needed
       while test and not self._matching_to_state(test):
           test.pop()
       return test
   ```

3. **Path Trimming:**
   - If a target state is specified, trims the path from the end until it reaches the target state
   - May result in shorter tests than the maximum length

### Characteristics

- **Coverage:** Variable - depends on random choices and number of tests generated
- **Deterministic:** No - different results on each run (unless seeded)
- **Performance:** Fast - constant time per test generation
- **Use Case:** When you need quick test generation or want to explore edge cases through randomness

### Example

For the same state machine, might generate:
```
Test 1: [login_invalid, retry_login, login_valid, add_to_cart]
Test 2: [login_valid]
Test 3: [login_valid, add_to_cart, checkout, payment_success]
Test 4: [login_invalid]
... (random combinations)
```

---

## 3. AllPairs-Random Strategy

**Class:** `AllPairsRandomStrategy`

### Algorithm Overview

The AllPairs-Random strategy combines **pairwise testing** (all-pairs) for variable combinations with **random path generation**. It ensures that all pairs of variable values are tested while using random exploration for state transitions.

### How It Works

1. **Variable Value Generation:**
   ```python
   def _generate_all_pairs_variable_values(self):
       if len(list(self._machine.variables)) < 2:
           # Handle edge cases for 0 or 1 variables
           return [v for v in var.values] or [[]]
       return AllPairs([v.values for v in self._machine.variables])
   ```
   - Uses the AllPairs algorithm to generate minimal set of test cases covering all variable pairs
   - Much more efficient than full Cartesian product for systems with many variables

2. **Path Generation:**
   - Inherits the random path generation from `RandomStrategy`
   - For each AllPairs variable combination, generates a random test path

3. **Pairwise Coverage:**
   - Ensures every pair of variable values appears in at least one test
   - Significantly reduces the number of required tests compared to full combinatorial coverage

### Characteristics

- **Coverage:** Optimal for variable combinations, random for paths
- **Deterministic:** Partially - AllPairs combinations are deterministic, paths are random
- **Performance:** Very efficient for systems with many variables
- **Use Case:** When you have many variables and want efficient combinatorial coverage
- **Limitation:** Does not work with rule constraints (`rules_are_ok()`)

### Example

For variables `${EMAIL}` (2 values) and `${PASSWORD}` (2 values) and `${PAYMENT}` (2 values):

Instead of 2×2×2 = 8 full combinations, AllPairs might generate only 4 combinations that cover all pairs:
```
Test 1: [EMAIL=valid, PASSWORD=valid, PAYMENT=success] + random_path
Test 2: [EMAIL=valid, PASSWORD=invalid, PAYMENT=failure] + random_path  
Test 3: [EMAIL=invalid, PASSWORD=valid, PAYMENT=failure] + random_path
Test 4: [EMAIL=invalid, PASSWORD=invalid, PAYMENT=success] + random_path
```

---

## Strategy Comparison

| Aspect | DFS | Random | AllPairs-Random |
|--------|-----|--------|-----------------|
| **Path Coverage** | Complete | Variable | Variable |
| **Variable Coverage** | Complete | Variable | Pairwise Complete |
| **Performance** | Slow (exponential) | Fast | Fast |
| **Deterministic** | Yes | No | Partially |
| **Memory Usage** | High | Low | Low |
| **Rules Support** | Yes | Yes | No |
| **Best For** | Small models, complete coverage | Quick testing, large models | Many variables, efficient coverage |

## Choosing the Right Strategy

### Use **DFS** when:
- You need complete test coverage
- The state machine is relatively small
- You want deterministic, reproducible test suites
- Testing time is not a constraint

### Use **Random** when:
- You need fast test generation
- The state space is large
- You want to find unexpected edge cases
- You're doing exploratory testing

### Use **AllPairs-Random** when:
- You have many variables (3+ with multiple values each)
- You want efficient combinatorial coverage
- You don't have complex rule constraints
- You need a balance between coverage and performance

## Implementation Notes

### Variable Rules
Both DFS and Random strategies support machine rules that constrain valid variable combinations. The AllPairs strategy explicitly rejects rule usage due to complexity in the AllPairs algorithm.

### Target State Handling
All strategies support specifying a target end state (`--to-state` parameter). They handle this by:
- **DFS:** Only generates paths that naturally end in the target state
- **Random:** Trims generated paths from the end until they reach the target state
- **AllPairs-Random:** Same as Random (inherits the behavior)

### Memory and Performance Considerations
- **DFS** can consume significant memory for large state spaces due to recursive path generation
- **Random** and **AllPairs-Random** are memory-efficient as they generate tests one at a time
- The `max_tests` parameter limits total test generation to prevent infinite generation

This comprehensive approach allows RoboMachine users to choose the most appropriate strategy based on their specific testing needs, model complexity, and performance requirements.
