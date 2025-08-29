# ============================================================================
# TEST COVERAGE INFORMATION
# ============================================================================
#
# Covered states (5/6):
#     Authenticated
#     End
#     Error
#     Failed
#     Start
#
# Covered actions (9/12):
#     authenticate user  (Start -> Failed)
#     authenticate user  (Start -> Authenticated)
#     exit system  (Failed -> End)
#     logout  (Error -> Start)
#     logout  (Authenticated -> Start)
#     perform action  (Authenticated -> Error)
#     restart system  (End -> Start)
#     retry action  (Error -> Authenticated)
#     retry authentication  (Failed -> Start)
#
# Uncovered states (1/6):
#     Success
#
# Uncovered actions (3/12):
#     continue working (Success -> Authenticated)
#     logout (Success -> Start)
#     perform action (Authenticated -> Success)
#
# ============================================================================

*** Settings ***
Library         ../ExampleLibrary.py
Test Setup      Setup Example Environment


*** Variables ***
${VALID_USER}         user1
${INVALID_USER}       invalid_user
${VALID_ACTION}       action_success
${INVALID_ACTION}     action_fail


*** Test Cases ***
Test 1
  Set Machine Variables  ${VALID_USER}  ${INVALID_ACTION}
  authenticate user
  logout
  authenticate user
  perform action
  retry action

Test 2
  Set Machine Variables  ${INVALID_USER}  ${INVALID_ACTION}
  authenticate user
  exit system
  restart system
  authenticate user
  retry authentication

Test 3
  Set Machine Variables  ${INVALID_USER}  ${INVALID_ACTION}
  authenticate user
  exit system
  restart system
  authenticate user
  exit system

Test 4
  Set Machine Variables  ${VALID_USER}  ${INVALID_ACTION}
  authenticate user
  perform action
  logout
  authenticate user
  perform action

Test 5
  Set Machine Variables  ${INVALID_USER}  ${VALID_ACTION}
  authenticate user
  retry authentication
  authenticate user
  retry authentication
  authenticate user

*** Keywords ***

Setup Example Environment
    Log    Setting up example environment

Authenticate User
    Log    Authenticating user: ${USER}

Perform Action
    Log    Performing action: ${ACTION}

Logout
    Log    User logging out

Retry Authentication
    Log    Retrying authentication

Exit System
    Log    Exiting system

Continue Working
    Log    Continuing work

Retry Action
    Log    Retrying action

Restart System
    Log    Restarting system
Set Machine Variables
  [Arguments]  ${USER}  ${ACTION}
  Set Test Variable  \${USER}
  Set Test Variable  \${ACTION}
