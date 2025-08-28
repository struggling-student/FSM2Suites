import random


class _Strategy(object):
    """Base class for test generation strategies."""

    def __init__(self, machine, max_actions, to_state=None):
        self._machine = machine
        self._max_actions = max_actions
        self._to_state = to_state
        assert not to_state or self._machine.find_state_by_name(to_state)

    def _matching_to_state(self, test):
        """Check if test ends in the target state."""
        return not self._to_state or self._to_state == test[-1].next_state.name


class DepthFirstSearchStrategy(_Strategy):
    """Enhanced DFS strategy with loop prevention and diverse exploration."""

    def __init__(self, machine, max_actions, to_state=None):
        super(DepthFirstSearchStrategy, self).__init__(machine, max_actions, to_state)
        self._explored_state_action_pairs = set()

    def tests(self):
        """Enhanced DFS with loop prevention and diverse exploration."""
        all_combinations = list(self._variable_value_sets(self._machine.variables))
        
        # If no combinations available, use empty values
        if not all_combinations:
            all_combinations = [[]]
        
        for values in all_combinations:
            self._machine.apply_variable_values(values)
            
            # Generate tests with different path lengths to ensure diversity
            path_lengths = [3, 7, max(10, self._max_actions // 2), self._max_actions]
            path_lengths = [length for length in path_lengths if length <= self._max_actions]
            
            for max_len in path_lengths:
                test_count = 0
                max_tests_per_combo = max(5, 50 // len(all_combinations))
                
                for test in self._generate_diverse_paths(self._machine.start_state, max_len):
                    if test_count >= max_tests_per_combo:
                        break
                    if self._matching_to_state(test):
                        yield test, [v.current_value for v in self._machine.variables]
                        test_count += 1

    def _variable_value_sets(self, variables):
        """Generate all valid combinations of variable values."""
        if not variables:
            return ([],)
        return (vs for vs in self._var_set(variables) if self._machine.rules_are_ok(vs))

    def _var_set(self, vars):
        """Generate cartesian product of variable values."""
        if not vars:
            return [[]]
        return ([val] + sub_set for val in vars[0].values for sub_set in self._var_set(vars[1:]))

    def _generate_diverse_paths(self, state, max_actions, visited_in_path=None):
        """Generate diverse paths with cycle detection and state-action tracking."""
        if visited_in_path is None:
            visited_in_path = []
        
        if not state.actions or max_actions == 0:
            yield []
            return
        
        # Limit consecutive visits to same state (prevents tight loops)
        recent_visits = visited_in_path[-4:] if len(visited_in_path) > 4 else visited_in_path
        if recent_visits.count(state.name) >= 2:
            # Allow one more visit, then stop to prevent infinite loops
            if len([s for s in recent_visits if s == state.name]) >= 2:
                yield []
                return
        
        # Prioritize unexplored state-action pairs for better coverage
        unexplored_actions = []
        explored_actions = []
        
        for action in state.actions:
            pair_key = (state.name, action.name, action.next_state.name)
            if pair_key not in self._explored_state_action_pairs:
                unexplored_actions.append(action)
            else:
                explored_actions.append(action)
        
        # Try unexplored actions first, then explored ones
        actions_to_try = unexplored_actions + explored_actions
        
        for action in actions_to_try:
            # Mark this state-action pair as explored
            pair_key = (state.name, action.name, action.next_state.name)
            self._explored_state_action_pairs.add(pair_key)
            
            new_path = visited_in_path + [state.name]
            
            for test in self._generate_diverse_paths(action.next_state, max_actions - 1, new_path):
                yield [action] + test
            
            # For unexplored actions, generate multiple paths if possible
            if action in unexplored_actions and max_actions > 1:
                # Generate a few more paths from this action to explore thoroughly
                extra_paths = 0
                for test in self._generate_diverse_paths(action.next_state, max_actions - 1, new_path):
                    if extra_paths >= 2:  # Limit extra exploration
                        break
                    yield [action] + test
                    extra_paths += 1


class RandomStrategy(_Strategy):
    """Strategy that generates tests randomly."""

    def tests(self):
        """Generate tests randomly until stopped."""
        while True:
            test = self._generate_test(self._generate_variable_values())
            if not test and self._to_state and self._to_state != self._machine.start_state.name:
                continue
            yield test, [v.current_value for v in self._machine.variables]

    def _generate_test(self, values):
        """Generate a single random test."""
        test = []
        self._machine.apply_variable_values(values)
        current_state = self._machine.start_state
        while self._max_actions > len(test) and current_state.actions:
            action = random.choice(current_state.actions)
            current_state = action.next_state
            test.append(action)
        while test and not self._matching_to_state(test):
            test.pop()
        return test

    def _generate_variable_values(self):
        """Generate random variable values that satisfy all rules."""
        while True:
            candidate = [random.choice(v.values) for v in self._machine.variables]
            if self._machine.rules_are_ok(candidate):
                return candidate

