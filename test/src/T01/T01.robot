*** Settings ***
Library         Keyword.py
Test Setup      Setup Test Environment


*** Variables ***
${TRIP_NAME}           Test Trip
${USER_TYPE}           organizer


*** Test Cases ***
Test 1
  Set Machine Variables  Test Trip  organizer
  create trip
  Draft
  publish trip
  Published
  cancel trip
  Canceled

Test 2
  Set Machine Variables  Test Trip  participant
  create trip
  Draft
  publish trip
  Published
  cancel trip
  Canceled

Test 3
  Set Machine Variables  Business Trip  organizer
  create trip
  Draft
  publish trip
  Published
  cancel trip
  Canceled

Test 4
  Set Machine Variables  Business Trip  participant
  create trip
  Draft
  publish trip
  Published
  cancel trip
  Canceled

*** Keywords ***

create trip
  [Documentation]    Create a new trip in draft state
  create new trip via api
  verify trip created

publish trip
  [Documentation]    Publish the trip making it read-only
  publish trip api call
  verify trip status    Published

cancel trip
  [Documentation]    Cancel a published trip
  cancel trip api call
  verify trip status    Canceled
Set Machine Variables
  [Arguments]  ${TRIP_NAME}  ${USER_TYPE}
  Set Test Variable  \${TRIP_NAME}
  Set Test Variable  \${USER_TYPE}
Draft
  assert trip state is      Draft
Published
  assert trip state is      Published
Canceled
  assert trip state is      Canceled
