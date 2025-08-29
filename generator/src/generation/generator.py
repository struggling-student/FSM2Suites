from io import StringIO
from ..parsing.parsing import parse
from .strategies import DepthFirstSearchStrategy


class Generator(object):
    """Generator for creating Robot Framework test files from state machines."""
    
    def __init__(self):
        self.visited_states = set()
        self.visited_actions = set()

    def generate(self, machine, max_tests=1000, max_actions=None, to_state=None, output=None,
                 strategy=DepthFirstSearchStrategy, all_actions=None):
        """Generate test cases and write them to output."""
        max_actions = -1 if max_actions is None else max_actions
        
        if all_actions is not None:
            self._generate_with_coverage(machine, max_tests, max_actions, to_state, output, strategy, all_actions)
        else:
            self._generate_without_coverage(machine, max_tests, max_actions, to_state, output, strategy)

    def transform(self, text, all_actions=None):
        """Transform machine definition text into Robot Framework test file."""
        output = StringIO()
        machine = parse(text)
        
        if all_actions is None:
            all_actions = self._collect_all_actions(machine)
        
        self.generate(machine, output=output, all_actions=all_actions)
        return output.getvalue()

    def _generate_with_coverage(self, machine, max_tests, max_actions, to_state, output, strategy, all_actions):
        """Generate tests with coverage information."""
        temp_output = StringIO()
        self._write_full_test_file(machine, max_tests, max_actions, to_state, temp_output, strategy)
        
        self._write_coverage_comments(machine, all_actions, output)
        output.write(temp_output.getvalue())

    def _generate_without_coverage(self, machine, max_tests, max_actions, to_state, output, strategy):
        """Generate tests without coverage information."""
        self._write_full_test_file(machine, max_tests, max_actions, to_state, output, strategy)

    def _write_full_test_file(self, machine, max_tests, max_actions, to_state, output, strategy):
        """Write complete test file with settings, variables, tests, and keywords."""
        machine.write_settings_table(output)
        machine.write_variables_table(output)
        output.write('*** Test Cases ***')
        self._write_tests(machine, max_tests, max_actions, to_state, output, strategy)
        machine.write_keywords_table(output)

    def _collect_all_actions(self, machine):
        """Collect all actions from the machine states."""
        all_actions = set()
        for state in machine.states:
            for action in state._actions:
                all_actions.add(action)
        return all_actions

    def _write_test(self, name, machine, output, test, values):
        output.write('\n{:s}\n'.format(name))
        if values:
            machine.write_variable_setting_step(values, output)
        machine.start_state.write_to(output)
        self.visited_states.add(machine.start_state)
        for action in test:
            self.visited_actions.add(action)
            self.visited_states.add(action.next_state)
            action.write_to(output)

    def _write_tests(self, machine, max_tests, max_actions, to_state, output, strategy):
        i = 1
        skipped = 0
        generated_tests = set()

        strategy_class = strategy(machine, max_actions, to_state)
        for test, values in strategy_class.tests():
            if i > max_tests:
                print('--tests-max generation try limit {:d} reached with {:d} tests generated'.format(max_tests, i - 1))
                break
            if (tuple(test), tuple(values)) in generated_tests:
                skipped += 1
                continue
            else:
                generated_tests.add((tuple(test), tuple(values)))
            self._write_test('Test {:d}'.format(i), machine, output, test, values)
            i += 1

    def _write_coverage_comments(self, machine, all_actions, output):
        """Write coverage information as comments at the start of the file"""
        covered_states = self.visited_states
        covered_actions = self.visited_actions
        uncovered_states = set(machine.states).difference(self.visited_states)
        uncovered_actions = all_actions.difference(self.visited_actions)
        
        output.write('# ' + '=' * 76 + '\n')
        output.write('# TEST COVERAGE INFORMATION\n')
        output.write('# ' + '=' * 76 + '\n')
        output.write('#\n')
        
        # Covered states
        output.write('# Covered states ({:d}/{:d}):\n'.format(len(covered_states), len(machine.states)))
        if covered_states:
            for state in sorted(covered_states, key=lambda s: s.name):
                output.write('#     {:s}\n'.format(state.name))
        else:
            output.write('#     -none-\n')
        output.write('#\n')
        
        # Covered actions
        output.write('# Covered actions ({:d}/{:d}):\n'.format(len(covered_actions), len(all_actions)))
        if covered_actions:
            # Group actions by their parent state by searching through machine states
            for action in sorted(covered_actions, key=lambda a: a.name):
                action_name = action.name if action.name != '' else '[tau]'
                # Find parent state for this action
                parent_state_name = "Unknown"
                for state in machine.states:
                    if action in state._actions:
                        parent_state_name = state.name
                        break
                output.write('#     {:s}  ({:s} -> {:s})\n'.format(action_name, parent_state_name, action.next_state.name if action.next_state else action._next_state_name))
        else:
            output.write('#     -none-\n')
        output.write('#\n')
        
        # Uncovered states
        if uncovered_states:
            output.write('# Uncovered states ({:d}/{:d}):\n'.format(len(uncovered_states), len(machine.states)))
            for state in sorted(uncovered_states, key=lambda s: s.name):
                output.write('#     {:s}\n'.format(state.name))
            output.write('#\n')
        
        # Uncovered actions
        if uncovered_actions:
            output.write('# Uncovered actions ({:d}/{:d}):\n'.format(len(uncovered_actions), len(all_actions)))
            # Group actions by their parent state by searching through machine states
            for action in sorted(uncovered_actions, key=lambda a: a.name):
                action_name = action.name if action.name != '' else '[tau]'
                # Find parent state for this action
                parent_state_name = "Unknown"
                for state in machine.states:
                    if action in state._actions:
                        parent_state_name = state.name
                        break
                output.write('#     {:s} ({:s} -> {:s})\n'.format(action_name, parent_state_name, action.next_state.name if action.next_state else action._next_state_name))
            output.write('#\n')
        
        output.write('# ' + '=' * 76 + '\n')
        output.write('\n')

