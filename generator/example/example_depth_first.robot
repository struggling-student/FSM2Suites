*** Settings ***
Library         ExampleLibrary.py
Test Setup      Setup Example Environment

*** Variables ***
${VALID_USER}         user1
${INVALID_USER}       invalid_user
${VALID_ACTION}       action_success
${INVALID_ACTION}     action_fail

# ============================================================================
# TEST COVERAGE INFORMATION
# ============================================================================
#
# Covered states (3/6):
#     Authenticated
#     Start
#     Success
#
# Covered actions (5/12):
#     logout  (Authenticated -> Start)
#     perform action  (Authenticated -> Success)
#     authenticate user  (Start -> Authenticated)
#     continue working  (Success -> Authenticated)
#     logout  (Success -> Start)
#
# Uncovered states (3/6):
#     End
#     Error
#     Failed
#
# Uncovered actions (7/12):
#     perform action (Authenticated -> Error)
#     restart system (End -> Start)
#     logout (Error -> Start)
#     retry action (Error -> Authenticated)
#     exit system (Failed -> End)
#     retry authentication (Failed -> Start)
#     authenticate user (Start -> Failed)
#
# ============================================================================

*** Test Cases ***
Test 1
  Set Machine Variables  ${VALID_USER}  ${VALID_ACTION}
  authenticate user
  perform action
  continue working
  perform action
  continue working
  perform action
  continue working
  perform action
  continue working
  perform action
  continue working
  perform action
  continue working
  perform action
  continue working
  perform action
  continue working
  perform action
  continue working
  perform action

Test 2
  Set Machine Variables  ${VALID_USER}  ${VALID_ACTION}
  authenticate user
  perform action
  continue working
  perform action
  continue working
  perform action
  continue working
  perform action
  continue working
  perform action
  continue working
  perform action
  continue working
  perform action
  continue working
  perform action
  continue working
  perform action
  continue working
  logout

Test 3
  Set Machine Variables  ${VALID_USER}  ${VALID_ACTION}
  authenticate user
  perform action
  continue working
  perform action
  continue working
  perform action
  continue working
  perform action
  continue working
  perform action
  continue working
  perform action
  continue working
  perform action
  continue working
  perform action
  continue working
  perform action
  logout
  authenticate user

Test 4
  Set Machine Variables  ${VALID_USER}  ${VALID_ACTION}
  authenticate user
  perform action
  continue working
  perform action
  continue working
  perform action
  continue working
  perform action
  continue working
  perform action
  continue working
  perform action
  continue working
  perform action
  continue working
  perform action
  continue working
  logout
  authenticate user
  perform action

Test 5
  Set Machine Variables  ${VALID_USER}  ${VALID_ACTION}
  authenticate user
  perform action
  continue working
  perform action
  continue working
  perform action
  continue working
  perform action
  continue working
  perform action
  continue working
  perform action
  continue working
  perform action
  continue working
  perform action
  continue working
  logout
  authenticate user
  logout

Test 6
  Set Machine Variables  ${VALID_USER}  ${VALID_ACTION}
  authenticate user
  perform action
  continue working
  perform action
  continue working
  perform action
  continue working
  perform action
  continue working
  perform action
  continue working
  perform action
  continue working
  perform action
  continue working
  perform action
  logout
  authenticate user
  perform action
  continue working

Test 7
  Set Machine Variables  ${VALID_USER}  ${VALID_ACTION}
  authenticate user
  perform action
  continue working
  perform action
  continue working
  perform action
  continue working
  perform action
  continue working
  perform action
  continue working
  perform action
  continue working
  perform action
  continue working
  perform action
  logout
  authenticate user
  perform action
  logout

Test 8
  Set Machine Variables  ${VALID_USER}  ${VALID_ACTION}
  authenticate user
  perform action
  continue working
  perform action
  continue working
  perform action
  continue working
  perform action
  continue working
  perform action
  continue working
  perform action
  continue working
  perform action
  continue working
  perform action
  logout
  authenticate user
  logout
  authenticate user

Test 9
  Set Machine Variables  ${VALID_USER}  ${VALID_ACTION}
  authenticate user
  perform action
  continue working
  perform action
  continue working
  perform action
  continue working
  perform action
  continue working
  perform action
  continue working
  perform action
  continue working
  perform action
  continue working
  logout
  authenticate user
  perform action
  continue working
  perform action

Test 10
  Set Machine Variables  ${VALID_USER}  ${VALID_ACTION}
  authenticate user
  perform action
  continue working
  perform action
  continue working
  perform action
  continue working
  perform action
  continue working
  perform action
  continue working
  perform action
  continue working
  perform action
  continue working
  logout
  authenticate user
  perform action
  continue working
  logout

Test 11
  Set Machine Variables  ${VALID_USER}  ${VALID_ACTION}
  authenticate user
  perform action
  continue working
  perform action
  continue working
  perform action
  continue working
  perform action
  continue working
  perform action
  continue working
  perform action
  continue working
  perform action
  continue working
  logout
  authenticate user
  perform action
  logout
  authenticate user

Test 12
  Set Machine Variables  ${VALID_USER}  ${VALID_ACTION}
  authenticate user
  perform action
  continue working
  perform action
  continue working
  perform action
  continue working
  perform action
  continue working
  perform action
  continue working
  perform action
  continue working
  perform action
  continue working
  logout
  authenticate user
  logout
  authenticate user
  perform action

Test 13
  Set Machine Variables  ${VALID_USER}  ${VALID_ACTION}
  authenticate user
  perform action
  continue working
  perform action
  continue working
  perform action
  continue working
  perform action
  continue working
  perform action
  continue working
  perform action
  continue working
  perform action
  continue working
  logout
  authenticate user
  logout
  authenticate user
  logout

Test 14
  Set Machine Variables  ${VALID_USER}  ${VALID_ACTION}
  authenticate user
  perform action
  continue working
  perform action
  continue working
  perform action
  continue working
  perform action
  continue working
  perform action
  continue working
  perform action
  continue working
  perform action
  logout
  authenticate user
  perform action
  continue working
  perform action
  continue working

Test 15
  Set Machine Variables  ${VALID_USER}  ${VALID_ACTION}
  authenticate user
  perform action
  continue working
  perform action
  continue working
  perform action
  continue working
  perform action
  continue working
  perform action
  continue working
  perform action
  continue working
  perform action
  logout
  authenticate user
  perform action
  continue working
  perform action
  logout

Test 16
  Set Machine Variables  ${VALID_USER}  ${VALID_ACTION}
  authenticate user
  perform action
  continue working
  perform action
  continue working
  perform action
  continue working
  perform action
  continue working
  perform action
  continue working
  perform action
  continue working
  perform action
  logout
  authenticate user
  perform action
  continue working
  logout
  authenticate user

Test 17
  Set Machine Variables  ${VALID_USER}  ${VALID_ACTION}
  authenticate user
  perform action
  continue working
  perform action
  continue working
  perform action
  continue working
  perform action
  continue working
  perform action
  continue working
  perform action
  continue working
  perform action
  logout
  authenticate user
  perform action
  logout
  authenticate user
  perform action

Test 18
  Set Machine Variables  ${VALID_USER}  ${VALID_ACTION}
  authenticate user
  perform action
  continue working
  perform action
  continue working
  perform action
  continue working
  perform action
  continue working
  perform action
  continue working
  perform action
  continue working
  perform action
  logout
  authenticate user
  perform action
  logout
  authenticate user
  logout

Test 19
  Set Machine Variables  ${VALID_USER}  ${VALID_ACTION}
  authenticate user
  perform action
  continue working
  perform action
  continue working
  perform action
  continue working
  perform action
  continue working
  perform action
  continue working
  perform action
  continue working
  perform action
  logout
  authenticate user
  logout
  authenticate user
  perform action
  continue working

Test 20
  Set Machine Variables  ${VALID_USER}  ${VALID_ACTION}
  authenticate user
  perform action
  continue working
  perform action
  continue working
  perform action
  continue working
  perform action
  continue working
  perform action
  continue working
  perform action
  continue working
  perform action
  logout
  authenticate user
  logout
  authenticate user
  perform action
  logout

Test 21
  Set Machine Variables  ${VALID_USER}  ${VALID_ACTION}
  authenticate user
  perform action
  continue working
  perform action
  continue working
  perform action
  continue working
  perform action
  continue working
  perform action
  continue working
  perform action
  continue working
  perform action
  logout
  authenticate user
  logout
  authenticate user
  logout
  authenticate user

Test 22
  Set Machine Variables  ${VALID_USER}  ${VALID_ACTION}
  authenticate user
  perform action
  continue working
  perform action
  continue working
  perform action
  continue working
  perform action
  continue working
  perform action
  continue working
  perform action
  continue working
  logout
  authenticate user
  perform action
  continue working
  perform action
  continue working
  perform action

Test 23
  Set Machine Variables  ${VALID_USER}  ${VALID_ACTION}
  authenticate user
  perform action
  continue working
  perform action
  continue working
  perform action
  continue working
  perform action
  continue working
  perform action
  continue working
  perform action
  continue working
  logout
  authenticate user
  perform action
  continue working
  perform action
  continue working
  logout

Test 24
  Set Machine Variables  ${VALID_USER}  ${VALID_ACTION}
  authenticate user
  perform action
  continue working
  perform action
  continue working
  perform action
  continue working
  perform action
  continue working
  perform action
  continue working
  perform action
  continue working
  logout
  authenticate user
  perform action
  continue working
  perform action
  logout
  authenticate user

Test 25
  Set Machine Variables  ${VALID_USER}  ${VALID_ACTION}
  authenticate user
  perform action
  continue working
  perform action
  continue working
  perform action
  continue working
  perform action
  continue working
  perform action
  continue working
  perform action
  continue working
  logout
  authenticate user
  perform action
  continue working
  logout
  authenticate user
  perform action

Test 26
  Set Machine Variables  ${VALID_USER}  ${VALID_ACTION}
  authenticate user
  perform action
  continue working
  perform action
  continue working
  perform action
  continue working
  perform action
  continue working
  perform action
  continue working
  perform action
  continue working
  logout
  authenticate user
  perform action
  continue working
  logout
  authenticate user
  logout

Test 27
  Set Machine Variables  ${VALID_USER}  ${VALID_ACTION}
  authenticate user
  perform action
  continue working
  perform action
  continue working
  perform action
  continue working
  perform action
  continue working
  perform action
  continue working
  perform action
  continue working
  logout
  authenticate user
  perform action
  logout
  authenticate user
  perform action
  continue working

Test 28
  Set Machine Variables  ${VALID_USER}  ${VALID_ACTION}
  authenticate user
  perform action
  continue working
  perform action
  continue working
  perform action
  continue working
  perform action
  continue working
  perform action
  continue working
  perform action
  continue working
  logout
  authenticate user
  perform action
  logout
  authenticate user
  perform action
  logout

Test 29
  Set Machine Variables  ${VALID_USER}  ${VALID_ACTION}
  authenticate user
  perform action
  continue working
  perform action
  continue working
  perform action
  continue working
  perform action
  continue working
  perform action
  continue working
  perform action
  continue working
  logout
  authenticate user
  perform action
  logout
  authenticate user
  logout
  authenticate user

Test 30
  Set Machine Variables  ${VALID_USER}  ${VALID_ACTION}
  authenticate user
  perform action
  continue working
  perform action
  continue working
  perform action
  continue working
  perform action
  continue working
  perform action
  continue working
  perform action
  continue working
  logout
  authenticate user
  logout
  authenticate user
  perform action
  continue working
  perform action

Test 31
  Set Machine Variables  ${VALID_USER}  ${VALID_ACTION}
  authenticate user
  perform action
  continue working
  perform action
  continue working
  perform action
  continue working
  perform action
  continue working
  perform action
  continue working
  perform action
  continue working
  logout
  authenticate user
  logout
  authenticate user
  perform action
  continue working
  logout

Test 32
  Set Machine Variables  ${VALID_USER}  ${VALID_ACTION}
  authenticate user
  perform action
  continue working
  perform action
  continue working
  perform action
  continue working
  perform action
  continue working
  perform action
  continue working
  perform action
  continue working
  logout
  authenticate user
  logout
  authenticate user
  perform action
  logout
  authenticate user

Test 33
  Set Machine Variables  ${VALID_USER}  ${VALID_ACTION}
  authenticate user
  perform action
  continue working
  perform action
  continue working
  perform action
  continue working
  perform action
  continue working
  perform action
  continue working
  perform action
  continue working
  logout
  authenticate user
  logout
  authenticate user
  logout
  authenticate user
  perform action

Test 34
  Set Machine Variables  ${VALID_USER}  ${VALID_ACTION}
  authenticate user
  perform action
  continue working
  perform action
  continue working
  perform action
  continue working
  perform action
  continue working
  perform action
  continue working
  perform action
  continue working
  logout
  authenticate user
  logout
  authenticate user
  logout
  authenticate user
  logout

Test 35
  Set Machine Variables  ${VALID_USER}  ${VALID_ACTION}
  authenticate user
  perform action
  continue working
  perform action
  continue working
  perform action
  continue working
  perform action
  continue working
  perform action
  continue working
  perform action
  logout
  authenticate user
  perform action
  continue working
  perform action
  continue working
  perform action
  continue working

Test 36
  Set Machine Variables  ${VALID_USER}  ${VALID_ACTION}
  authenticate user
  perform action
  continue working
  perform action
  continue working
  perform action
  continue working
  perform action
  continue working
  perform action
  continue working
  perform action
  logout
  authenticate user
  perform action
  continue working
  perform action
  continue working
  perform action
  logout

Test 37
  Set Machine Variables  ${VALID_USER}  ${VALID_ACTION}
  authenticate user
  perform action
  continue working
  perform action
  continue working
  perform action
  continue working
  perform action
  continue working
  perform action
  continue working
  perform action
  logout
  authenticate user
  perform action
  continue working
  perform action
  continue working
  logout
  authenticate user

Test 38
  Set Machine Variables  ${VALID_USER}  ${VALID_ACTION}
  authenticate user
  perform action
  continue working
  perform action
  continue working
  perform action
  continue working
  perform action
  continue working
  perform action
  continue working
  perform action
  logout
  authenticate user
  perform action
  continue working
  perform action
  logout
  authenticate user
  perform action

Test 39
  Set Machine Variables  ${VALID_USER}  ${VALID_ACTION}
  authenticate user
  perform action
  continue working
  perform action
  continue working
  perform action
  continue working
  perform action
  continue working
  perform action
  continue working
  perform action
  logout
  authenticate user
  perform action
  continue working
  perform action
  logout
  authenticate user
  logout

Test 40
  Set Machine Variables  ${VALID_USER}  ${VALID_ACTION}
  authenticate user
  perform action
  continue working
  perform action
  continue working
  perform action
  continue working
  perform action
  continue working
  perform action
  continue working
  perform action
  logout
  authenticate user
  perform action
  continue working
  logout
  authenticate user
  perform action
  continue working

Test 41
  Set Machine Variables  ${VALID_USER}  ${VALID_ACTION}
  authenticate user
  perform action
  continue working
  perform action
  continue working
  perform action
  continue working
  perform action
  continue working
  perform action
  continue working
  perform action
  logout
  authenticate user
  perform action
  continue working
  logout
  authenticate user
  perform action
  logout

Test 42
  Set Machine Variables  ${VALID_USER}  ${VALID_ACTION}
  authenticate user
  perform action
  continue working
  perform action
  continue working
  perform action
  continue working
  perform action
  continue working
  perform action
  continue working
  perform action
  logout
  authenticate user
  perform action
  continue working
  logout
  authenticate user
  logout
  authenticate user

Test 43
  Set Machine Variables  ${VALID_USER}  ${VALID_ACTION}
  authenticate user
  perform action
  continue working
  perform action
  continue working
  perform action
  continue working
  perform action
  continue working
  perform action
  continue working
  perform action
  logout
  authenticate user
  perform action
  logout
  authenticate user
  perform action
  continue working
  perform action

Test 44
  Set Machine Variables  ${VALID_USER}  ${VALID_ACTION}
  authenticate user
  perform action
  continue working
  perform action
  continue working
  perform action
  continue working
  perform action
  continue working
  perform action
  continue working
  perform action
  logout
  authenticate user
  perform action
  logout
  authenticate user
  perform action
  continue working
  logout

Test 45
  Set Machine Variables  ${VALID_USER}  ${VALID_ACTION}
  authenticate user
  perform action
  continue working
  perform action
  continue working
  perform action
  continue working
  perform action
  continue working
  perform action
  continue working
  perform action
  logout
  authenticate user
  perform action
  logout
  authenticate user
  perform action
  logout
  authenticate user

Test 46
  Set Machine Variables  ${VALID_USER}  ${VALID_ACTION}
  authenticate user
  perform action
  continue working
  perform action
  continue working
  perform action
  continue working
  perform action
  continue working
  perform action
  continue working
  perform action
  logout
  authenticate user
  perform action
  logout
  authenticate user
  logout
  authenticate user
  perform action

Test 47
  Set Machine Variables  ${VALID_USER}  ${VALID_ACTION}
  authenticate user
  perform action
  continue working
  perform action
  continue working
  perform action
  continue working
  perform action
  continue working
  perform action
  continue working
  perform action
  logout
  authenticate user
  perform action
  logout
  authenticate user
  logout
  authenticate user
  logout

Test 48
  Set Machine Variables  ${VALID_USER}  ${VALID_ACTION}
  authenticate user
  perform action
  continue working
  perform action
  continue working
  perform action
  continue working
  perform action
  continue working
  perform action
  continue working
  perform action
  logout
  authenticate user
  logout
  authenticate user
  perform action
  continue working
  perform action
  continue working

Test 49
  Set Machine Variables  ${VALID_USER}  ${VALID_ACTION}
  authenticate user
  perform action
  continue working
  perform action
  continue working
  perform action
  continue working
  perform action
  continue working
  perform action
  continue working
  perform action
  logout
  authenticate user
  logout
  authenticate user
  perform action
  continue working
  perform action
  logout

Test 50
  Set Machine Variables  ${VALID_USER}  ${VALID_ACTION}
  authenticate user
  perform action
  continue working
  perform action
  continue working
  perform action
  continue working
  perform action
  continue working
  perform action
  continue working
  perform action
  logout
  authenticate user
  logout
  authenticate user
  perform action
  continue working
  logout
  authenticate user

*** Keywords ***
Set Machine Variables
  [Arguments]  ${USER}  ${ACTION}
  Set Test Variable  \${USER}
  Set Test Variable  \${ACTION}
