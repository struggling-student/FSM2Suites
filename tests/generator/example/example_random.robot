*** Settings ***
Library         ExampleLibrary.py
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
  logout
  authenticate user
  perform action
  logout
  authenticate user

Test 2
  Set Machine Variables  ${VALID_USER}  ${VALID_ACTION}
  authenticate user
  logout
  authenticate user
  perform action
  continue working
  logout

Test 3
  Set Machine Variables  ${INVALID_USER}  ${INVALID_ACTION}
  authenticate user
  exit system
  restart system
  authenticate user
  retry authentication
  authenticate user

Test 4
  Set Machine Variables  ${INVALID_USER}  ${VALID_ACTION}
  authenticate user
  exit system
  restart system
  authenticate user
  exit system
  restart system

*** Keywords ***
Set Machine Variables
  [Arguments]  ${USER}  ${ACTION}
  Set Test Variable  \${USER}
  Set Test Variable  \${ACTION}
