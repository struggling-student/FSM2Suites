import unittest
import sys
import os

# Add the parent directory to the path so we can import src as a package
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.core import (
    Condition, UnequalCondition, GreaterThanCondition, GreaterThanOrEqualCondition,
    LessThanCondition, LessThanOrEqualCondition, RegexCondition, RegexNegatedCondition,
    AndRule, OrRule, NotRule, EquivalenceRule, ImplicationRule
)


class TestConditions(unittest.TestCase):
    """Unit tests for condition classes"""

    def test_condition_equal(self):
        """Test basic equality condition"""
        condition = Condition("${VAR}", "value1")
        
        # Test valid condition
        value_mapping = {"${VAR}": "value1"}
        self.assertTrue(condition.is_valid(value_mapping))
        
        # Test invalid condition
        value_mapping = {"${VAR}": "value2"}
        self.assertFalse(condition.is_valid(value_mapping))

    def test_unequal_condition(self):
        """Test inequality condition"""
        condition = UnequalCondition("${VAR}", "value1")
        
        # Test valid condition (not equal)
        value_mapping = {"${VAR}": "value2"}
        self.assertTrue(condition.is_valid(value_mapping))
        
        # Test invalid condition (equal)
        value_mapping = {"${VAR}": "value1"}
        self.assertFalse(condition.is_valid(value_mapping))

    def test_greater_than_condition(self):
        """Test greater than condition (string comparison)"""
        condition = GreaterThanCondition("${NUM}", "5")
        
        # Test valid condition - string comparison "9" > "5" is True
        value_mapping = {"${NUM}": "9"}
        self.assertTrue(condition.is_valid(value_mapping))
        
        # Test invalid condition - string comparison "3" > "5" is False  
        value_mapping = {"${NUM}": "3"}
        self.assertFalse(condition.is_valid(value_mapping))
        
        # Test equal value - string comparison "5" > "5" is False
        value_mapping = {"${NUM}": "5"}
        self.assertFalse(condition.is_valid(value_mapping))

    def test_greater_than_or_equal_condition(self):
        """Test greater than or equal condition (string comparison)"""
        condition = GreaterThanOrEqualCondition("${NUM}", "5")
        
        # Test valid conditions - string comparison "9" >= "5" is True
        value_mapping = {"${NUM}": "9"}
        self.assertTrue(condition.is_valid(value_mapping))
        
        # String comparison "5" >= "5" is True
        value_mapping = {"${NUM}": "5"}
        self.assertTrue(condition.is_valid(value_mapping))
        
        # Test invalid condition - string comparison "3" >= "5" is False
        value_mapping = {"${NUM}": "3"}
        self.assertFalse(condition.is_valid(value_mapping))

    def test_less_than_condition(self):
        """Test less than condition (string comparison)"""
        condition = LessThanCondition("${NUM}", "5")
        
        # Test valid condition - string comparison "3" < "5" is True
        value_mapping = {"${NUM}": "3"}
        self.assertTrue(condition.is_valid(value_mapping))
        
        # Test invalid condition - string comparison "9" < "5" is False
        value_mapping = {"${NUM}": "9"}
        self.assertFalse(condition.is_valid(value_mapping))
        
        # Test equal value - string comparison "5" < "5" is False
        value_mapping = {"${NUM}": "5"}
        self.assertFalse(condition.is_valid(value_mapping))

    def test_less_than_or_equal_condition(self):
        """Test less than or equal condition (string comparison)"""
        condition = LessThanOrEqualCondition("${NUM}", "5")
        
        # Test valid conditions - string comparison "3" <= "5" is True
        value_mapping = {"${NUM}": "3"}
        self.assertTrue(condition.is_valid(value_mapping))
        
        # String comparison "5" <= "5" is True
        value_mapping = {"${NUM}": "5"}
        self.assertTrue(condition.is_valid(value_mapping))
        
        # Test invalid condition - string comparison "9" <= "5" is False
        value_mapping = {"${NUM}": "9"}
        self.assertFalse(condition.is_valid(value_mapping))

    def test_regex_condition(self):
        """Test regex condition"""
        condition = RegexCondition("${EMAIL}", r".*@.*\.com")
        
        # Test valid email
        value_mapping = {"${EMAIL}": "test@example.com"}
        self.assertTrue(condition.is_valid(value_mapping))
        
        # Test invalid email
        value_mapping = {"${EMAIL}": "invalid-email"}
        self.assertFalse(condition.is_valid(value_mapping))

    def test_regex_negated_condition(self):
        """Test negated regex condition"""
        condition = RegexNegatedCondition("${EMAIL}", r".*@.*\.com")
        
        # Test invalid email (should be true for negated)
        value_mapping = {"${EMAIL}": "invalid-email"}
        self.assertTrue(condition.is_valid(value_mapping))
        
        # Test valid email (should be false for negated)
        value_mapping = {"${EMAIL}": "test@example.com"}
        self.assertFalse(condition.is_valid(value_mapping))


class TestCompositeRules(unittest.TestCase):
    """Unit tests for composite rule classes"""

    def setUp(self):
        self.condition1 = Condition("${VAR1}", "a")
        self.condition2 = Condition("${VAR2}", "1")
        self.condition3 = Condition("${VAR3}", "x")

    def test_and_rule(self):
        """Test AND rule"""
        and_rule = AndRule([self.condition1, self.condition2])
        
        # Test all conditions true
        value_mapping = {"${VAR1}": "a", "${VAR2}": "1"}
        self.assertTrue(and_rule.is_valid(value_mapping))
        
        # Test one condition false
        value_mapping = {"${VAR1}": "b", "${VAR2}": "1"}
        self.assertFalse(and_rule.is_valid(value_mapping))
        
        # Test all conditions false
        value_mapping = {"${VAR1}": "b", "${VAR2}": "2"}
        self.assertFalse(and_rule.is_valid(value_mapping))

    def test_or_rule(self):
        """Test OR rule"""
        or_rule = OrRule([self.condition1, self.condition2])
        
        # Test all conditions true
        value_mapping = {"${VAR1}": "a", "${VAR2}": "1"}
        self.assertTrue(or_rule.is_valid(value_mapping))
        
        # Test one condition true
        value_mapping = {"${VAR1}": "a", "${VAR2}": "2"}
        self.assertTrue(or_rule.is_valid(value_mapping))
        
        # Test all conditions false
        value_mapping = {"${VAR1}": "b", "${VAR2}": "2"}
        self.assertFalse(or_rule.is_valid(value_mapping))

    def test_not_rule(self):
        """Test NOT rule"""
        not_rule = NotRule(self.condition1)
        
        # Test condition false (NOT should be true)
        value_mapping = {"${VAR1}": "b"}
        self.assertTrue(not_rule.is_valid(value_mapping))
        
        # Test condition true (NOT should be false)
        value_mapping = {"${VAR1}": "a"}
        self.assertFalse(not_rule.is_valid(value_mapping))

    def test_equivalence_rule(self):
        """Test equivalence rule (biconditional)"""
        equiv_rule = EquivalenceRule(self.condition1, self.condition2)
        
        # Test both conditions true
        value_mapping = {"${VAR1}": "a", "${VAR2}": "1"}
        self.assertTrue(equiv_rule.is_valid(value_mapping))
        
        # Test both conditions false
        value_mapping = {"${VAR1}": "b", "${VAR2}": "2"}
        self.assertTrue(equiv_rule.is_valid(value_mapping))
        
        # Test one true, one false
        value_mapping = {"${VAR1}": "a", "${VAR2}": "2"}
        self.assertFalse(equiv_rule.is_valid(value_mapping))

    def test_implication_rule(self):
        """Test implication rule"""
        impl_rule = ImplicationRule(self.condition1, self.condition2)
        
        # Test antecedent false (implication always true)
        value_mapping = {"${VAR1}": "b", "${VAR2}": "1"}
        self.assertTrue(impl_rule.is_valid(value_mapping))
        
        value_mapping = {"${VAR1}": "b", "${VAR2}": "2"}
        self.assertTrue(impl_rule.is_valid(value_mapping))
        
        # Test antecedent true, consequent true
        value_mapping = {"${VAR1}": "a", "${VAR2}": "1"}
        self.assertTrue(impl_rule.is_valid(value_mapping))
        
        # Test antecedent true, consequent false
        value_mapping = {"${VAR1}": "a", "${VAR2}": "2"}
        self.assertFalse(impl_rule.is_valid(value_mapping))


class TestRuleStringRepresentation(unittest.TestCase):
    """Unit tests for string representations of rules"""

    def test_condition_str(self):
        """Test string representation of conditions"""
        condition = Condition("${VAR}", "value")
        self.assertEqual(str(condition), "${VAR} == value")

    def test_and_rule_str(self):
        """Test string representation of AND rule"""
        condition1 = Condition("${VAR1}", "a")
        condition2 = Condition("${VAR2}", "b")
        and_rule = AndRule([condition1, condition2])
        expected = "${VAR1} == a  and  ${VAR2} == b"
        self.assertEqual(str(and_rule), expected)

    def test_or_rule_str(self):
        """Test string representation of OR rule"""
        condition1 = Condition("${VAR1}", "a")
        condition2 = Condition("${VAR2}", "b")
        or_rule = OrRule([condition1, condition2])
        expected = "${VAR1} == a  or  ${VAR2} == b"
        self.assertEqual(str(or_rule), expected)

    def test_equivalence_rule_str(self):
        """Test string representation of equivalence rule"""
        condition1 = Condition("${VAR1}", "a")
        condition2 = Condition("${VAR2}", "b")
        equiv_rule = EquivalenceRule(condition1, condition2)
        expected = "${VAR1} == a  <==>  ${VAR2} == b"
        self.assertEqual(str(equiv_rule), expected)

    def test_implication_rule_str(self):
        """Test string representation of implication rule"""
        condition1 = Condition("${VAR1}", "a")
        condition2 = Condition("${VAR2}", "b")
        impl_rule = ImplicationRule(condition1, condition2)
        expected = "${VAR1} == a  ==>  ${VAR2} == b"
        self.assertEqual(str(impl_rule), expected)


if __name__ == '__main__':
    unittest.main()
