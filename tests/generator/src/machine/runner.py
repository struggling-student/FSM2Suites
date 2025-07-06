from __future__ import print_function

import os
import sys
from .parsing import MachineParsingException, parse

from . import __version__
import argparse

from .generator import Generator
from .strategies import DepthFirstSearchStrategy, RandomStrategy

if sys.version_info.major == 3:
    unicode = str

parser = argparse.ArgumentParser(description='Machine {:s} - '.format(__version__) +
                                 'a test data generator for Robot Framework',
                                 formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument('input', type=str, help='input file')
parser.add_argument('--output', '-o', type=str, default=None,
                    help='output file (default is input file with txt suffix)')
parser.add_argument('--tests-max', '-t',
                    type=int, default=1000,
                    help='maximum number of tests to generate (default 1000)')
parser.add_argument('--to-state', '-T',
                    type=str, default=None,
                    help='The state that all generated tests should end in.\n' +
                    'If none given, all states are considered valid test end states')
parser.add_argument('--actions-max', '-a',
                    type=int, default=100,
                    help='maximum number of actions to generate (default 100)')
parser.add_argument('--generation-algorithm', '-g',
                    type=str, default='dfs', choices=['dfs', 'random', 'allpairs-random'],
                    help='''\
Use test generation algorithm:
allpairs-random = generate tests randomly, use allpairs algorithm for parameter value selection
dfs = depth first search  (default)
random = generate tests randomly''')


def main():
    args = parser.parse_args()
    generator = Generator()
    strategy_class = _select_strategy(args.generation_algorithm)
    all_actions = set()

    if args.input.endswith('.txt') and not args.output:
        sys.exit('txt input not allowed when no output')
    try:
        with open(args.input, 'r') as inp:
            machine = parse(inp.read())
    except IOError as e:
        sys.exit(unicode(e))
    except MachineParsingException as e:
        sys.exit(1)

    # File names:
    output_base_name = os.path.splitext(args.output or args.input)[0]
    output_test_file = output_base_name + '.robot'

    # Find unique actions:
    for state in machine.states:
        for action in state._actions:
            action._parent_state = state
            all_actions.add(action)

    # Generate tests:
    with open(output_test_file, 'w') as out:
        generator.generate(machine,
                           max_tests=args.tests_max,
                           max_actions=args.actions_max,
                           to_state=args.to_state,
                           output=out,
                           strategy=strategy_class)
    print('Generated test file: {:s}'.format(output_test_file))

    # Coverage information:
    covered_states = generator.visited_states
    covered_actions = generator.visited_actions
    uncovered_states = set(machine.states).difference(generator.visited_states)
    uncovered_actions = all_actions.difference(generator.visited_actions)
    #
    # Write to STDOUT:
    print('-' * 78)
    #
    # Covered states:
    print('Covered states ({:d}/{:d}):'.format(len(covered_states), len(machine.states)))
    if covered_states:
        for state in covered_states:
            print('    {:s}'.format(state.name))
    else:
        print('    -none-')
    #
    # Covered actions:
    print('\nCovered actions ({:d}/{:d}):'.format(len(covered_actions), len(all_actions)))
    if covered_actions:
        for action in covered_actions:
            action_name = action.name if action.name != '' else '[tau]'
            print('    {:s}  ({:s} -> {:s})'.format(action_name, action._parent_state.name, action.next_state.name))
    else:
        print('    -none-')
    #
    # Uncovered states:
    if uncovered_states:
        print('\nUncovered states ({:d}/{:d}):'.format(len(uncovered_states), len(machine.states)))
        for state in uncovered_states:
            print('    {:s}'.format(state.name))
    #
    # Uncovered actions:
    if uncovered_actions:
        print('\nUncovered actions ({:d}/{:d}):'.format(len(uncovered_actions), len(all_actions)))
        for action in uncovered_actions:
            action_name = action.name if action.name != '' else '[tau]'
            print('    {:s} ({:s} -> {:s})'.format(action_name, action._parent_state.name, action.next_state.name))
    print('-' * 78)


def _select_strategy(strategy):
    if strategy == 'random':
        return RandomStrategy
    if strategy == 'dfs':
        return DepthFirstSearchStrategy
    if strategy == 'allpairs-random':
        try:
            from src.machine.allpairsstrategy import AllPairsRandomStrategy
            return AllPairsRandomStrategy
        except ImportError:
            print('ERROR! allpairs-random strategy needs the AllPairs module')
            print('please install it from Python Package Index')
            print('pip install allpairspy')
            raise


if __name__ == '__main__':
    main()
