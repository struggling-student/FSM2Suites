# Machine File Grammar Documentation

This document provides a comprehensive guide to the `.machine` file format used by the test generation framework. The machine file format defines finite state machines that can be used to generate automated tests.

## Table of Contents

1. [Overview](#overview)
2. [File Structure](#file-structure)
3. [Grammar Specification](#grammar-specification)
4. [Sections](#sections)
5. [Syntax Rules](#syntax-rules)
6. [Variables](#variables)
7. [States and Actions](#states-and-actions)
8. [Rules and Constraints](#rules-and-constraints)
9. [Examples](#examples)
10. [Best Practices](#best-practices)
11. [Troubleshooting](#troubleshooting)

## Overview

A `.machine` file defines a finite state machine (FSM) using a structured format similar to Robot Framework syntax. The file describes:

- **Variables**: Parameters that can have different values during test execution
- **States**: Different conditions or stages in the system
- **Actions**: Operations that can be performed to transition between states
- **Rules**: Conditions that govern when transitions can occur

## File Structure

Every machine file follows this basic structure:

```
*** Variables ***
<variable definitions>

*** Machine ***
<state definitions and transitions>

*** Keywords *** (optional)
<keyword implementations>
```

## Grammar Specification

### EBNF Grammar

```ebnf
machine_file ::= variable_section machine_section keyword_section?

variable_section ::= "*** Variables ***" newline variable_definition*
variable_definition ::= variable_name whitespace variable_values newline
variable_name ::= "${" identifier "}"
variable_values ::= value (whitespace value)*
value ::= "${" identifier "}" | string

machine_section ::= "*** Machine ***" newline state_definition*
state_definition ::= state_name newline action_definition*
state_name ::= identifier ":"?
action_definition ::= whitespace action_name (whitespace condition)? newline transition*
action_name ::= identifier (whitespace identifier)*
condition ::= "(" expression ")"
transition ::= whitespace+ target_state newline
target_state ::= identifier

keyword_section ::= "*** Keywords ***" newline keyword_definition*
keyword_definition ::= keyword_name newline implementation*
keyword_name ::= identifier (whitespace identifier)*
implementation ::= whitespace+ statement newline

expression ::= variable comparison_op value | logical_expression
comparison_op ::= "==" | "!=" | "<" | ">" | "<=" | ">="
logical_expression ::= expression ("and" | "or") expression

identifier ::= letter (letter | digit | "_")*
string ::= quoted_string | unquoted_string
whitespace ::= " " | "\t"
newline ::= "\n" | "\r\n"
```

### Syntax Elements

#### Comments
```
# This is a comment - lines starting with # are ignored
```

#### Variable References
```
${VARIABLE_NAME}    # Reference to a variable
```

#### State Names
```
StateName           # Simple state name
State Name          # State name with spaces
```

#### Action Names
```
action name         # Action with spaces
single_action       # Single word action
perform complex action  # Multi-word action
```

## Sections

### 1. Variables Section

The Variables section defines parameters that can have different values during test execution.

```
*** Variables ***
${USER}          ${VALID_USER}    ${INVALID_USER}
${ACTION}        ${VALID_ACTION}  ${INVALID_ACTION}
${TIMEOUT}       30              60              120
```

#### Syntax Rules:
- Section starts with `*** Variables ***`
- Each variable is defined on a separate line
- Variable names must be enclosed in `${}`
- Values are separated by whitespace
- Values can be variable references (`${OTHER_VAR}`) or literals

#### Variable Types:
1. **String Variables**: Text values
2. **Numeric Variables**: Integer or decimal numbers
3. **Boolean Variables**: True/False values
4. **Reference Variables**: References to other variables

### 2. Machine Section

The Machine section defines the state machine structure, including states, actions, and transitions.

```
*** Machine ***
Start
    authenticate user (${USER} == ${VALID_USER})
        Authenticated
    authenticate user (${USER} == ${INVALID_USER})
        Failed

Authenticated
    perform action (${ACTION} == ${VALID_ACTION})
        Success
    perform action (${ACTION} == ${INVALID_ACTION})
        Error
    logout
        Start
```

#### Structure:
1. **State Definition**: State name followed by a colon (optional) or newline
2. **Action Definition**: Indented action name with optional condition
3. **Transition Definition**: Further indented target state

#### Indentation Rules:
- States: No indentation (column 0)
- Actions: 4 spaces or 1 tab
- Target states: 8 spaces or 2 tabs
- Consistent indentation within a file is required

### 3. Keywords Section (Optional)

The Keywords section can define implementations for actions, primarily for documentation or Robot Framework integration.

```
*** Keywords ***
authenticate user
    Log    Authenticating user: ${USER}
    Set Global Variable    ${CURRENT_USER}    ${USER}

perform action
    Log    Performing action: ${ACTION}
    Run Keyword If    '${ACTION}' == '${VALID_ACTION}'    Valid Action Steps
    Run Keyword If    '${ACTION}' == '${INVALID_ACTION}'    Invalid Action Steps
```

## Syntax Rules

### Naming Conventions

1. **Variable Names**:
   - Must be enclosed in `${}`
   - Use UPPERCASE for constants: `${VALID_USER}`
   - Use descriptive names: `${USER_TYPE}` instead of `${UT}`

2. **State Names**:
   - Use PascalCase: `Authenticated`, `UserLoggedIn`
   - Can contain spaces: `User Logged In`
   - Should be descriptive and meaningful

3. **Action Names**:
   - Use lowercase with spaces: `authenticate user`
   - Use verb phrases: `perform action`, `validate input`
   - Should describe what the action does

### Conditions

Conditions control when actions can be performed:

```
action name (${VARIABLE} == ${VALUE})
    TargetState

action name (${USER} == ${VALID_USER} and ${STATUS} == ${ACTIVE})
    TargetState
```

#### Supported Operators:
- `==` : Equal to
- `!=` : Not equal to
- `<`  : Less than
- `>`  : Greater than
- `<=` : Less than or equal
- `>=` : Greater than or equal

#### Logical Operators:
- `and` : Both conditions must be true
- `or`  : Either condition must be true

### Multiple Transitions

An action can lead to different states based on conditions:

```
validate input (${INPUT} == ${VALID})
    Success
validate input (${INPUT} == ${INVALID})
    Error
validate input (${INPUT} == ${EMPTY})
    Prompt
```

## Variables

### Variable Definition

Variables are defined in the Variables section and can have multiple possible values:

```
*** Variables ***
${USER_TYPE}     admin    user    guest
${STATUS}        active   inactive
${RETRY_COUNT}   1        2       3
```

### Variable Usage

Variables are used in conditions and can be referenced throughout the machine:

```
authenticate (${USER_TYPE} == admin)
    AdminDashboard
authenticate (${USER_TYPE} == user)
    UserDashboard
authenticate (${USER_TYPE} == guest)
    GuestArea
```

### Variable Scope

- Variables are global within a machine file
- Variable values are set during test generation
- Each test case uses a specific combination of variable values

## States and Actions

### State Definition

States represent different conditions or phases in your system:

```
# Simple state
Start

# State with multiple actions
Authenticated
    view dashboard
        Dashboard
    edit profile
        ProfileEdit
    logout
        Start
```

### Action Definition

Actions define operations that can be performed from a state:

```
# Simple action (always available)
logout
    Start

# Conditional action
perform action (${ACTION} == ${VALID_ACTION})
    Success

# Action with complex condition
process request (${USER} == ${ADMIN} and ${REQUEST_TYPE} == ${URGENT})
    UrgentProcessing
```

### Implicit vs Explicit Actions

1. **Implicit Actions**: Always available from a state
```
logout
    Start
```

2. **Explicit Actions**: Available only when conditions are met
```
admin action (${USER_TYPE} == admin)
    AdminPanel
```

## Rules and Constraints

### Simple Rules

Rules define when actions are available:

```
# Action only available for valid users
access secure area (${USER} == ${VALID_USER})
    SecureArea
```

### Complex Rules

Multiple conditions can be combined:

```
# Action requires both conditions
approve request (${USER_TYPE} == manager and ${REQUEST_VALUE} < 10000)
    Approved

# Action available if either condition is true
escalate (${PRIORITY} == high or ${USER_TYPE} == admin)
    Escalated
```

### Rule Evaluation

Rules are evaluated during test generation:
- If a rule evaluates to `true`, the action is available
- If a rule evaluates to `false`, the action is not available
- Actions without rules are always available

## Examples

### Simple Login System

```
*** Variables ***
${USERNAME}    valid_user    invalid_user
${PASSWORD}    correct_pass  wrong_pass

*** Machine ***
LoginPage
    enter credentials (${USERNAME} == valid_user and ${PASSWORD} == correct_pass)
        Dashboard
    enter credentials (${USERNAME} == invalid_user or ${PASSWORD} == wrong_pass)
        LoginError

Dashboard
    logout
        LoginPage

LoginError
    retry login
        LoginPage
    forgot password
        PasswordReset

PasswordReset
    reset password
        LoginPage
```

### E-commerce Workflow

```
*** Variables ***
${USER_TYPE}     guest    registered    premium
${CART_STATUS}   empty    has_items     
${PAYMENT}       valid    invalid       expired

*** Machine ***
Homepage
    browse products
        ProductCatalog
    login (${USER_TYPE} != guest)
        UserAccount

ProductCatalog
    add to cart
        Cart
    view product details
        ProductDetails

Cart
    checkout (${CART_STATUS} == has_items)
        Checkout
    continue shopping
        ProductCatalog

Checkout
    process payment (${PAYMENT} == valid)
        OrderConfirmed
    process payment (${PAYMENT} != valid)
        PaymentError

OrderConfirmed
    view order
        OrderDetails
    continue shopping
        ProductCatalog
```

### Multi-User System

```
*** Variables ***
${USER_ROLE}     admin       user        guest
${PERMISSION}    read        write       admin
${RESOURCE}      public      private     restricted

*** Machine ***
Start
    login (${USER_ROLE} == admin)
        AdminDashboard
    login (${USER_ROLE} == user)  
        UserDashboard
    browse (${USER_ROLE} == guest)
        PublicArea

AdminDashboard
    manage users (${PERMISSION} == admin)
        UserManagement
    access reports (${PERMISSION} == admin)
        Reports
    logout
        Start

UserDashboard
    view profile
        Profile
    access resource (${RESOURCE} == public)
        PublicResource
    access resource (${RESOURCE} == private and ${PERMISSION} == write)
        PrivateResource
    logout
        Start
```

## Best Practices

### 1. State Design

- **Keep states focused**: Each state should represent a clear system condition
- **Use descriptive names**: `UserAuthenticated` instead of `State1`
- **Avoid deep nesting**: Limit the number of states to keep the model manageable

### 2. Variable Design

- **Use meaningful names**: `${USER_TYPE}` instead of `${UT}`
- **Group related values**: Put similar variable values together
- **Consider test coverage**: Ensure variable combinations provide good test coverage

### 3. Action Design

- **Use verb phrases**: `authenticate user` instead of `auth`
- **Be specific**: `submit login form` instead of `submit`
- **Keep actions atomic**: Each action should represent a single operation

### 4. Rule Design

- **Keep rules simple**: Complex rules are harder to understand and debug
- **Use meaningful conditions**: `${USER_TYPE} == admin` instead of `${UT} == 1`
- **Document complex logic**: Add comments for non-obvious rules

### 5. File Organization

```
*** Variables ***
# User-related variables
${USER_TYPE}     admin    user    guest
${USER_STATUS}   active   inactive

# System-related variables  
${SYSTEM_MODE}   normal   maintenance
${FEATURE_FLAG}  enabled  disabled

*** Machine ***
# Main workflow states
Start
    # Authentication actions
    login
        Dashboard
        
Dashboard  
    # Primary user actions
    view data
        DataView
```

## Troubleshooting

### Common Syntax Errors

1. **Missing Section Headers**
```
# ERROR: Missing *** Variables ***
${USER}    admin    user

# CORRECT:
*** Variables ***
${USER}    admin    user
```

2. **Incorrect Indentation**
```
# ERROR: Inconsistent indentation
Start
  action1
      Target1
    action2
        Target2

# CORRECT: Consistent indentation
Start
    action1
        Target1
    action2
        Target2
```

3. **Invalid Variable References**
```
# ERROR: Missing ${} around variable
action (USER == admin)
    Target

# CORRECT:
action (${USER} == admin)
    Target
```

4. **Malformed Conditions**
```
# ERROR: Missing parentheses
action ${USER} == admin
    Target

# CORRECT:
action (${USER} == admin)
    Target
```

### Parser Error Messages

Common error messages and their solutions:

- **"Expected state name"**: Check that state names are at the beginning of lines
- **"Invalid variable definition"**: Ensure variables are in `${NAME}` format
- **"Unexpected indentation"**: Verify consistent indentation (spaces vs tabs)
- **"Missing target state"**: Every action must have at least one target state

### Debugging Tips

1. **Start simple**: Begin with a basic machine and add complexity gradually
2. **Validate syntax**: Use the parser to check syntax before testing
3. **Test incrementally**: Add one state/action at a time and test
4. **Check indentation**: Use a text editor that shows whitespace characters
5. **Verify variables**: Ensure all referenced variables are defined

### Performance Considerations

- **Limit variable combinations**: Too many combinations can lead to excessive test generation
- **Avoid deep state hierarchies**: Deep nesting can impact generation performance
- **Use rules wisely**: Complex rules can slow down test generation
- **Consider strategy choice**: Some strategies work better with certain machine structures

## Machine File Validation

The parser performs several validation checks:

1. **Syntax validation**: Correct section headers, indentation, variable format
2. **Reference validation**: All referenced variables must be defined
3. **Structure validation**: States must have actions, actions must have targets
4. **Logic validation**: Conditions must be syntactically correct

Example validation output:
```
✅ Machine loaded successfully!
   States: 6
   Variables: 2
   Total actions: 12
   Conditional actions: 8
```

This comprehensive documentation should help you understand and create effective machine files for test generation.
