import unittest
import sys
import os

# Add the parent directory to the path so we can import src as a package
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.model import Machine, State, Action, Variable
from src.rules import Condition


class TestVariable(unittest.TestCase):
    """Unit tests for the Variable class"""

    def test_variable_creation(self):
        """Test basic variable creation"""
        var = Variable("${TEST_VAR}", ["value1", "value2", "value3"])
        self.assertEqual(var.name, "${TEST_VAR}")
        self.assertEqual(var.values, ["value1", "value2", "value3"])
        # Variable should start with no value set
        with self.assertRaises(AssertionError):
            _ = var.current_value

    def test_variable_set_current_value(self):
        """Test setting current value"""
        var = Variable("${TEST_VAR}", ["value1", "value2"])
        var.set_current_value("value1")
        self.assertEqual(var.current_value, "value1")

    def test_variable_regex_validation(self):
        """Test variable name regex validation"""
        # Valid variable names
        valid_names = ["${VAR}", "${TEST_VAR}", "${VAR_123}", "${VALID_NAME}"]
        for name in valid_names:
            var = Variable(name, ["test"])
            self.assertTrue(var.name.startswith("${"))
            self.assertTrue(var.name.endswith("}"))

    def test_variable_set_machine(self):
        """Test setting machine reference"""
        var = Variable("${TEST_VAR}", ["value1"])
        machine = Machine([], [var], [])
        var.set_machine(machine)
        self.assertEqual(var._machine, machine)


class TestAction(unittest.TestCase):
    """Unit tests for the Action class"""

    def setUp(self):
        self.start_state = State("Start", [], [])
        self.end_state = State("End", [], [])
        
    def test_action_creation(self):
        """Test basic action creation"""
        action = Action("test action", "End")
        self.assertEqual(action.name, "test action")
        self.assertEqual(action._next_state_name, "End")
        self.assertIsNone(action.condition)

    def test_action_with_condition(self):
        """Test action with condition"""
        condition = Condition("${VAR}", "value1")
        action = Action("conditional action", "End", condition)
        self.assertEqual(action.condition, condition)

    def test_action_is_available_no_condition(self):
        """Test action availability when no condition is set"""
        action = Action("test action", "End")
        self.assertTrue(action.is_available())

    def test_action_is_available_with_condition(self):
        """Test action availability with condition"""
        var = Variable("${VAR}", ["value1", "value2"])
        var.set_current_value("value1")
        end_state = State("End", [], [])
        machine = Machine([end_state], [var], [])
        
        condition = Condition("${VAR}", "value1")
        action = Action("conditional action", "End", condition)
        action.set_machine(machine)
        
        self.assertTrue(action.is_available())
        
        var.set_current_value("value2")
        self.assertFalse(action.is_available())


class TestState(unittest.TestCase):
    """Unit tests for the State class"""

    def setUp(self):
        self.start_state = State("Start", ["Print Starting"], [])
        self.end_state = State("End", ["Print Ending"], [])

    def test_state_creation(self):
        """Test basic state creation"""
        state = State("TestState", ["Step 1", "Step 2"], [])
        self.assertEqual(state.name, "TestState")
        self.assertEqual(state.steps, ["Step 1", "Step 2"])
        self.assertEqual(state._actions, [])

    def test_state_with_actions(self):
        """Test state with actions"""
        action1 = Action("action1", "End")
        action2 = Action("action2", "End")
        
        state = State("TestState", [], [action1, action2])
        actions = state._actions  # Test internal actions first
        
        self.assertEqual(len(actions), 2)
        self.assertIn(action1, actions)
        self.assertIn(action2, actions)

    def test_state_actions_filtering(self):
        """Test that only available actions are returned"""
        var = Variable("${VAR}", ["value1", "value2"])
        var.set_current_value("value1")
        end_state = State("End", [], [])
        machine = Machine([end_state], [var], [])
        
        condition1 = Condition("${VAR}", "value1")
        condition2 = Condition("${VAR}", "value2")
        
        action1 = Action("available_action", "End", condition1)
        action2 = Action("unavailable_action", "End", condition2)
        
        action1.set_machine(machine)
        action2.set_machine(machine)
        
        state = State("TestState", [], [action1, action2])
        state.set_machine(machine)  # Set machine for the state
        available_actions = state.actions
        
        self.assertEqual(len(available_actions), 1)
        self.assertEqual(available_actions[0], action1)

    def test_state_actions_no_duplicates(self):
        """Test that duplicate action names are filtered out"""
        action1 = Action("same_name", "End")
        action2 = Action("same_name", "End")
        
        # Create a simple machine for testing
        end_state = State("End", [], [])
        machine = Machine([end_state], [], [])
        
        action1.set_machine(machine)
        action2.set_machine(machine)
        
        state = State("TestState", [], [action1, action2])
        state.set_machine(machine)
        actions = state.actions
        
        self.assertEqual(len(actions), 1)


class TestMachine(unittest.TestCase):
    """Unit tests for the Machine class"""

    def setUp(self):
        self.var1 = Variable("${VAR1}", ["a", "b"])
        self.var2 = Variable("${VAR2}", ["1", "2"])
        self.state1 = State("State1", [], [])
        self.state2 = State("State2", [], [])

    def test_machine_creation(self):
        """Test basic machine creation"""
        machine = Machine([self.state1, self.state2], [self.var1, self.var2], [])
        
        self.assertEqual(len(machine.states), 2)
        self.assertEqual(len(machine.variables), 2)
        self.assertEqual(len(machine.rules), 0)

    def test_machine_start_state(self):
        """Test that start state is the first state"""
        machine = Machine([self.state1, self.state2], [], [])
        self.assertEqual(machine.start_state, self.state1)

    def test_find_state_by_name(self):
        """Test finding state by name"""
        machine = Machine([self.state1, self.state2], [], [])
        
        found_state = machine.find_state_by_name("State1")
        self.assertEqual(found_state, self.state1)
        
        not_found = machine.find_state_by_name("NonExistent")
        self.assertIsNone(not_found)

    def test_find_variable_by_name(self):
        """Test finding variable by name"""
        machine = Machine([], [self.var1, self.var2], [])
        
        found_var = machine.find_variable_by_name("${VAR1}")
        self.assertEqual(found_var, self.var1)
        
        not_found = machine.find_variable_by_name("${NONEXISTENT}")
        self.assertIsNone(not_found)

    def test_variable_value_mapping(self):
        """Test variable value mapping"""
        self.var1.set_current_value("a")
        self.var2.set_current_value("1")
        
        machine = Machine([], [self.var1, self.var2], [])
        mapping = machine.variable_value_mapping
        
        expected = {"${VAR1}": "a", "${VAR2}": "1"}
        self.assertEqual(mapping, expected)

    def test_apply_variable_values(self):
        """Test applying variable values"""
        machine = Machine([], [self.var1, self.var2], [])
        values = ["b", "2"]
        
        machine.apply_variable_values(values)
        
        self.assertEqual(self.var1.current_value, "b")
        self.assertEqual(self.var2.current_value, "2")

    def test_rules_validation(self):
        """Test rules validation"""
        rule = Condition("${VAR1}", "a")
        machine = Machine([], [self.var1, self.var2], [rule])
        
        # Valid values
        self.assertTrue(machine.rules_are_ok(["a", "1"]))
        # Invalid values
        self.assertFalse(machine.rules_are_ok(["b", "1"]))


if __name__ == '__main__':
    unittest.main()
