from allpairspy import AllPairs
from .strategies import RandomStrategy


class AllPairsRandomStrategy(RandomStrategy):

    def __init__(self, machine, max_actions, to_state=None):
        if machine.rules:
            raise AssertionError('ERROR! AllPairs does not work correctly with rules')
        RandomStrategy.__init__(self, machine, max_actions, to_state)

    def tests(self):
        for values in self._generate_all_pairs_variable_values():
            test = self._generate_test(values)
            if not test and self._to_state and self._to_state != self._machine.start_state.name:
                continue
            yield test, [v.current_value for v in self._machine.variables]

    def _generate_all_pairs_variable_values(self):
        if len(list(self._machine.variables)) < 2:
            for var in self._machine.variables:
                return [v for v in var.values]
            return [[]]
        return AllPairs([v.values for v in self._machine.variables])
