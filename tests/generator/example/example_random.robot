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
# Covered states (6/6):
#     Authenticated
#     End
#     Error
#     Failed
#     Start
#     Success
#
# Covered actions (12/12):
#     logout  (Authenticated -> Start)
#     perform action  (Authenticated -> Error)
#     perform action  (Authenticated -> Success)
#     restart system  (End -> Start)
#     logout  (Error -> Start)
#     retry action  (Error -> Authenticated)
#     exit system  (Failed -> End)
#     retry authentication  (Failed -> Start)
#     authenticate user  (Start -> Authenticated)
#     authenticate user  (Start -> Failed)
#     continue working  (Success -> Authenticated)
#     logout  (Success -> Start)
#
# ============================================================================

*** Test Cases ***
Test 1
  Set Machine Variables  ${INVALID_USER}  ${INVALID_ACTION}
  authenticate user
  retry authentication
  authenticate user
  retry authentication
  authenticate user
  exit system
  restart system
  authenticate user
  retry authentication
  authenticate user
  exit system
  restart system
  authenticate user
  exit system
  restart system
  authenticate user
  exit system
  restart system
  authenticate user
  retry authentication

Test 2
  Set Machine Variables  ${VALID_USER}  ${VALID_ACTION}
  authenticate user
  logout
  authenticate user
  logout
  authenticate user
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
  logout
  authenticate user
  perform action
  logout

Test 3
  Set Machine Variables  ${INVALID_USER}  ${INVALID_ACTION}
  authenticate user
  retry authentication
  authenticate user
  exit system
  restart system
  authenticate user
  retry authentication
  authenticate user
  exit system
  restart system
  authenticate user
  retry authentication
  authenticate user
  exit system
  restart system
  authenticate user
  retry authentication
  authenticate user
  exit system
  restart system

Test 4
  Set Machine Variables  ${INVALID_USER}  ${INVALID_ACTION}
  authenticate user
  exit system
  restart system
  authenticate user
  exit system
  restart system
  authenticate user
  exit system
  restart system
  authenticate user
  retry authentication
  authenticate user
  exit system
  restart system
  authenticate user
  exit system
  restart system
  authenticate user
  retry authentication
  authenticate user

Test 5
  Set Machine Variables  ${INVALID_USER}  ${VALID_ACTION}
  authenticate user
  exit system
  restart system
  authenticate user
  retry authentication
  authenticate user
  exit system
  restart system
  authenticate user
  exit system
  restart system
  authenticate user
  exit system
  restart system
  authenticate user
  exit system
  restart system
  authenticate user
  exit system
  restart system

Test 6
  Set Machine Variables  ${VALID_USER}  ${INVALID_ACTION}
  authenticate user
  logout
  authenticate user
  logout
  authenticate user
  perform action
  logout
  authenticate user
  perform action
  logout
  authenticate user
  logout
  authenticate user
  logout
  authenticate user
  logout
  authenticate user
  perform action
  retry action
  logout

Test 7
  Set Machine Variables  ${INVALID_USER}  ${VALID_ACTION}
  authenticate user
  retry authentication
  authenticate user
  exit system
  restart system
  authenticate user
  retry authentication
  authenticate user
  retry authentication
  authenticate user
  retry authentication
  authenticate user
  exit system
  restart system
  authenticate user
  exit system
  restart system
  authenticate user
  retry authentication
  authenticate user

Test 8
  Set Machine Variables  ${INVALID_USER}  ${INVALID_ACTION}
  authenticate user
  retry authentication
  authenticate user
  exit system
  restart system
  authenticate user
  retry authentication
  authenticate user
  exit system
  restart system
  authenticate user
  exit system
  restart system
  authenticate user
  retry authentication
  authenticate user
  exit system
  restart system
  authenticate user
  retry authentication

Test 9
  Set Machine Variables  ${VALID_USER}  ${INVALID_ACTION}
  authenticate user
  logout
  authenticate user
  perform action
  logout
  authenticate user
  logout
  authenticate user
  logout
  authenticate user
  logout
  authenticate user
  logout
  authenticate user
  logout
  authenticate user
  perform action
  retry action
  perform action
  retry action

Test 10
  Set Machine Variables  ${VALID_USER}  ${INVALID_ACTION}
  authenticate user
  logout
  authenticate user
  perform action
  retry action
  perform action
  retry action
  perform action
  retry action
  logout
  authenticate user
  logout
  authenticate user
  logout
  authenticate user
  logout
  authenticate user
  perform action
  logout
  authenticate user

Test 11
  Set Machine Variables  ${VALID_USER}  ${INVALID_ACTION}
  authenticate user
  perform action
  retry action
  logout
  authenticate user
  perform action
  logout
  authenticate user
  logout
  authenticate user
  logout
  authenticate user
  perform action
  retry action
  logout
  authenticate user
  logout
  authenticate user
  perform action
  logout

Test 12
  Set Machine Variables  ${VALID_USER}  ${VALID_ACTION}
  authenticate user
  perform action
  continue working
  logout
  authenticate user
  logout
  authenticate user
  perform action
  continue working
  logout
  authenticate user
  perform action
  logout
  authenticate user
  perform action
  continue working
  logout
  authenticate user
  perform action
  logout

Test 13
  Set Machine Variables  ${INVALID_USER}  ${VALID_ACTION}
  authenticate user
  retry authentication
  authenticate user
  retry authentication
  authenticate user
  exit system
  restart system
  authenticate user
  retry authentication
  authenticate user
  retry authentication
  authenticate user
  exit system
  restart system
  authenticate user
  retry authentication
  authenticate user
  retry authentication
  authenticate user
  retry authentication

Test 14
  Set Machine Variables  ${INVALID_USER}  ${VALID_ACTION}
  authenticate user
  retry authentication
  authenticate user
  retry authentication
  authenticate user
  exit system
  restart system
  authenticate user
  exit system
  restart system
  authenticate user
  exit system
  restart system
  authenticate user
  exit system
  restart system
  authenticate user
  retry authentication
  authenticate user
  exit system

Test 15
  Set Machine Variables  ${INVALID_USER}  ${VALID_ACTION}
  authenticate user
  retry authentication
  authenticate user
  retry authentication
  authenticate user
  retry authentication
  authenticate user
  exit system
  restart system
  authenticate user
  retry authentication
  authenticate user
  retry authentication
  authenticate user
  exit system
  restart system
  authenticate user
  exit system
  restart system
  authenticate user

Test 16
  Set Machine Variables  ${VALID_USER}  ${VALID_ACTION}
  authenticate user
  perform action
  continue working
  logout
  authenticate user
  logout
  authenticate user
  logout
  authenticate user
  logout
  authenticate user
  perform action
  continue working
  logout
  authenticate user
  logout
  authenticate user
  perform action
  continue working
  perform action

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
  logout
  authenticate user
  perform action
  continue working
  logout
  authenticate user
  perform action
  continue working
  logout
  authenticate user
  logout
  authenticate user

Test 18
  Set Machine Variables  ${VALID_USER}  ${VALID_ACTION}
  authenticate user
  logout
  authenticate user
  logout
  authenticate user
  perform action
  logout
  authenticate user
  perform action
  logout
  authenticate user
  perform action
  logout
  authenticate user
  logout
  authenticate user
  perform action
  logout
  authenticate user
  logout

Test 19
  Set Machine Variables  ${INVALID_USER}  ${VALID_ACTION}
  authenticate user
  retry authentication
  authenticate user
  retry authentication
  authenticate user
  exit system
  restart system
  authenticate user
  exit system
  restart system
  authenticate user
  exit system
  restart system
  authenticate user
  retry authentication
  authenticate user
  exit system
  restart system
  authenticate user
  exit system

Test 20
  Set Machine Variables  ${VALID_USER}  ${VALID_ACTION}
  authenticate user
  perform action
  continue working
  logout
  authenticate user
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
  continue working
  perform action
  continue working
  perform action

Test 21
  Set Machine Variables  ${VALID_USER}  ${VALID_ACTION}
  authenticate user
  perform action
  continue working
  logout
  authenticate user
  logout
  authenticate user
  perform action
  logout
  authenticate user
  logout
  authenticate user
  perform action
  logout
  authenticate user
  perform action
  continue working
  perform action
  logout
  authenticate user

Test 22
  Set Machine Variables  ${VALID_USER}  ${INVALID_ACTION}
  authenticate user
  perform action
  retry action
  perform action
  retry action
  logout
  authenticate user
  logout
  authenticate user
  logout
  authenticate user
  perform action
  retry action
  logout
  authenticate user
  logout
  authenticate user
  perform action
  retry action
  perform action

Test 23
  Set Machine Variables  ${INVALID_USER}  ${INVALID_ACTION}
  authenticate user
  retry authentication
  authenticate user
  exit system
  restart system
  authenticate user
  exit system
  restart system
  authenticate user
  exit system
  restart system
  authenticate user
  retry authentication
  authenticate user
  retry authentication
  authenticate user
  exit system
  restart system
  authenticate user
  exit system

Test 24
  Set Machine Variables  ${VALID_USER}  ${INVALID_ACTION}
  authenticate user
  logout
  authenticate user
  logout
  authenticate user
  perform action
  logout
  authenticate user
  perform action
  retry action
  perform action
  logout
  authenticate user
  perform action
  retry action
  perform action
  retry action
  logout
  authenticate user
  logout

Test 25
  Set Machine Variables  ${INVALID_USER}  ${VALID_ACTION}
  authenticate user
  retry authentication
  authenticate user
  retry authentication
  authenticate user
  exit system
  restart system
  authenticate user
  exit system
  restart system
  authenticate user
  exit system
  restart system
  authenticate user
  retry authentication
  authenticate user
  exit system
  restart system
  authenticate user
  retry authentication

Test 26
  Set Machine Variables  ${VALID_USER}  ${VALID_ACTION}
  authenticate user
  logout
  authenticate user
  logout
  authenticate user
  logout
  authenticate user
  perform action
  logout
  authenticate user
  perform action
  logout
  authenticate user
  perform action
  logout
  authenticate user
  perform action
  logout
  authenticate user
  perform action

Test 27
  Set Machine Variables  ${INVALID_USER}  ${VALID_ACTION}
  authenticate user
  retry authentication
  authenticate user
  retry authentication
  authenticate user
  retry authentication
  authenticate user
  exit system
  restart system
  authenticate user
  exit system
  restart system
  authenticate user
  exit system
  restart system
  authenticate user
  exit system
  restart system
  authenticate user
  exit system

Test 28
  Set Machine Variables  ${INVALID_USER}  ${VALID_ACTION}
  authenticate user
  retry authentication
  authenticate user
  retry authentication
  authenticate user
  exit system
  restart system
  authenticate user
  retry authentication
  authenticate user
  retry authentication
  authenticate user
  retry authentication
  authenticate user
  retry authentication
  authenticate user
  retry authentication
  authenticate user
  exit system
  restart system

Test 29
  Set Machine Variables  ${VALID_USER}  ${VALID_ACTION}
  authenticate user
  perform action
  logout
  authenticate user
  perform action
  logout
  authenticate user
  perform action
  continue working
  logout
  authenticate user
  perform action
  logout
  authenticate user
  perform action
  continue working
  perform action
  logout
  authenticate user
  logout

Test 30
  Set Machine Variables  ${INVALID_USER}  ${INVALID_ACTION}
  authenticate user
  retry authentication
  authenticate user
  exit system
  restart system
  authenticate user
  retry authentication
  authenticate user
  retry authentication
  authenticate user
  retry authentication
  authenticate user
  exit system
  restart system
  authenticate user
  retry authentication
  authenticate user
  retry authentication
  authenticate user
  retry authentication

Test 31
  Set Machine Variables  ${VALID_USER}  ${VALID_ACTION}
  authenticate user
  perform action
  continue working
  logout
  authenticate user
  perform action
  logout
  authenticate user
  logout
  authenticate user
  logout
  authenticate user
  logout
  authenticate user
  logout
  authenticate user
  logout
  authenticate user
  logout
  authenticate user

Test 32
  Set Machine Variables  ${INVALID_USER}  ${INVALID_ACTION}
  authenticate user
  exit system
  restart system
  authenticate user
  retry authentication
  authenticate user
  retry authentication
  authenticate user
  retry authentication
  authenticate user
  exit system
  restart system
  authenticate user
  exit system
  restart system
  authenticate user
  exit system
  restart system
  authenticate user
  exit system

Test 33
  Set Machine Variables  ${INVALID_USER}  ${VALID_ACTION}
  authenticate user
  retry authentication
  authenticate user
  exit system
  restart system
  authenticate user
  exit system
  restart system
  authenticate user
  exit system
  restart system
  authenticate user
  retry authentication
  authenticate user
  exit system
  restart system
  authenticate user
  retry authentication
  authenticate user
  retry authentication

Test 34
  Set Machine Variables  ${VALID_USER}  ${INVALID_ACTION}
  authenticate user
  logout
  authenticate user
  logout
  authenticate user
  perform action
  logout
  authenticate user
  logout
  authenticate user
  logout
  authenticate user
  perform action
  logout
  authenticate user
  perform action
  logout
  authenticate user
  perform action
  retry action

Test 35
  Set Machine Variables  ${INVALID_USER}  ${VALID_ACTION}
  authenticate user
  exit system
  restart system
  authenticate user
  exit system
  restart system
  authenticate user
  retry authentication
  authenticate user
  retry authentication
  authenticate user
  retry authentication
  authenticate user
  exit system
  restart system
  authenticate user
  retry authentication
  authenticate user
  exit system
  restart system

Test 36
  Set Machine Variables  ${VALID_USER}  ${INVALID_ACTION}
  authenticate user
  perform action
  retry action
  perform action
  logout
  authenticate user
  perform action
  retry action
  perform action
  logout
  authenticate user
  logout
  authenticate user
  perform action
  logout
  authenticate user
  logout
  authenticate user
  logout
  authenticate user

Test 37
  Set Machine Variables  ${VALID_USER}  ${VALID_ACTION}
  authenticate user
  logout
  authenticate user
  perform action
  logout
  authenticate user
  perform action
  logout
  authenticate user
  perform action
  continue working
  logout
  authenticate user
  logout
  authenticate user
  logout
  authenticate user
  perform action
  logout
  authenticate user

Test 38
  Set Machine Variables  ${INVALID_USER}  ${VALID_ACTION}
  authenticate user
  exit system
  restart system
  authenticate user
  retry authentication
  authenticate user
  retry authentication
  authenticate user
  retry authentication
  authenticate user
  exit system
  restart system
  authenticate user
  exit system
  restart system
  authenticate user
  retry authentication
  authenticate user
  retry authentication
  authenticate user

Test 39
  Set Machine Variables  ${INVALID_USER}  ${VALID_ACTION}
  authenticate user
  retry authentication
  authenticate user
  retry authentication
  authenticate user
  retry authentication
  authenticate user
  exit system
  restart system
  authenticate user
  retry authentication
  authenticate user
  retry authentication
  authenticate user
  exit system
  restart system
  authenticate user
  retry authentication
  authenticate user
  retry authentication

Test 40
  Set Machine Variables  ${VALID_USER}  ${VALID_ACTION}
  authenticate user
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
  continue working
  logout
  authenticate user
  logout
  authenticate user
  perform action
  logout
  authenticate user

Test 41
  Set Machine Variables  ${VALID_USER}  ${INVALID_ACTION}
  authenticate user
  logout
  authenticate user
  perform action
  logout
  authenticate user
  perform action
  logout
  authenticate user
  logout
  authenticate user
  logout
  authenticate user
  perform action
  logout
  authenticate user
  perform action
  logout
  authenticate user
  perform action

Test 42
  Set Machine Variables  ${INVALID_USER}  ${VALID_ACTION}
  authenticate user
  retry authentication
  authenticate user
  retry authentication
  authenticate user
  exit system
  restart system
  authenticate user
  exit system
  restart system
  authenticate user
  exit system
  restart system
  authenticate user
  exit system
  restart system
  authenticate user
  exit system
  restart system
  authenticate user

Test 43
  Set Machine Variables  ${INVALID_USER}  ${VALID_ACTION}
  authenticate user
  retry authentication
  authenticate user
  retry authentication
  authenticate user
  exit system
  restart system
  authenticate user
  exit system
  restart system
  authenticate user
  exit system
  restart system
  authenticate user
  exit system
  restart system
  authenticate user
  retry authentication
  authenticate user
  retry authentication

Test 44
  Set Machine Variables  ${INVALID_USER}  ${VALID_ACTION}
  authenticate user
  exit system
  restart system
  authenticate user
  retry authentication
  authenticate user
  retry authentication
  authenticate user
  retry authentication
  authenticate user
  exit system
  restart system
  authenticate user
  exit system
  restart system
  authenticate user
  retry authentication
  authenticate user
  exit system
  restart system

Test 45
  Set Machine Variables  ${INVALID_USER}  ${VALID_ACTION}
  authenticate user
  exit system
  restart system
  authenticate user
  retry authentication
  authenticate user
  retry authentication
  authenticate user
  retry authentication
  authenticate user
  retry authentication
  authenticate user
  exit system
  restart system
  authenticate user
  exit system
  restart system
  authenticate user
  exit system
  restart system

Test 46
  Set Machine Variables  ${VALID_USER}  ${VALID_ACTION}
  authenticate user
  perform action
  logout
  authenticate user
  logout
  authenticate user
  perform action
  logout
  authenticate user
  perform action
  continue working
  logout
  authenticate user
  perform action
  continue working
  perform action
  logout
  authenticate user
  perform action
  continue working

Test 47
  Set Machine Variables  ${VALID_USER}  ${INVALID_ACTION}
  authenticate user
  logout
  authenticate user
  logout
  authenticate user
  logout
  authenticate user
  logout
  authenticate user
  perform action
  retry action
  logout
  authenticate user
  logout
  authenticate user
  logout
  authenticate user
  perform action
  retry action
  perform action

Test 48
  Set Machine Variables  ${INVALID_USER}  ${INVALID_ACTION}
  authenticate user
  retry authentication
  authenticate user
  retry authentication
  authenticate user
  retry authentication
  authenticate user
  exit system
  restart system
  authenticate user
  retry authentication
  authenticate user
  retry authentication
  authenticate user
  exit system
  restart system
  authenticate user
  retry authentication
  authenticate user
  retry authentication

Test 49
  Set Machine Variables  ${VALID_USER}  ${INVALID_ACTION}
  authenticate user
  logout
  authenticate user
  logout
  authenticate user
  logout
  authenticate user
  perform action
  retry action
  perform action
  logout
  authenticate user
  logout
  authenticate user
  perform action
  retry action
  perform action
  retry action
  logout
  authenticate user

Test 50
  Set Machine Variables  ${VALID_USER}  ${INVALID_ACTION}
  authenticate user
  perform action
  logout
  authenticate user
  logout
  authenticate user
  logout
  authenticate user
  perform action
  logout
  authenticate user
  logout
  authenticate user
  perform action
  retry action
  perform action
  retry action
  logout
  authenticate user
  logout

*** Keywords ***
Set Machine Variables
  [Arguments]  ${USER}  ${ACTION}
  Set Test Variable  \${USER}
  Set Test Variable  \${ACTION}
