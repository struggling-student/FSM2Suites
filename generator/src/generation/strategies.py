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

    def __init__(self, machine, max_actions, to_state=None):
        super(RandomStrategy, self).__init__(machine, max_actions, to_state)
        self._max_generation_attempts = 1000
        self._max_variable_attempts = 100

    def tests(self):
        """Generate tests randomly with limits to prevent infinite loops."""
        generation_attempts = 0
        successful_tests = 0
        max_successful_tests = 100  # Reasonable upper bound
        
        while generation_attempts < self._max_generation_attempts and successful_tests < max_successful_tests:
            generation_attempts += 1
            
            try:
                variable_values = self._generate_variable_values()
                if variable_values is None:
                    continue
                    
                test = self._generate_test(variable_values)
                if test is not None:
                    successful_tests += 1
                    yield test, [v.current_value for v in self._machine.variables]
                elif self._to_state and self._to_state != self._machine.start_state.name:
                    continue
                else:
                    # Even empty tests are valid if no target state is specified
                    successful_tests += 1
                    yield [], [v.current_value for v in self._machine.variables]
            except Exception:
                # Skip problematic combinations and continue
                continue

    def _generate_test(self, values):
        """Generate a single random test."""
        if values is None:
            return None
            
        test = []
        try:
            self._machine.apply_variable_values(values)
            current_state = self._machine.start_state
            
            # Prevent infinite loops in test generation
            max_attempts = max(50, self._max_actions * 2)
            attempts = 0
            
            while (self._max_actions < 0 or self._max_actions > len(test)) and current_state.actions and attempts < max_attempts:
                attempts += 1
                action = random.choice(current_state.actions)
                current_state = action.next_state
                test.append(action)
                
                # Break if we've reached a reasonable test length
                if len(test) >= 20:  # Safety limit
                    break
            
            # Trim test to match target state if specified
            trimming_attempts = 0
            while test and not self._matching_to_state(test) and trimming_attempts < len(test):
                test.pop()
                trimming_attempts += 1
                
            return test
        except Exception:
            return None

    def _generate_variable_values(self):
        """Generate random variable values that satisfy all rules."""
        if not self._machine.variables:
            return []
            
        attempts = 0
        while attempts < self._max_variable_attempts:
            attempts += 1
            try:
                candidate = [random.choice(v.values) for v in self._machine.variables]
                if self._machine.rules_are_ok(candidate):
                    return candidate
            except Exception:
                continue
        
        # If we can't find valid combinations, try a simpler approach
        # Just return the first value for each variable
        try:
            simple_candidate = [v.values[0] for v in self._machine.variables]
            if self._machine.rules_are_ok(simple_candidate):
                return simple_candidate
        except Exception:
            pass
            
        return None

