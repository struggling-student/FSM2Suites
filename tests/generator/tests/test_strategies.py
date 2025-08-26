import unittest
import sys
import os

# Add the parent directory to the path so we can import src as a package
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.model import Machine, State, Action, Variable
from src.rules import Condition
from src.strategies import DepthFirstSearchStrategy, RandomStrategy


class TestDepthFirstSearchStrategy(unittest.TestCase):
    """Unit tests for the DepthFirstSearchStrategy"""

    def setUp(self):
        """Set up a simple test machine"""
        # Create states
        self.start_state = State("Start", ["Print Starting"], [])
        self.middle_state = State("Middle", ["Print Middle"], [])
        self.end_state = State("End", ["Print End"], [])
        
        # Create variables
        self.var1 = Variable("${VAR1}", ["a", "b"])
        self.var2 = Variable("${VAR2}", ["1", "2"])
        
        # Create actions with state names (not state objects)
        self.action1 = Action("go_to_middle", "Middle")
        self.action2 = Action("go_to_end", "End")
        self.action3 = Action("finish", "End")
        
        # Add actions to states
        self.start_state._actions = [self.action1, self.action2]
        self.middle_state._actions = [self.action3]
        self.end_state._actions = []
        
        # Create machine
        self.machine = Machine(
            [self.start_state, self.middle_state, self.end_state],
            [self.var1, self.var2],
            []
        )
        # Validate the machine to set up relationships
        self.machine.validate()

    def test_strategy_initialization(self):
        """Test strategy initialization"""
        strategy = DepthFirstSearchStrategy(self.machine, max_actions=5)
        self.assertEqual(strategy._machine, self.machine)
        self.assertEqual(strategy._max_actions, 5)
        self.assertIsNone(strategy._to_state)

    def test_strategy_with_to_state(self):
        """Test strategy initialization with target state"""
        strategy = DepthFirstSearchStrategy(self.machine, max_actions=5, to_state="End")
        self.assertEqual(strategy._to_state, "End")

    def test_strategy_invalid_to_state(self):
        """Test strategy initialization with invalid target state"""
        with self.assertRaises(AssertionError):
            DepthFirstSearchStrategy(self.machine, max_actions=5, to_state="NonExistent")

    def test_variable_value_sets_no_variables(self):
        """Test variable value generation with no variables"""
        # Create a simple machine with no variables and no external state references
        simple_state = State("Simple", [], [])
        machine = Machine([simple_state], [], [])
        machine.validate()  # Validate the machine to set up relationships
        strategy = DepthFirstSearchStrategy(machine, max_actions=1)
        value_sets = list(strategy._variable_value_sets([]))
        self.assertEqual(value_sets, [[]])

    def test_variable_value_sets_with_variables(self):
        """Test variable value generation with variables"""
        strategy = DepthFirstSearchStrategy(self.machine, max_actions=1)
        value_sets = list(strategy._variable_value_sets([self.var1, self.var2]))
        
        expected_sets = [
            ["a", "1"], ["a", "2"], ["b", "1"], ["b", "2"]
        ]
        self.assertEqual(len(value_sets), 4)
        for value_set in value_sets:
            self.assertIn(value_set, expected_sets)

    def test_generate_tests_simple(self):
        """Test test generation for simple machine"""
        strategy = DepthFirstSearchStrategy(self.machine, max_actions=2)
        tests = list(strategy.tests())
        
        # Should generate tests for each variable combination
        self.assertGreater(len(tests), 0)
        
        # Each test should be a tuple of (test_sequence, variable_values)
        for test, values in tests:
            self.assertIsInstance(test, list)
            self.assertIsInstance(values, list)
            self.assertEqual(len(values), 2)  # Two variables

    def test_generate_tests_with_max_actions(self):
        """Test that max_actions limit is respected"""
        strategy = DepthFirstSearchStrategy(self.machine, max_actions=1)
        tests = list(strategy.tests())
        
        for test, values in tests:
            self.assertLessEqual(len(test), 1)

    def test_generate_tests_with_to_state(self):
        """Test test generation with target state"""
        strategy = DepthFirstSearchStrategy(self.machine, max_actions=3, to_state="End")
        tests = list(strategy.tests())
        
        # All tests should end in the target state
        for test, values in tests:
            if test:  # If test is not empty
                self.assertEqual(test[-1].next_state.name, "End")


class TestRandomStrategy(unittest.TestCase):
    """Unit tests for the RandomStrategy"""

    def setUp(self):
        """Set up a simple test machine"""
        # Create states
        self.start_state = State("Start", ["Print Starting"], [])
        self.middle_state = State("Middle", ["Print Middle"], [])
        self.end_state = State("End", ["Print End"], [])
        
        # Create variables
        self.var1 = Variable("${VAR1}", ["a", "b"])
        
        # Create actions with state names
        self.action1 = Action("go_to_middle", "Middle")
        self.action2 = Action("go_to_end", "End")
        self.action3 = Action("finish", "End")
        
        # Add actions to states
        self.start_state._actions = [self.action1, self.action2]
        self.middle_state._actions = [self.action3]
        self.end_state._actions = []
        
        # Create machine
        self.machine = Machine(
            [self.start_state, self.middle_state, self.end_state],
            [self.var1],
            []
        )
        # Validate the machine to set up relationships
        self.machine.validate()

    def test_strategy_initialization(self):
        """Test strategy initialization"""
        strategy = RandomStrategy(self.machine, max_actions=5)
        self.assertEqual(strategy._machine, self.machine)
        self.assertEqual(strategy._max_actions, 5)
        self.assertIsNone(strategy._to_state)

    def test_generate_variable_values(self):
        """Test random variable value generation"""
        strategy = RandomStrategy(self.machine, max_actions=5)
        
        # Generate multiple sets of values
        for _ in range(10):
            values = strategy._generate_variable_values()
            self.assertEqual(len(values), 1)  # One variable
            self.assertIn(values[0], ["a", "b"])  # Valid value

    def test_generate_test(self):
        """Test random test generation"""
        strategy = RandomStrategy(self.machine, max_actions=3)
        
        # Generate multiple tests
        for _ in range(10):
            values = strategy._generate_variable_values()
            test = strategy._generate_test(values)
            
            self.assertIsInstance(test, list)
            self.assertLessEqual(len(test), 3)  # Respects max_actions

    def test_generate_tests_iterator(self):
        """Test that tests() returns an iterator"""
        strategy = RandomStrategy(self.machine, max_actions=2)
        
        # Get a few tests from the iterator
        tests_iter = strategy.tests()
        for i, (test, values) in enumerate(tests_iter):
            self.assertIsInstance(test, list)
            self.assertIsInstance(values, list)
            if i >= 5:  # Just test a few iterations
                break

    def test_matching_to_state(self):
        """Test the _matching_to_state method"""
        strategy = RandomStrategy(self.machine, max_actions=2, to_state="End")
        
        # Test with matching state
        test_matching = [self.action2]  # Goes to End
        self.assertTrue(strategy._matching_to_state(test_matching))
        
        # Test with non-matching state
        test_non_matching = [self.action1]  # Goes to Middle
        self.assertFalse(strategy._matching_to_state(test_non_matching))


class TestStrategyWithConditions(unittest.TestCase):
    """Test strategies with conditional actions"""

    def setUp(self):
        """Set up a machine with conditional actions"""
        # Create states
        self.start_state = State("Start", [], [])
        self.success_state = State("Success", [], [])
        self.failure_state = State("Failure", [], [])
        
        # Create variable
        self.var = Variable("${RESULT}", ["success", "failure"])
        
        # Create conditional actions with state names
        self.success_condition = Condition("${RESULT}", "success")
        self.failure_condition = Condition("${RESULT}", "failure")
        
        self.success_action = Action("succeed", "Success", self.success_condition)
        self.failure_action = Action("fail", "Failure", self.failure_condition)
        
        # Add actions to start state
        self.start_state._actions = [self.success_action, self.failure_action]
        
        # Create machine
        self.machine = Machine(
            [self.start_state, self.success_state, self.failure_state],
            [self.var],
            []
        )
        # Validate the machine to set up relationships
        self.machine.validate()

    def test_depth_first_with_conditions(self):
        """Test depth-first strategy with conditional actions"""
        strategy = DepthFirstSearchStrategy(self.machine, max_actions=1)
        tests = list(strategy.tests())
        
        # Should generate tests for each variable value
        self.assertEqual(len(tests), 2)
        
        # Check that each test uses the correct action based on variable value
        for test, values in tests:
            if values[0] == "success":
                if test:  # If test is not empty
                    self.assertEqual(test[0].next_state.name, "Success")
            elif values[0] == "failure":
                if test:  # If test is not empty
                    self.assertEqual(test[0].next_state.name, "Failure")

    def test_random_with_conditions(self):
        """Test random strategy with conditional actions"""
        strategy = RandomStrategy(self.machine, max_actions=1)
        
        # Generate several tests
        for _ in range(10):
            test_iter = strategy.tests()
            test, values = next(test_iter)
            
            # Check that the action is available for the variable value
            if test:  # If test is not empty
                action = test[0]
                self.assertTrue(action.is_available())


if __name__ == '__main__':
    unittest.main()
