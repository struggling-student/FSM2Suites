"""Parser for .machine files using pyparsing grammar.

This module provides a pure pyparsing implementation for parsing
finite state machine definitions into Machine objects.
"""

from pyparsing import (CharsNotIn, Forward, Literal, LineEnd, Optional,
                       Regex, StringEnd, White, Word, ZeroOrMore,
                       delimitedList, printables,
                       ParseBaseException)
from ..core.model import Machine, State, Action, Variable
from ..core.rules import (AndRule, Condition, EquivalenceRule, OrRule,
                   NotRule, ImplicationRule, UnequalCondition,
                   GreaterThanCondition, GreaterThanOrEqualCondition,
                   LessThanCondition, LessThanOrEqualCondition,
                   RegexCondition, RegexNegatedCondition)


end_of_line = Regex(r' *\n') ^ LineEnd()

settings_table = Literal('*** Settings ***') + Regex(r'[^\*]+(?=\*)')
settings_table.setParseAction(lambda t: '\n'.join(t))
variables_table = Literal('*** Variables ***') + Regex(r'[^\*]+(?=\*)')
variables_table.setParseAction(lambda t: '\n'.join(t))
keywords_table = Literal('*** Keywords ***') + CharsNotIn('') + StringEnd()
keywords_table.setParseAction(lambda t: '\n'.join(t))

state_name = Regex(r'\w+( \w+)*')
state_name.leaveWhitespace()
state_name = state_name.setResultsName('state_name')

robo_step = Regex(r'([\w\$\{\}][ \w\$\{\}]*[\w\}]|\w)')
robo_step.leaveWhitespace()
robo_step = robo_step.setResultsName('robo_step')

variable = Regex(Variable.REGEX)

variable_value = Regex(r'[\w\$\{\}!?\-\=\_\.\/]+( [\w\$\{\}!?\-\=\_\.\/]+)*')

splitter = Regex(r'  +')
splitter.leaveWhitespace()
splitter.setParseAction(lambda t: '  ')

variable_values = (variable_value + ZeroOrMore(splitter + variable_value))
variable_values.setParseAction(lambda t: t[0::2])
variable_values.setResultsName('variable_values')

variable_definition = variable.setResultsName(
    'variable_name') + splitter + 'any of' + splitter + variable_values + end_of_line
variable_definition.leaveWhitespace()
variable_definition.setParseAction(lambda t: [Variable(t[0], [t[i] for i in range(4, len(t)-1)])])

rule = Forward()

condition_rule = variable + ' == ' + variable_value
condition_rule.setParseAction(lambda t: [Condition(t[0], t[2])])
condition_rule.leaveWhitespace()

unequal_condition_rule = variable + ' != ' + variable_value
unequal_condition_rule.setParseAction(lambda t: [UnequalCondition(t[0], t[2])])
unequal_condition_rule.leaveWhitespace()

cond_gt_rule = variable + ' > ' + variable_value
cond_gt_rule.setParseAction(lambda t: [GreaterThanCondition(t[0], t[2])])
cond_gt_rule.leaveWhitespace()

cond_ge_rule = variable + ' >= ' + variable_value
cond_ge_rule.setParseAction(lambda t: [GreaterThanOrEqualCondition(t[0], t[2])])
cond_ge_rule.leaveWhitespace()

cond_lt_rule = variable + ' < ' + variable_value
cond_lt_rule.setParseAction(lambda t: [LessThanCondition(t[0], t[2])])
cond_lt_rule.leaveWhitespace()

cond_le_rule = variable + ' <= ' + variable_value
cond_le_rule.setParseAction(lambda t: [LessThanOrEqualCondition(t[0], t[2])])
cond_le_rule.leaveWhitespace()

cond_in_rule = (variable + ' in ' + Literal('(').suppress() +
                variable_value + ZeroOrMore((Literal(',') + Optional(Literal(' '))).suppress() + variable_value) +
                Literal(')').suppress())
cond_in_rule.setParseAction(lambda t: [OrRule([Condition(t[0], t[i]) for i in range(2, len(t))])])
cond_in_rule.leaveWhitespace()

cond_regex_rule = variable + ' ~ ' + delimitedList(Word(printables), delim=' ', combine=True)
cond_regex_rule.setParseAction(lambda t: [RegexCondition(t[0], t[2])])
cond_regex_rule.leaveWhitespace()

cond_regex_neg_rule = variable + ' !~ ' + delimitedList(Word(printables), delim=' ', combine=True)
cond_regex_neg_rule.setParseAction(lambda t: [RegexNegatedCondition(t[0], t[2])])
cond_regex_neg_rule.leaveWhitespace()

closed_rule = condition_rule ^ unequal_condition_rule ^ cond_gt_rule ^ cond_ge_rule ^ cond_lt_rule ^ \
              cond_le_rule ^ cond_in_rule ^ cond_regex_rule ^ cond_regex_neg_rule ^ ('(' + rule + ')')
closed_rule.setParseAction(lambda t: [t[1]] if len(t) == 3 else t)

not_rule = Literal('not ') + closed_rule
not_rule.leaveWhitespace()
not_rule.setParseAction(lambda t: [NotRule(t[1])])

equivalence_rule = closed_rule + splitter + '<==>' + splitter + closed_rule
equivalence_rule.leaveWhitespace()
equivalence_rule.setParseAction(lambda t: [EquivalenceRule(t[0], t[4])])

implication_rule = closed_rule + splitter + '==>' + splitter + closed_rule
implication_rule.leaveWhitespace()
implication_rule.setParseAction(lambda t: [ImplicationRule(t[0], t[4])])

and_rule = closed_rule + ZeroOrMore(splitter + 'and' + splitter + closed_rule)
and_rule.setParseAction(lambda t: [AndRule([t[i] for i in range(len(t)) if i % 4 == 0])] if len(t) > 1 else [t[0]])
and_rule.leaveWhitespace()

or_rule = closed_rule + ZeroOrMore(splitter + 'or' + splitter + closed_rule)
or_rule.setParseAction(lambda t: [OrRule([t[i] for i in range(len(t)) if i % 4 == 0])] if len(t) > 1 else [t[0]])
or_rule.leaveWhitespace()

rule << (not_rule ^ equivalence_rule ^ implication_rule ^ and_rule ^ or_rule ^ closed_rule)

step = Regex(r'  [^\n\[][^\n]*(?=\n)') + LineEnd()
step.leaveWhitespace()
step.setParseAction(lambda t: t[0].strip())

action_header = White(min=2) + '[Actions]' + end_of_line

when_condition = splitter + Literal('when') + splitter + rule
when_condition.setParseAction(lambda t: t[3])

otherwise_condition = Regex(r'  +otherwise')
otherwise_condition.setParseAction(lambda t: 'otherwise')

condition = when_condition ^ otherwise_condition
condition.leaveWhitespace()
condition = Optional(condition).setResultsName('condition')

args_keyword = splitter + Literal('args').suppress() + splitter
arguments = ZeroOrMore(variable_value + Optional(splitter))
arguments.setParseAction(lambda t: [t[i] for i in range(len(t)) if i % 2 == 0])
args_section = Optional(args_keyword + arguments).setResultsName('args')

action = White(min=4) + robo_step + White(min=2) + \
         '==>' + White(min=2) + state_name + condition + args_section + end_of_line
action.leaveWhitespace()
action.setParseAction(lambda t: Action(t.robo_step.strip(), 
                                      t.state_name, 
                                      t.condition if t.condition else None, 
                                      t.args if hasattr(t, 'args') and t.args else []))

actions = action_header + ZeroOrMore(action).setResultsName('actions')
actions = Optional(actions)
actions.leaveWhitespace()
actions.setResultsName('actions')

comment = Regex(r'(^\s*\#[^\n]*\n)|(\s\s+\#[^\n]*(?=\n))|(\n\s*\#[^\n]*)')
comment.leaveWhitespace()

steps = ZeroOrMore(step).setResultsName('steps')

machine_header = Literal('*** Machine ***') + end_of_line
variables = ZeroOrMore(variable_definition).setResultsName('variables')
rules = ZeroOrMore(rule + end_of_line).setResultsName('rules')
rules.setParseAction(lambda t: [t[i] for i in range(len(t)) if i % 2 == 0])

single_state = state_name + end_of_line + steps + actions
single_state.leaveWhitespace()
single_state.setParseAction(lambda p: State(p.state_name, list(p.steps) if p.steps else [], list(p.actions) if p.actions else []))

states_section = single_state + ZeroOrMore(ZeroOrMore(LineEnd()) + single_state)
states_section.setResultsName('states')

machine = Optional(settings_table).setResultsName('settings_table') + \
          Optional(variables_table).setResultsName('variables_table') + \
          machine_header + \
          Optional(ZeroOrMore(end_of_line) + variables) + \
          Optional(ZeroOrMore(end_of_line) + rules) + \
          ZeroOrMore(end_of_line) + states_section + \
          Optional(keywords_table).setResultsName('keywords_table')


def _create_machine(p):
    def is_rule(obj):
        return isinstance(obj, (EquivalenceRule, ImplicationRule, AndRule,
                                OrRule, NotRule))

    rules = [v for v in p if is_rule(v)]
    
    from ..core.model import State
    states = [v for v in p if isinstance(v, State)]
    
    settings_table = p.settings_table if hasattr(p, 'settings_table') and p.settings_table else []
    variables_table = p.variables_table if hasattr(p, 'variables_table') and p.variables_table else []
    keywords_table = p.keywords_table if hasattr(p, 'keywords_table') and p.keywords_table else []
    
    if isinstance(settings_table, str):
        settings_table = [settings_table]
    if isinstance(variables_table, str):
        variables_table = [variables_table]
    if isinstance(keywords_table, str):
        keywords_table = [keywords_table]
    
    machine = Machine(states,
                       list(p.variables),
                       rules,
                       settings_table=settings_table,
                       variables_table=variables_table,
                       keywords_table=keywords_table)
    
    machine.validate()
    
    return machine


machine.setParseAction(_create_machine)
machine.ignore(comment)
machine.setWhitespaceChars(' ')


class MachineParsingException(Exception):
    """Exception raised when machine parsing fails."""
    pass


def _resolve_whitespace(text):
    output_texts = []
    for index, line in enumerate(text.splitlines()):
        if '\t' in line:
            print('WARNING! tab detected on line [{:d}]: {:r}'.format(index, line))
        output_texts.append(line.rstrip())
    return '\n'.join(output_texts).strip() + '\n'


def parse(text):
    """Parse machine definition text and return Machine object."""
    try:
        text = _resolve_whitespace(text)
        result = machine.parseString(text)
        return result[0]
    except ParseBaseException as pe:
        print('Parser failed at line {:d}'.format(pe.lineno))
        print(pe.msg)
        print('line: "{:s}"'.format(pe.line))
        raise MachineParsingException(f"Parsing failed: {pe.msg}")
    except Exception as ae:
        print(ae)
        raise MachineParsingException(f"Parsing failed: {ae}")



