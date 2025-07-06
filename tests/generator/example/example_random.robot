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
# Covered actions (10/12):
#     logout  (Authenticated -> Start)
#     perform action  (Authenticated -> Error)
#     perform action  (Authenticated -> Success)
#     logout  (Error -> Start)
#     retry action  (Error -> Authenticated)
#     exit system  (Failed -> End)
#     retry authentication  (Failed -> Start)
#     authenticate user  (Start -> Failed)
#     authenticate user  (Start -> Authenticated)
#     continue working  (Success -> Authenticated)
#
# Uncovered actions (2/12):
#     restart system (End -> Start)
#     logout (Success -> Start)
#
# ============================================================================

*** Test Cases ***
Test 1
  Set Machine Variables  ${VALID_USER}  ${INVALID_ACTION}
  authenticate user
  perform action
  logout
  authenticate user
  perform action
  retry action

Test 2
  Set Machine Variables  ${VALID_USER}  ${VALID_ACTION}
  authenticate user
  logout
  authenticate user
  perform action
  continue working
  logout

Test 3
  Set Machine Variables  ${VALID_USER}  ${VALID_ACTION}
  authenticate user
  logout
  authenticate user
  logout
  authenticate user
  logout

Test 4
  Set Machine Variables  ${VALID_USER}  ${VALID_ACTION}
  authenticate user
  perform action
  continue working
  perform action
  continue working
  perform action

Test 5
  Set Machine Variables  ${INVALID_USER}  ${VALID_ACTION}
  authenticate user
  retry authentication
  authenticate user
  retry authentication
  authenticate user
  exit system

*** Keywords ***
Set Machine Variables
  [Arguments]  ${USER}  ${ACTION}
  Set Test Variable  \${USER}
  Set Test Variable  \${ACTION}
