import re


class Machine(object):
    """Represents a finite state machine with states, variables, and rules."""

    def __init__(self, states, variables, rules, settings_table=None,
                 variables_table=None, keywords_table=None):
        self.states = states or []
        self.variables = variables or []
        self.rules = rules or []
        self._settings_table = settings_table or []
        self._variables_table = variables_table or []
        self._keywords_table = keywords_table or []
        self._validated = False

    def validate(self):
        """Validate the machine after all components are parsed."""
        if self._validated:
            return
        
        for state in self.states:
            state.set_machine(self)
        for variable in self.variables:
            variable.set_machine(self)
        self._validated = True

    @property
    def start_state(self):
        """Get the initial state of the machine."""
        if not self._validated:
            self.validate()
        return self.states[0]

    @property
    def variable_value_mapping(self):
        """Get current variable values as a dictionary."""
        if not self._validated:
            self.validate()
        return dict((v.name, v.current_value) for v in self.variables)

    def find_state_by_name(self, name):
        """Find a state by its name."""
        for state in self.states:
            if state.name == name:
                return state
        return None

    def find_variable_by_name(self, name):
        """Find a variable by its name."""
        for variable in self.variables:
            if variable.name == name:
                return variable
        return None

    def rules_are_ok(self, values):
        """Check if variable values satisfy all rules."""
        if not self._validated:
            self.validate()
        value_mapping = dict((v.name, value) for v, value in zip(self.variables, values))
        for rule in self.rules:
            if not rule.is_valid(value_mapping=value_mapping):
                return False
        return True

    def apply_variable_values(self, values):
        """Apply variable values to the machine."""
        if not self._validated:
            self.validate()
        for variable, value in zip(self.variables, values):
            variable.set_current_value(value)

    def write_settings_table(self, output):
        if self._settings_table:
            for content in self._settings_table:
                output.write(content)
            output.write('\n')  # Add spacing after settings

    def write_variables_table(self, output):
        if self._variables_table:
            for content in self._variables_table:
                output.write(content)
            output.write('\n')  # Add spacing after variables

    def write_keywords_table(self, output):
        for content in self._keywords_table:
            output.write('\n'+content)
        if not self._keywords_table:
            output.write('\n*** Keywords ***\n')
        if self.variables:
            self.write_variable_setter(output)
        for state in self.states:
            if state.steps:
                output.write(state.name+'\n')
                state.write_steps_to(output)

    def write_variable_setter(self, output):
        output.write('Set Machine Variables\n')
        output.write('  [Arguments]  {:s}\n'.format('  '.join(variable.name for variable in self.variables)))
        for variable in self.variables:
            output.write('  Set Test Variable  \\{:s}\n'.format(variable.name))

    @staticmethod
    def write_variable_setting_step(values, output):
        output.write('  Set Machine Variables  {:s}\n'.format('  '.join(values)))


class State(object):
    """Represents a state in the finite state machine."""

    def __init__(self, name, steps, actions):
        self.name = name
        self.steps = steps or []
        self._actions = actions or []

    @property
    def actions(self):
        """Get available actions from this state."""
        result = []
        names = set()
        for action in self._actions:
            if action.is_available() and action.name not in names:
                result.append(action)
                names.add(action.name)
        return result

    def set_machine(self, machine):
        """Associate this state with a machine and validate actions."""
        for action in self._actions:
            action.set_machine(machine)

    def write_steps_to(self, output):
        """Write state steps to output."""
        for step in self.steps:
            output.write(step + '\n')

    def write_to(self, output):
        """Write state to output."""
        if self.steps:
            output.write('  {:s}\n'.format(self.name))


class Action(object):
    """Represents an action that transitions between states."""

    def __init__(self, name, next_state, condition=None, args=None):
        self.name = name
        self._next_state_name = next_state
        self.condition = condition
        self.args = args or []
        self._machine = None

    def set_machine(self, machine):
        """Associate this action with a machine and validate target state."""
        self._machine = machine
        if not self.next_state:
            raise AssertionError('Invalid end state "{:s}" in '.format(self._next_state_name) +
                                 'action "{:s}"!'.format(self.name))

    @property
    def next_state(self):
        """Get the target state for this action."""
        return self._machine.find_state_by_name(self._next_state_name)

    def is_available(self):
        """Check if this action is available based on current conditions."""
        if not self.condition:
            return True
        if self.condition == 'otherwise':
            return True
        return self.condition.is_valid(value_mapping=self._machine.variable_value_mapping)

    def write_to(self, output):
        """Write action to output with resolved variables."""
        if self.name:
            if self.args:
                resolved_args = []
                for arg in self.args:
                    if self._machine and Variable.PATTERN.search(arg):
                        resolved_arg = Variable.PATTERN.sub(self._resolve_variable, arg)
                        resolved_args.append(resolved_arg)
                    else:
                        resolved_args.append(arg)
                args_str = '  '.join(resolved_args)
                output.write('  {:s}  {:s}\n'.format(self.name, args_str))
            else:
                output.write('  {:s}\n'.format(self.name))
        self.next_state.write_to(output)

    def _resolve_variable(self, var_match):
        """Helper method to resolve variable references in arguments."""
        var = self._machine.find_variable_by_name(var_match.group(0))
        if not var:
            return var_match.group(0)
        return var.current_value


class Variable(object):
    """Represents a variable with multiple possible values."""
    
    REGEX = r'\$\{[_A-Z][_A-Z0-9]*\}'
    PATTERN = re.compile(REGEX)
    _NO_VALUE = object()

    def __init__(self, name, values):
        self.name = name
        self.values = values
        self._current_value = Variable._NO_VALUE
        self._machine = None

    def set_machine(self, machine):
        """Associate this variable with a machine."""
        self._machine = machine

    def set_current_value(self, value):
        """Set the current value of this variable."""
        self._current_value = value

    @property
    def current_value(self):
        """Get the current value with variable resolution."""
        if self._current_value is Variable._NO_VALUE:
            raise AssertionError('No current value set')
        return self._resolve_value(self._current_value)

    def _resolve_value(self, value):
        """Resolve variable references within the value."""
        if hasattr(self, '_resolving') and self._resolving:
            return value  # Prevent infinite recursion
        
        self._resolving = True
        try:
            return self.PATTERN.sub(self._resolve_variable, value)
        finally:
            self._resolving = False

    def _resolve_variable(self, var_match):
        """Helper method to resolve variable references."""
        var = self._machine.find_variable_by_name(var_match.group(0))
        if not var:
            return var_match.group(0)
        return var.current_value
