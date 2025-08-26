import unittest
import sys
import os

# Add the parent directory to the path so we can import src as a package
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.parsing import parse
from src.core import Machine
from src.core import Condition


class TestParsing(unittest.TestCase):
    """Unit tests for the parsing functionality"""

    def test_parse_simple_machine(self):
        """Test parsing a simple machine definition"""
        machine_text = """*** Machine ***
${VAR}  any of  value1  value2

Start
  [Actions]
    action1  ==>  End

End
"""
        machine = parse(machine_text)
        
        self.assertIsInstance(machine, Machine)
        self.assertEqual(len(machine.states), 2)
        self.assertEqual(len(machine.variables), 1)
        
        # Check variable
        var = machine.variables[0]
        self.assertEqual(var.name, "${VAR}")
        self.assertEqual(var.values, ["value1", "value2"])
        
        # Check states
        start_state = machine.find_state_by_name("Start")
        end_state = machine.find_state_by_name("End")
        self.assertIsNotNone(start_state)
        self.assertIsNotNone(end_state)

    def test_parse_machine_with_conditions(self):
        """Test parsing machine with conditional actions"""
        machine_text = """*** Machine ***
${STATUS}  any of  success  failure

Start
  [Actions]
    proceed  ==>  Success  when  ${STATUS} == success
    proceed  ==>  Failure  when  ${STATUS} == failure

Success

Failure
"""
        machine = parse(machine_text)
        
        self.assertEqual(len(machine.states), 3)
        self.assertEqual(len(machine.variables), 1)
        
        start_state = machine.find_state_by_name("Start")
        self.assertEqual(len(start_state._actions), 2)
        
        # Check conditions
        for action in start_state._actions:
            self.assertIsNotNone(action.condition)
            self.assertIsInstance(action.condition, Condition)

    def test_parse_machine_with_rules(self):
        """Test parsing machine with rules"""
        machine_text = """*** Machine ***
${VAR1}  any of  a  b
${VAR2}  any of  1  2

${VAR1} == a  ==>  ${VAR2} == 1

Start
  [Actions]
    action1  ==>  End

End
"""
        machine = parse(machine_text)
        
        self.assertEqual(len(machine.rules), 1)
        
        # Test rule validation
        self.assertTrue(machine.rules_are_ok(["a", "1"]))  # Valid combination
        self.assertTrue(machine.rules_are_ok(["b", "1"]))  # Valid (antecedent false)
        self.assertTrue(machine.rules_are_ok(["b", "2"]))  # Valid (antecedent false)
        self.assertFalse(machine.rules_are_ok(["a", "2"]))  # Invalid (antecedent true, consequent false)

    def test_parse_machine_with_settings(self):
        """Test parsing machine with settings table"""
        machine_text = """*** Settings ***
Library    TestLibrary
Test Setup    Setup Test

*** Machine ***
${VAR}  any of  value1

Start
  [Actions]
    action1  ==>  End

End
"""
        machine = parse(machine_text)
        
        self.assertIsInstance(machine, Machine)
        # Settings should be preserved in the machine
        self.assertTrue(len(machine._settings_table) > 0)

    def test_parse_machine_with_variables_table(self):
        """Test parsing machine with variables table"""
        machine_text = """*** Variables ***
${GLOBAL_VAR}    global_value

*** Machine ***
${VAR}  any of  value1

Start
  [Actions]
    action1  ==>  End

End
"""
        machine = parse(machine_text)
        
        self.assertIsInstance(machine, Machine)
        # Variables table should be preserved
        self.assertTrue(len(machine._variables_table) > 0)

    def test_parse_machine_with_keywords(self):
        """Test parsing machine with keywords table"""
        machine_text = """*** Machine ***
${VAR}  any of  value1

Start
  [Actions]
    action1  ==>  End

End

*** Keywords ***
Test Keyword
    Log    Test keyword executed
"""
        machine = parse(machine_text)
        
        self.assertIsInstance(machine, Machine)
        # Keywords should be preserved
        self.assertTrue(len(machine._keywords_table) > 0)

    def test_parse_state_with_steps(self):
        """Test parsing state with steps"""
        machine_text = """*** Machine ***
Start
    Log    Starting test
    Set Variable    ${test_var}    test_value
  [Actions]
    action1  ==>  End

End
    Log    Test completed
"""
        machine = parse(machine_text)
        
        start_state = machine.find_state_by_name("Start")
        end_state = machine.find_state_by_name("End")
        
        self.assertTrue(len(start_state.steps) > 0)
        self.assertTrue(len(end_state.steps) > 0)

    def test_parse_complex_conditions(self):
        """Test parsing complex condition expressions"""
        machine_text = """*** Machine ***
${VAR1}  any of  a  b
${VAR2}  any of  1  2  3

Start
  [Actions]
    action1  ==>  End  when  ${VAR1} == a  and  ${VAR2} > 1
    action2  ==>  End  when  ${VAR1} != a  or  ${VAR2} <= 2

End
"""
        machine = parse(machine_text)
        
        start_state = machine.find_state_by_name("Start")
        self.assertEqual(len(start_state._actions), 2)
        
        # Both actions should have conditions
        for action in start_state._actions:
            self.assertIsNotNone(action.condition)

    def test_parse_multiple_variable_values(self):
        """Test parsing variables with multiple values"""
        machine_text = """*** Machine ***
${VAR}  any of  value1  value2  value3  value4  value5

Start
  [Actions]
    action1  ==>  End

End
"""
        machine = parse(machine_text)
        
        var = machine.variables[0]
        expected_values = ["value1", "value2", "value3", "value4", "value5"]
        self.assertEqual(var.values, expected_values)

    def test_parse_otherwise_condition(self):
        """Test parsing 'otherwise' condition"""
        machine_text = """*** Machine ***
${STATUS}  any of  success  failure

Start
  [Actions]
    proceed  ==>  Success  when  ${STATUS} == success
    proceed  ==>  Failure  otherwise

Success

Failure
"""
        machine = parse(machine_text)
        
        start_state = machine.find_state_by_name("Start")
        actions = start_state._actions
        
        # Should have two actions
        self.assertEqual(len(actions), 2)
        
        # First action should have condition, second should be otherwise (no condition or True condition)
        conditional_actions = [a for a in actions if a.condition is not None]
        self.assertGreaterEqual(len(conditional_actions), 1)


if __name__ == '__main__':
    unittest.main()
