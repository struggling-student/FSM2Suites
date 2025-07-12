# Machine Generator Test Suite

This directory contains comprehensive unit and integration tests for the machine generator system. The test suite validates all core components including parsing, model classes, generation strategies, and end-to-end workflows.

## Test Overview

The test suite consists of **82 tests** organized into 6 main test files:

- **Unit Tests**: 73 tests covering individual components
- **Integration Tests**: 9 tests covering complete workflows
- **Coverage**: Tests validate core functionality, edge cases, and error conditions

## Test Structure

### Unit Tests

#### 1. Model Tests (`test_model.py`) - 19 tests
Tests the core data model classes: `Variable`, `State`, `Action`, and `Machine`.

**Example Tests:**
```python
def test_variable_creation(self):
    """Test basic variable creation"""
    var = Variable("${TEST_VAR}", ["value1", "value2"])
    self.assertEqual(var.name, "${TEST_VAR}")
    self.assertEqual(var.values, ["value1", "value2"])

def test_machine_start_state(self):
    """Test that start state is the first state"""
    machine = Machine([self.start_state, self.end_state], [], [])
    self.assertEqual(machine.start_state, self.start_state)
```

#### 2. Rules Tests (`test_rules.py`) - 18 tests
Tests condition evaluation and composite rule logic including AND, OR, NOT, and implication rules.

**Example Tests:**
```python
def test_condition_equal(self):
    """Test basic equality condition"""
    condition = Condition("${VAR}", "test_value")
    value_mapping = {"${VAR}": "test_value"}
    self.assertTrue(condition.is_valid(value_mapping))

def test_implication_rule(self):
    """Test implication rule"""
    antecedent = Condition("${A}", "true")
    consequent = Condition("${B}", "true")
    rule = ImplicationRule(antecedent, consequent)
    # Test: true => true = true
    self.assertTrue(rule.is_valid({"${A}": "true", "${B}": "true"}))
```

#### 3. Strategies Tests (`test_strategies.py`) - 15 tests
Tests test generation strategies including depth-first search and random generation.

**Example Tests:**
```python
def test_generate_tests_simple(self):
    """Test test generation for simple machine"""
    strategy = DepthFirstSearchStrategy(self.machine, -1, None)
    tests = list(strategy.tests())
    self.assertGreater(len(tests), 0)
    # Each test should be a tuple of (actions, variable_values)
    for test, values in tests:
        self.assertIsInstance(test, list)
        self.assertIsInstance(values, list)
```

#### 4. Parsing Tests (`test_parsing.py`) - 10 tests
Tests machine definition parsing from Robot Framework-style text format.

**Example Tests:**
```python
def test_parse_machine_with_rules(self):
    """Test parsing machine with rules"""
    machine_text = """*** Machine ***
${VAR1}  any of  a  b
${VAR2}  any of  1  2

${VAR1} == a  ==>  ${VAR2} == 1

Start
  [Actions]
    action1  ==>  End
"""
    machine = parse(machine_text)
    self.assertEqual(len(machine.rules), 1)
    self.assertTrue(machine.rules_are_ok(["a", "1"]))  # Valid combination
    self.assertFalse(machine.rules_are_ok(["a", "2"]))  # Invalid
```

#### 5. Generator Tests (`test_generator.py`) - 11 tests
Tests the main Generator class functionality including test generation, coverage tracking, and output formatting.

**Example Tests:**
```python
def test_coverage_tracking(self):
    """Test that coverage tracking works correctly"""
    generator = Generator()
    # Get all actions for coverage tracking
    all_actions = set()
    for state in self.machine.states:
        all_actions.update(state.actions)
    
    generator.generate(
        self.machine,
        max_tests=10,
        all_actions=all_actions,
        output=output
    )
    
    # Check that states and actions were tracked
    self.assertGreater(len(generator.visited_states), 0)
    self.assertIn("Covered states", result)
```

### Integration Tests

#### 6. Integration Tests (`test_integration.py`) - 9 tests
Tests complete end-to-end workflows from parsing machine definitions to generating Robot Framework test files.

**Example Tests:**
```python
def test_parse_and_generate_simple_machine(self):
    """Test complete workflow: parse and generate from simple machine"""
    machine_text = """*** Machine ***
${STATUS}  any of  success  failure

Start
  [Actions]
    proceed  ==>  Success  when  ${STATUS} == success
    proceed  ==>  Failure  when  ${STATUS} == failure
"""
    
    machine = parse(machine_text)
    generator = Generator()
    generator.generate(machine, output=output)
    
    generated_content = output.getvalue()
    self.assertIn("*** Test Cases ***", generated_content)
    self.assertIn("Test 1", generated_content)
```

## Running Tests

The test suite uses an invoke-based task system for easy test execution:

### Run All Tests
```bash
invoke test
```

### Run Specific Test Categories
```bash
# Run all unit tests
invoke test-unit

# Run integration tests only
invoke test-integration

# Run individual test modules
invoke test-model
invoke test-rules
invoke test-strategies
invoke test-parsing
invoke test-generator
```

## Test Features

### Comprehensive Coverage
- **Model Classes**: Variable, State, Action, Machine creation and behavior
- **Rule Engine**: All condition types and composite rules
- **Parsing**: Machine definition parsing with various formats
- **Generation**: Test generation with different strategies
- **Integration**: Complete workflows from parsing to output

### Edge Case Testing
- Empty machines and states
- Invalid state references
- Complex conditional logic
- Variable resolution and validation
- Error handling and boundary conditions

### Performance Testing
- Large machine definitions (20+ tests generated)
- Complex rule combinations
- Memory and execution time validation

## Test Data Examples

### Simple Machine Definition
```robot
*** Machine ***
${STATUS}  any of  success  failure

Start
  [Actions]
    proceed  ==>  Success  when  ${STATUS} == success
    proceed  ==>  Failure  when  ${STATUS} == failure

Success
Failure
```

### Complex Machine with Rules
```robot
*** Machine ***
${USER_TYPE}  any of  admin  user  guest
${ACTION}     any of  read  write  delete

${USER_TYPE} == admin  ==>  ${ACTION} in (read, write, delete)
${USER_TYPE} == user   ==>  ${ACTION} in (read, write)

Login
  [Actions]
    authenticate  ==>  Authenticated  when  ${USER_TYPE} != guest
    authenticate  ==>  GuestMode      when  ${USER_TYPE} == guest
```

## Expected Output Example

When tests generate Robot Framework files, the output includes:

```robot
*** Test Cases ***
Test 1
  Set Machine Variables  success
  Start
  proceed
  Success

Test 2
  Set Machine Variables  failure
  Start
  proceed
  Failure

*** Keywords ***
Set Machine Variables
  [Arguments]  ${STATUS}
  Set Test Variable  \${STATUS}

Start
  Log    Starting test

Success
  Log    Operation successful
```

## Test Results

Current test suite status:
- **82 total tests**
- **81 passing tests** (98.8% success rate)
- **1 skipped test** (due to known limitation with infinite state loops)
- **0 failing tests**

The test suite provides comprehensive validation ensuring code quality and preventing regressions in the machine generator system.
