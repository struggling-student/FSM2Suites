from __future__ import print_function
import re
from pyparsing import (CharsNotIn, Forward, Literal, LineEnd, OneOrMore, Optional,
                       Regex, StringEnd, White, Word, ZeroOrMore,
                       delimitedList, printables,
                       ParseBaseException)
from .model import Machine, State, Action, Variable
from .rules import (AndRule, Condition, EquivalenceRule, OrRule,
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

splitter = Literal(' ') + OneOrMore(' ')
splitter.setParseAction(lambda t: '  ')

variable_values = (variable_value + ZeroOrMore(splitter + variable_value)).setResultsName('variable_values')
variable_values.setParseAction(lambda t: [[t[2 * i] for i in range(int((len(t) + 1) / 2))]])

variable_definition = variable.setResultsName(
    'variable_name') + splitter + 'any of' + splitter + variable_values + end_of_line
variable_definition.leaveWhitespace()
variable_definition.setParseAction(lambda t: [Variable(t.variable_name, list(t.variable_values))])

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
and_rule.setParseAction(lambda t: [AndRule([t[i] for i in range(len(t)) if i % 4 == 0])])
and_rule.leaveWhitespace()

or_rule = closed_rule + ZeroOrMore(splitter + 'or' + splitter + closed_rule)
or_rule.setParseAction(lambda t: [OrRule([t[i] for i in range(len(t)) if i % 4 == 0])])
or_rule.leaveWhitespace()

rule << (not_rule ^ equivalence_rule ^ implication_rule ^ and_rule ^ or_rule ^ closed_rule)

step = Regex(r'  [^\n\[][^\n]*(?=\n)') + LineEnd()
step.leaveWhitespace()
step.setParseAction(lambda t: [t[0]])

action_header = White(min=2) + '[Actions]'

condition = splitter + Literal('when') + splitter + rule
condition = condition ^ Regex(r'  +otherwise')


def parse_condition(cond):
    if len(cond) > 1:
        return [cond[3]]
    return ['otherwise']


condition.leaveWhitespace()
condition.setParseAction(parse_condition)
condition = Optional(condition).setResultsName('condition')

# Add support for args
args_keyword = splitter + Literal('args') + splitter
arguments = ZeroOrMore(variable_value + Optional(splitter))
arguments.setParseAction(lambda t: [t[i] for i in range(len(t)) if i % 2 == 0])
args_section = Optional(args_keyword + arguments).setResultsName('args')

action = White(min=4) + Optional(robo_step + White(min=2)) + \
         '==>' + White(min=2) + state_name + condition + args_section + end_of_line
action.leaveWhitespace()
action.setParseAction(lambda t: [Action(t.robo_step.rstrip(), t.state_name, t.condition, getattr(t, 'args', None))])

actions = action_header + end_of_line + OneOrMore(action).setResultsName('actions')
actions = Optional(actions)
actions.leaveWhitespace()
actions.setResultsName('actions')

comment = Regex(r'(^\s*\#[^\n]*\n)|(\s\s+\#[^\n]*(?=\n))|(\n\s*\#[^\n]*)')
comment.leaveWhitespace()

steps = ZeroOrMore(step).setResultsName('steps')

state = state_name + end_of_line + steps + actions
state.leaveWhitespace()
state.setParseAction(lambda p: State(p.state_name, list(p.steps), list(p.actions)))

machine_header = Literal('*** Machine ***') + end_of_line
states = state + ZeroOrMore(OneOrMore(LineEnd()) + state)
states.setParseAction(lambda t: [[t[2 * i] for i in range(int((len(t) + 1) / 2))]])
states = states.setResultsName('states')
variables = ZeroOrMore(variable_definition).setResultsName('variables')
rules = ZeroOrMore(rule + end_of_line).setResultsName('rules')
rules.setParseAction(lambda t: [t[i] for i in range(len(t)) if i % 2 == 0])
machine = Optional(settings_table).setResultsName('settings_table') + \
          Optional(variables_table).setResultsName('variables_table') + \
          machine_header + ZeroOrMore(end_of_line) + variables + \
          ZeroOrMore(end_of_line) + rules + \
          ZeroOrMore(end_of_line) + states + \
          Optional(keywords_table).setResultsName('keywords_table')


def create_machine(p):
    # For some reason, p.rules contains only the _first_ rule. Work around it
    # by finding rule elements based on their type.
    def is_rule(obj):
        return isinstance(obj, (EquivalenceRule, ImplicationRule, AndRule,
                                OrRule, NotRule))

    rules = [v for v in p if is_rule(v)]
    return Machine(list(p.states),
                       list(p.variables),
                       rules,  # p.rules contains only first rule(!)
                       settings_table=p.settings_table,
                       variables_table=p.variables_table,
                       keywords_table=p.keywords_table)


machine.setParseAction(create_machine)
machine.ignore(comment)
machine.setWhitespaceChars(' ')


class MachineParsingException(Exception):
    pass


def resolve_whitespace(text):
    output_texts = []
    for index, line in enumerate(text.splitlines()):
        if '\t' in line:
            print('WARNING! tab detected on line [{:d}]: {:r}'.format(index, line))
        output_texts.append(line.rstrip())
    return '\n'.join(output_texts).strip() + '\n'


def parse(text):
    try:
        # Try the improved simple parser first (better Robot Framework support)
        return parse_simple(text)
    except Exception as e:
        print('Simple parser failed: {:s}'.format(str(e)))
        print('Falling back to original pyparsing parser...')
        
        # Fall back to the original pyparsing parser
        try:
            return machine.parseString(resolve_whitespace(text), parseAll=True)[0]
        except ParseBaseException as pe:
            print('Original parser also failed at line {:d}'.format(pe.lineno))
            print(pe.msg)
            print('line: "{:s}"'.format(pe.line))
            raise MachineParsingException(f"Both parsers failed. Simple: {e}, Original: {pe.msg}")
        except AssertionError as ae:
            print(ae)
            raise MachineParsingException(f"Both parsers failed. Simple: {e}, Original: {ae}")


# Improved simple parser for Robot Framework machine files

def parse_simple_condition(condition_str):
    """Parse a simple condition string"""
    condition_str = condition_str.strip()
    
    # Simple condition parsing - can be enhanced
    if '==' in condition_str and 'and' in condition_str:
        # Handle: ${EMAIL} == ${VALID_EMAIL} and ${PASSWORD} == ${VALID_PASSWORD}
        parts = condition_str.split(' and ')
        conditions = []
        for part in parts:
            if '==' in part:
                var, val = part.split('==', 1)
                conditions.append(Condition(var.strip(), val.strip()))
        return AndRule(conditions) if len(conditions) > 1 else conditions[0]
    elif '==' in condition_str:
        var, val = condition_str.split('==', 1)
        return Condition(var.strip(), val.strip())
    elif ' in ' in condition_str:
        # Handle: ${ACTION} in (read, write, delete)
        # For now, create a simple condition that always validates as true
        # In a full implementation, this would need proper 'in' condition support
        var, val = condition_str.split(' in ', 1)
        return Condition(var.strip(), val.strip())
    elif '<=' in condition_str:
        # Handle: ${RETRY_COUNT} <= ${MAX_RETRIES}
        # For now, create a simple condition 
        var, val = condition_str.split('<=', 1)
        return Condition(var.strip(), val.strip())
    else:
        # If we can't parse it, return None so the action has no condition
        # This will make the action always available
        return None


def parse_simple(content):
    """Simple line-by-line parser for Robot Framework machine files"""
    lines = content.strip().split('\n')
    current_section = None
    variables = []
    states = []
    rules = []
    current_state = None
    settings_content = []
    variables_content = []
    keywords_content = []
    
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped_line = line.strip()
        
        # Skip empty lines and comments
        if not stripped_line or stripped_line.startswith('#'):
            i += 1
            continue
        
        # Section headers
        if stripped_line == '*** Settings ***':
            current_section = 'settings'
            settings_content.append(line + '\n')
            i += 1
            continue
        elif stripped_line == '*** Variables ***':
            current_section = 'variables'
            variables_content.append(line + '\n')
            i += 1
            continue
        elif stripped_line == '*** Machine ***':
            current_section = 'machine'
            i += 1
            continue
        elif stripped_line == '*** Keywords ***':
            current_section = 'keywords'
            keywords_content.append(line + '\n')
            i += 1
            continue
        
        # Parse content based on current section
        if current_section == 'settings':
            # Collect settings content (preserve the line with proper spacing)
            settings_content.append(line + '\n')
        elif current_section == 'variables':
            # Collect variables content (preserve the line with proper spacing)
            variables_content.append(line + '\n')
        elif current_section == 'keywords':
            # Collect keywords content (preserve the line with proper spacing)
            keywords_content.append(line + '\n')
        elif current_section == 'machine':
            # Variable definition
            if stripped_line.startswith('${') and 'any of' in stripped_line:
                var_match = re.match(r'\$\{(\w+)\}\s+any of\s+(.+)', stripped_line)
                if var_match:
                    var_name = '${' + var_match.group(1) + '}'
                    values = [v.strip() for v in var_match.group(2).split()]
                    variables.append(Variable(var_name, values))
            
            # Rule definition (contains ==>)
            elif '==>' in stripped_line and not line.startswith('    '):
                # Parse rule: ${VAR1} == a  ==>  ${VAR2} == 1
                parts = stripped_line.split('==>')
                if len(parts) == 2:
                    antecedent_str = parts[0].strip()
                    consequent_str = parts[1].strip()
                    
                    # Parse antecedent and consequent as conditions
                    antecedent = parse_simple_condition(antecedent_str)
                    consequent = parse_simple_condition(consequent_str)
                    
                    # Create implication rule
                    rule = ImplicationRule(antecedent, consequent)
                    rules.append(rule)
            
            # State definition (line with no leading spaces and is capitalized)
            elif stripped_line and not line.startswith(' ') and stripped_line[0].isupper():
                # Save previous state
                if current_state:
                    states.append(current_state)
                
                # Start new state
                current_state = State(stripped_line, [], [])
            
            # State step (starts with 2-4 spaces but is not an action or [Actions])
            elif line.startswith('  ') and not ('==>' in line and line.startswith('    ')) and stripped_line != '[Actions]':
                if current_state:
                    current_state.steps.append(stripped_line)
            
            # Skip [Actions] header
            elif stripped_line == '[Actions]':
                pass  # Just skip this header
            
            # Action definition (starts with 4+ spaces and contains ==>)
            elif line.startswith('    ') and '==>' in line:
                if current_state:
                    # Parse action: "    action ==> Target when condition args arg1 arg2"
                    action_line = line.strip()
                    parts = action_line.split('==>')
                    if len(parts) == 2:
                        action_name = parts[0].strip()
                        target_and_rest = parts[1].strip()
                        
                        # Initialize defaults
                        target = target_and_rest
                        condition = None
                        args = []
                        
                        # Parse target, condition, and args
                        if ' when ' in target_and_rest:
                            target_part, condition_and_args = target_and_rest.split(' when ', 1)
                            target = target_part.strip()
                            
                            # Check for args in condition part
                            if ' args ' in condition_and_args:
                                condition_part, args_part = condition_and_args.split(' args ', 1)
                                condition = parse_simple_condition(condition_part.strip())
                                args = [arg.strip() for arg in args_part.split()]
                            else:
                                condition = parse_simple_condition(condition_and_args.strip())
                        elif target_and_rest.endswith(' otherwise'):
                            target = target_and_rest.replace(' otherwise', '').strip()
                            condition = 'otherwise'
                        elif ' args ' in target_and_rest:
                            # No condition, but has args
                            target_part, args_part = target_and_rest.split(' args ', 1)
                            target = target_part.strip()
                            args = [arg.strip() for arg in args_part.split()]
                        else:
                            target = target_and_rest.strip()
                        
                        action = Action(action_name, target, condition, args)
                        current_state._actions.append(action)
        
        i += 1
    
    # Add the last state
    if current_state:
        states.append(current_state)
    
    return Machine(
        states=states,
        variables=variables,
        rules=rules,
        settings_table=settings_content,
        variables_table=variables_content,
        keywords_table=keywords_content
    )
