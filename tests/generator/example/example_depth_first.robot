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

Test 2
  Set Machine Variables  ${VALID_USER}  ${VALID_ACTION}
  authenticate user
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
  logout
  authenticate user

Test 4
  Set Machine Variables  ${VALID_USER}  ${VALID_ACTION}
  authenticate user
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
  logout
  authenticate user
  logout

*** Keywords ***
Set Machine Variables
  [Arguments]  ${USER}  ${ACTION}
  Set Test Variable  \${USER}
  Set Test Variable  \${ACTION}
