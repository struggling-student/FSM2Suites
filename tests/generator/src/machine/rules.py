import re


class EquivalenceRule(object):
    """Rule that enforces two conditions have the same truth value."""

    def __init__(self, condition1, condition2):
        self._condition1 = condition1
        self._condition2 = condition2

    def __str__(self):
        return '{:s}  <==>  {:s}'.format(str(self._condition1), str(self._condition2))

    def is_valid(self, value_mapping):
        return self._condition1.is_valid(value_mapping) == self._condition2.is_valid(value_mapping)


class ImplicationRule(object):
    """Rule that enforces logical implication between two conditions."""

    def __init__(self, condition1, condition2):
        self._condition1 = condition1
        self._condition2 = condition2

    def __str__(self):
        return '{:s}  ==>  {:s}'.format(str(self._condition1), str(self._condition2))

    def is_valid(self, value_mapping):
        return not self._condition1.is_valid(value_mapping) or self._condition2.is_valid(value_mapping)


class AndRule(object):
    """Rule that enforces all conditions must be true."""

    def __init__(self, conditions):
        self._conditions = conditions

    def __str__(self):
        return '  and  '.join(str(c) for c in self._conditions)

    def is_valid(self, value_mapping):
        return not(any(not(c.is_valid(value_mapping)) for c in self._conditions))


class OrRule(object):
    """Rule that enforces at least one condition must be true."""

    def __init__(self, conditions):
        self._conditions = conditions

    def __str__(self):
        return '  or  '.join(str(c) for c in self._conditions)

    def is_valid(self, value_mapping):
        return any(c.is_valid(value_mapping) for c in self._conditions)


class NotRule(object):
    """Rule that negates a condition."""

    def __init__(self, condition):
        self._condition = condition

    def __str__(self):
        return 'not ({:s})'.format(str(self._condition))

    def is_valid(self, value_mapping):
        return not self._condition.is_valid(value_mapping)


class Condition(object):
    """Basic equality condition for variable values."""

    def __init__(self, variable_name, value):
        self._name = variable_name.strip()
        self._value = value.strip()

    def __str__(self):
        return '{:s} == {:s}'.format(self._name, self._value)

    def is_valid(self, value_mapping):
        return value_mapping[self._name].strip() == self._value.strip()


def UnequalCondition(variable_name, value):
    """Factory function for inequality condition."""
    return NotRule(Condition(variable_name, value))


class GreaterThanCondition(object):
    """Condition for greater than comparison."""

    def __init__(self, variable_name, value):
        self._name = variable_name.strip()
        self._value = value.strip()

    def __str__(self):
        return '{:s} > {:s}'.format(self._name, self._value)

    def is_valid(self, value_mapping):
        return value_mapping[self._name].strip() > self._value.strip()


class GreaterThanOrEqualCondition(object):
    """Condition for greater than or equal comparison."""

    def __init__(self, variable_name, value):
        self._name = variable_name.strip()
        self._value = value.strip()

    def __str__(self):
        return '{:s} >= {:s}'.format(self._name, self._value)

    def is_valid(self, value_mapping):
        return value_mapping[self._name].strip() >= self._value.strip()


class LessThanCondition(object):
    """Condition for less than comparison."""

    def __init__(self, variable_name, value):
        self._name = variable_name.strip()
        self._value = value.strip()

    def __str__(self):
        return '{:s} < {:s}'.format(self._name, self._value)

    def is_valid(self, value_mapping):
        return value_mapping[self._name].strip() < self._value.strip()


class LessThanOrEqualCondition(object):
    """Condition for less than or equal comparison."""

    def __init__(self, variable_name, value):
        self._name = variable_name.strip()
        self._value = value.strip()

    def __str__(self):
        return '{:s} <= {:s}'.format(self._name, self._value)

    def is_valid(self, value_mapping):
        return value_mapping[self._name].strip() <= self._value.strip()


class RegexCondition(object):
    """Condition for regex pattern matching."""

    def __init__(self, variable_name, value):
        self._name = variable_name.strip()
        self._value = value.strip()

    def __str__(self):
        return '{:s} ~ {:s}'.format(self._name, self._value)

    def is_valid(self, value_mapping):
        return re.search(self._value.strip(), value_mapping[self._name].strip()) is not None


class RegexNegatedCondition(object):
    """Condition for negated regex pattern matching."""

    def __init__(self, variable_name, value):
        self._name = variable_name.strip()
        self._value = value.strip()

    def __str__(self):
        return '{:s} !~ {:s}'.format(self._name, self._value)

    def is_valid(self, value_mapping):
        return re.search(self._value.strip(), value_mapping[self._name].strip()) is None
