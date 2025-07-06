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
#     perform action  (Authenticated -> Success)
#     perform action  (Authenticated -> Error)
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
  logout
  authenticate user
  perform action
  logout
  authenticate user
  perform action
  continue working

Test 2
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
  exit system
  restart system
  authenticate user
  exit system
  restart system
  authenticate user
  retry authentication
  authenticate user

Test 3
  Set Machine Variables  ${INVALID_USER}  ${INVALID_ACTION}
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

Test 4
  Set Machine Variables  ${VALID_USER}  ${INVALID_ACTION}
  authenticate user
  perform action
  retry action
  perform action
  retry action
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
  logout
  authenticate user
  perform action
  logout

*** Keywords ***
Set Machine Variables
  [Arguments]  ${USER}  ${ACTION}
  Set Test Variable  \${USER}
  Set Test Variable  \${ACTION}
