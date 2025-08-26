import unittest
import sys
import os
import tempfile
from io import StringIO

# Add the src directory to the path so we can import machine modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from machine import generate
from machine.generator import Generator
from machine.parsing import parse
from machine.strategies import DepthFirstSearchStrategy, RandomStrategy


class TestIntegration(unittest.TestCase):
    """Integration tests for the complete machine generator workflow"""

    def setUp(self):
        """Set up test data"""
        self.simple_machine_text = """*** Settings ***
Library    TestLibrary

*** Variables ***
${GLOBAL_VAR}    global_value

*** Machine ***
${STATUS}  any of  success  failure

Start
    Log    Starting test
  [Actions]
    process  ==>  Success  when  ${STATUS} == success
    process  ==>  Failure  when  ${STATUS} == failure

Success
    Log    Operation successful
  [Actions]
    continue  ==>  End

Failure
    Log    Operation failed
  [Actions]
    retry  ==>  Start
    abort  ==>  End

End
    Log    Test completed

*** Keywords ***
Process
    Log    Processing operation

Continue
    Log    Continuing operation

Retry
    Log    Retrying operation

Abort
    Log    Aborting operation
"""

        self.complex_machine_text = """*** Settings ***
Library    ComplexLibrary
Test Setup    Setup Complex Test
Test Teardown    Teardown Complex Test

*** Variables ***
${MAX_RETRIES}    3
${TIMEOUT}        30s

*** Machine ***
${USER_TYPE}     any of  admin  user  guest
${ACTION}        any of  read  write  delete
${RESOURCE}      any of  file1  file2  file3
${RETRY_COUNT}   any of  0  1  2  3

${USER_TYPE} == admin  ==>  ${ACTION} in (read, write, delete)
${USER_TYPE} == user   ==>  ${ACTION} in (read, write)
${USER_TYPE} == guest  ==>  ${ACTION} == read
${RETRY_COUNT} <= ${MAX_RETRIES}

Login
    Log    User login: ${USER_TYPE}
  [Actions]
    authenticate  ==>  Authenticated  when  ${USER_TYPE} != guest
    authenticate  ==>  GuestMode      when  ${USER_TYPE} == guest

Authenticated
    Log    User authenticated successfully
  [Actions]
    access_resource  ==>  AccessGranted   when  ${USER_TYPE} == admin
    access_resource  ==>  AccessGranted   when  ${USER_TYPE} == user  and  ${ACTION} != delete
    access_resource  ==>  AccessDenied    otherwise

GuestMode
    Log    Operating in guest mode
  [Actions]
    access_resource  ==>  AccessGranted  when  ${ACTION} == read
    access_resource  ==>  AccessDenied   otherwise

AccessGranted
    Log    Access granted for ${ACTION} on ${RESOURCE}
  [Actions]
    perform_action  ==>  Success   when  ${RESOURCE} != file3
    perform_action  ==>  Failure   when  ${RESOURCE} == file3  and  ${RETRY_COUNT} >= 3
    perform_action  ==>  Retry     when  ${RESOURCE} == file3  and  ${RETRY_COUNT} < 3

AccessDenied
    Log    Access denied
  [Actions]
    logout  ==>  End

Success
    Log    Operation completed successfully
  [Actions]
    logout  ==>  End

Failure
    Log    Operation failed permanently
  [Actions]
    logout  ==>  End

Retry
    Log    Retrying operation (attempt ${RETRY_COUNT})
  [Actions]
    increment_retry  ==>  Authenticated

End
    Log    Session ended

*** Keywords ***
Setup Complex Test
    Log    Setting up complex test environment

Teardown Complex Test
    Log    Cleaning up test environment

Authenticate
    Log    Authenticating user: ${USER_TYPE}

Access Resource
    Log    Accessing resource: ${RESOURCE} for action: ${ACTION}

Perform Action
    Log    Performing ${ACTION} on ${RESOURCE}

Increment Retry
    Log    Incrementing retry count
    Set Test Variable    ${RETRY_COUNT}    ${RETRY_COUNT + 1}

Logout
    Log    User logged out
"""

    def test_parse_and_generate_simple_machine(self):
        """Test complete workflow: parse and generate from simple machine"""
        machine = parse(self.simple_machine_text)
        
        # Verify parsing worked
        self.assertEqual(len(machine.states), 4)  # Start, Success, Failure, End
        self.assertEqual(len(machine.variables), 1)  # STATUS
        
        # Generate tests with coverage information
        output = StringIO()
        generator = Generator()
        
        # Get all actions for coverage tracking
        all_actions = set()
        for state in machine.states:
            all_actions.update(state._actions)  # Use _actions to avoid condition evaluation
        
        generator.generate(
            machine,
            max_tests=10,
            max_actions=3,
            output=output,
            strategy=DepthFirstSearchStrategy,
            all_actions=all_actions
        )
        
        generated_content = output.getvalue()
        
        # Verify generated content structure
        self.assertIn("*** Settings ***", generated_content)
        self.assertIn("*** Variables ***", generated_content)
        self.assertIn("*** Keywords ***", generated_content)
        self.assertIn("Test 1", generated_content)
        
        # Verify coverage information
        self.assertIn("TEST COVERAGE INFORMATION", generated_content)
        self.assertIn("Covered states", generated_content)
        self.assertIn("Covered actions", generated_content)

    def test_parse_and_generate_complex_machine(self):
        """Test complete workflow with complex machine including rules"""
        machine = parse(self.complex_machine_text)
        
        # Verify parsing of complex elements
        self.assertEqual(len(machine.states), 9)  # Login, Authenticated, GuestMode, AccessGranted, AccessDenied, Success, Failure, Retry, End
        self.assertEqual(len(machine.variables), 4)
        self.assertTrue(len(machine.rules) > 0)  # Should have constraint rules
        
        # Generate tests with depth-first strategy
        output = StringIO()
        generate(
            machine,
            max_tests=20,
            max_actions=5,
            output=output,
            strategy=DepthFirstSearchStrategy
        )
        
        generated_content = output.getvalue()
        
        # Verify structure
        self.assertIn("*** Settings ***", generated_content)
        self.assertIn("Test Setup", generated_content)
        self.assertIn("Test Teardown", generated_content)
        
        # Should contain variable combinations that satisfy rules
        self.assertIn("Set Machine Variables", generated_content)

    def test_generate_with_random_strategy(self):
        """Test generation with random strategy"""
        machine = parse(self.simple_machine_text)
        
        output = StringIO()
        generate(
            machine,
            max_tests=5,
            max_actions=2,
            output=output,
            strategy=RandomStrategy
        )
        
        generated_content = output.getvalue()
        
        # Should generate valid Robot Framework tests
        self.assertIn("Test", generated_content)
        self.assertIn("*** Keywords ***", generated_content)

    def test_generate_with_target_state(self):
        """Test generation with specific target state"""
        machine = parse(self.simple_machine_text)
        
        output = StringIO()
        generate(
            machine,
            max_tests=10,
            max_actions=5,
            to_state="Success",
            output=output,
            strategy=DepthFirstSearchStrategy
        )
        
        generated_content = output.getvalue()
        
        # Should contain tests
        self.assertIn("Test", generated_content)

    def test_end_to_end_file_processing(self):
        """Test complete file-based workflow"""
        # Create temporary machine file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.machine', delete=False) as f:
            f.write(self.simple_machine_text)
            machine_file = f.name
        
        try:
            # Read and parse machine file
            with open(machine_file, 'r') as f:
                content = f.read()
            
            machine = parse(content)
            
            # Generate to temporary output file
            with tempfile.NamedTemporaryFile(mode='w', suffix='.robot', delete=False) as f:
                output_file = f.name
            
            try:
                with open(output_file, 'w') as f:
                    generate(
                        machine,
                        max_tests=5,
                        max_actions=3,
                        output=f,
                        strategy=DepthFirstSearchStrategy
                    )
                
                # Verify output file
                with open(output_file, 'r') as f:
                    content = f.read()
                
                self.assertIn("*** Keywords ***", content)
                self.assertIn("Test", content)
                
            finally:
                os.unlink(output_file)
        finally:
            os.unlink(machine_file)

    def test_machine_with_no_valid_variable_combinations(self):
        """Test machine with contradictory rules"""
        contradictory_machine = """*** Machine ***
${VAR1}  any of  a  b
${VAR2}  any of  1  2

${VAR1} == a  ==>  ${VAR2} == 1
${VAR1} == a  ==>  ${VAR2} == 2

Start
  [Actions]
    action  ==>  End

End
"""
        machine = parse(contradictory_machine)
        
        output = StringIO()
        generate(
            machine,
            max_tests=10,
            max_actions=1,
            output=output,
            strategy=DepthFirstSearchStrategy
        )
        
        generated_content = output.getvalue()
        
        # Should handle contradictory rules gracefully
        self.assertIn("*** Keywords ***", generated_content)

    def test_large_machine_performance(self):
        """Test performance with larger machine definition"""
        large_machine = """*** Machine ***
${VAR1}  any of  a  b  c  d  e
${VAR2}  any of  1  2  3  4  5
${VAR3}  any of  x  y  z

Start
  [Actions]
    action1  ==>  State1  when  ${VAR1} in (a, b)
    action2  ==>  State2  when  ${VAR1} in (c, d, e)

State1
  [Actions]
    action3  ==>  State3  when  ${VAR2} > 2
    action4  ==>  End     when  ${VAR2} <= 2

State2
  [Actions]
    action5  ==>  State3  when  ${VAR3} != z
    action6  ==>  End     when  ${VAR3} == z

State3
  [Actions]
    action7  ==>  End

End
"""
        machine = parse(large_machine)
        
        output = StringIO()
        # Limit tests to keep test runtime reasonable
        generate(
            machine,
            max_tests=20,
            max_actions=4,
            output=output,
            strategy=DepthFirstSearchStrategy
        )
        
        generated_content = output.getvalue()
        
        # Should complete successfully
        self.assertIn("*** Keywords ***", generated_content)
        self.assertIn("Test", generated_content)

    def test_machine_with_all_condition_types(self):
        """Test machine using various condition types"""
        conditions_machine = """*** Machine ***
${NUM}    any of  1  5  10
${TEXT}   any of  hello  world  test
${FLAG}   any of  true  false

Start
  [Actions]
    action1  ==>  State1  when  ${NUM} > 3
    action2  ==>  State2  when  ${NUM} <= 3
    action3  ==>  State3  when  ${TEXT} ~ .*llo.*
    action4  ==>  State4  when  ${FLAG} != true

State1
State2
State3
State4
"""
        machine = parse(conditions_machine)
        
        output = StringIO()
        generate(
            machine,
            max_tests=15,
            max_actions=1,
            output=output,
            strategy=DepthFirstSearchStrategy
        )
        
        generated_content = output.getvalue()
        
        # Should handle various condition types
        self.assertIn("*** Keywords ***", generated_content)
        self.assertIn("Test", generated_content)


if __name__ == '__main__':
    unittest.main()
