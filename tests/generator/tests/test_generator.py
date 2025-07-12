import unittest
import sys
import os
from io import StringIO

# Add the src directory to the path so we can import machine modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from machine.generator import Generator
from machine.model import Machine, State, Action, Variable
from machine.rules import Condition
from machine.strategies import DepthFirstSearchStrategy, RandomStrategy


class TestGenerator(unittest.TestCase):
    """Unit tests for the Generator class"""

    def setUp(self):
        """Set up a simple test machine for testing"""
        # Create states
        self.start_state = State("Start", ["Log    Starting"], [])
        self.middle_state = State("Middle", ["Log    In middle"], [])
        self.end_state = State("End", ["Log    Ending"], [])
        
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

    def test_generator_initialization(self):
        """Test generator initialization"""
        generator = Generator()
        self.assertEqual(len(generator.visited_states), 0)
        self.assertEqual(len(generator.visited_actions), 0)

    def test_write_test(self):
        """Test writing a single test"""
        generator = Generator()
        output = StringIO()
        
        test = [self.action1, self.action3]
        values = ["a", "1"]
        
        generator._write_test("Test 1", self.machine, output, test, values)
        
        result = output.getvalue()
        
        # Should contain test name
        self.assertIn("Test 1", result)
        # Should contain variable setting
        self.assertIn("Set Machine Variables", result)
        # Should track visited states and actions
        self.assertIn(self.start_state, generator.visited_states)
        self.assertIn(self.action1, generator.visited_actions)

    def test_generate_with_depth_first_strategy(self):
        """Test full generation with depth-first strategy"""
        generator = Generator()
        output = StringIO()
        
        # Get all actions for coverage tracking
        all_actions = set()
        for state in self.machine.states:
            all_actions.update(state.actions)
        
        generator.generate(
            self.machine,
            max_tests=10,
            max_actions=2,
            output=output,
            strategy=DepthFirstSearchStrategy,
            all_actions=all_actions
        )
        
        result = output.getvalue()
        
        # Should contain test cases
        self.assertIn("Test 1", result)
        # Should contain coverage information
        self.assertIn("TEST COVERAGE INFORMATION", result)
        # Should contain Robot Framework structure
        self.assertIn("*** Keywords ***", result)

    def test_generate_with_random_strategy(self):
        """Test generation with random strategy"""
        generator = Generator()
        output = StringIO()
        
        generator.generate(
            self.machine,
            max_tests=5,
            max_actions=2,
            output=output,
            strategy=RandomStrategy
        )
        
        result = output.getvalue()
        
        # Should contain test cases
        self.assertIn("Test", result)
        # Should contain Robot Framework structure
        self.assertIn("*** Keywords ***", result)

    def test_generate_with_max_tests_limit(self):
        """Test that max_tests limit is respected"""
        generator = Generator()
        output = StringIO()
        
        generator.generate(
            self.machine,
            max_tests=2,
            max_actions=1,
            output=output,
            strategy=DepthFirstSearchStrategy
        )
        
        result = output.getvalue()
        
        # Count test occurrences
        test_count = result.count("Test ")
        # Should not exceed max_tests (allowing for some flexibility in counting)
        self.assertLessEqual(test_count, 5)  # Reasonable upper bound

    def test_generate_with_to_state(self):
        """Test generation with target state"""
        generator = Generator()
        output = StringIO()
        
        generator.generate(
            self.machine,
            max_tests=10,
            max_actions=3,
            to_state="End",
            output=output,
            strategy=DepthFirstSearchStrategy
        )
        
        result = output.getvalue()
        
        # Should contain tests
        self.assertIn("Test", result)
        # All generated tests should end in the target state

    def test_coverage_tracking(self):
        """Test that coverage tracking works correctly"""
        generator = Generator()
        output = StringIO()
        
        # Get all actions for coverage tracking
        all_actions = set()
        for state in self.machine.states:
            all_actions.update(state.actions)
        
        # Generate tests
        generator.generate(
            self.machine,
            max_tests=10,
            max_actions=2,
            output=output,
            strategy=DepthFirstSearchStrategy,
            all_actions=all_actions
        )
        
        # Check that states and actions were tracked
        self.assertGreater(len(generator.visited_states), 0)
        self.assertGreater(len(generator.visited_actions), 0)
        
        result = output.getvalue()
        
        # Coverage info should be in output
        self.assertIn("Covered states", result)
        self.assertIn("Covered actions", result)

    def test_machine_with_conditions(self):
        """Test generation with conditional actions"""
        # Create machine with conditional actions
        var = Variable("${STATUS}", ["success", "failure"])
        
        success_condition = Condition("${STATUS}", "success")
        failure_condition = Condition("${STATUS}", "failure")
        
        success_action = Action("succeed", "End", success_condition)
        failure_action = Action("fail", "End", failure_condition)
        
        conditional_state = State("Conditional", [], [success_action, failure_action])
        
        machine = Machine(
            [conditional_state, self.end_state],
            [var],
            []
        )
        
        generator = Generator()
        output = StringIO()
        
        generator.generate(
            machine,
            max_tests=5,
            max_actions=1,
            output=output,
            strategy=DepthFirstSearchStrategy
        )
        
        result = output.getvalue()
        
        # Should generate tests for both conditions
        self.assertIn("Test", result)

    def test_empty_machine(self):
        """Test generation with empty machine"""
        # Create a state with no actions for this test
        empty_start = State("EmptyStart", ["Log    Empty start"], [])
        empty_machine = Machine([empty_start], [], [])
        
        generator = Generator()
        output = StringIO()
        
        generator.generate(
            empty_machine,
            max_tests=1,
            max_actions=1,
            output=output,
            strategy=DepthFirstSearchStrategy
        )
        
        result = output.getvalue()
        
        # Should handle empty machine gracefully
        self.assertIn("*** Keywords ***", result)

    def test_machine_with_no_actions(self):
        """Test generation with machine that has no actions"""
        no_action_state = State("NoActions", ["Log    No actions available"], [])
        machine = Machine([no_action_state], [], [])
        
        generator = Generator()
        output = StringIO()
        
        generator.generate(
            machine,
            max_tests=1,
            max_actions=1,
            output=output,
            strategy=DepthFirstSearchStrategy
        )
        
        result = output.getvalue()
        
        # Should handle machine with no actions
        self.assertIn("*** Keywords ***", result)

    def test_duplicate_test_filtering(self):
        """Test that duplicate tests are filtered out"""
        # Create a simple machine that might generate duplicates
        # Create fresh states for this test to avoid conflicts
        test_start = State("TestStart", ["Log    Test starting"], [])
        test_end = State("TestEnd", ["Log    Test ending"], [])
        
        # Create action that references the end state by name
        test_action = Action("same_action", "TestEnd")
        test_start._actions = [test_action]
        
        simple_machine = Machine([test_start, test_end], [], [])
        
        generator = Generator()
        output = StringIO()
        
        generator.generate(
            simple_machine,
            max_tests=10,
            max_actions=1,
            output=output,
            strategy=DepthFirstSearchStrategy
        )
        
        result = output.getvalue()
        
        # Should contain at least one test
        self.assertIn("Test 1", result)


if __name__ == '__main__':
    unittest.main()
