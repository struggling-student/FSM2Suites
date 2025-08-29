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
#     authenticate user  (Start -> Authenticated)
#     continue working  (Success -> Authenticated)
#     logout  (Success -> Start)
#     logout  (Authenticated -> Start)
#     perform action  (Authenticated -> Success)
#
# Uncovered states (3/6):
#     End
#     Error
#     Failed
#
# Uncovered actions (7/12):
#     authenticate user (Start -> Failed)
#     exit system (Failed -> End)
#     logout (Error -> Start)
#     perform action (Authenticated -> Error)
#     restart system (End -> Start)
#     retry action (Error -> Authenticated)
#     retry authentication (Failed -> Start)
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
  Set Machine Variables  ${VALID_USER}  ${VALID_ACTION}
  authenticate user
  perform action
  continue working

Test 2
  Set Machine Variables  ${VALID_USER}  ${VALID_ACTION}
  authenticate user
  perform action
  logout

Test 3
  Set Machine Variables  ${VALID_USER}  ${VALID_ACTION}
  authenticate user
  logout
  authenticate user

Test 4
  Set Machine Variables  ${VALID_USER}  ${VALID_ACTION}
  authenticate user
  perform action
  continue working
  perform action
  continue working

Test 5
  Set Machine Variables  ${VALID_USER}  ${VALID_ACTION}
  authenticate user
  perform action
  continue working
  perform action
  logout

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
