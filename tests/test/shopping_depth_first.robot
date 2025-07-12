# ============================================================================
# TEST COVERAGE INFORMATION
# ============================================================================
#
# Covered states (6/8):
#     Browsing
#     CartEditing
#     Checkout
#     Login
#     OrderConfirmed
#     SessionEnded
#
# Covered actions (10/17):
#     add product to cart  (Browsing -> CartEditing)
#     cancel checkout  (Checkout -> CartEditing)
#     login with credentials  (Login -> Browsing)
#     logout  (Checkout -> SessionEnded)
#     logout  (Browsing -> SessionEnded)
#     logout  (OrderConfirmed -> SessionEnded)
#     logout  (CartEditing -> SessionEnded)
#     proceed to checkout  (CartEditing -> Checkout)
#     process payment  (Checkout -> OrderConfirmed)
#     return to login  (SessionEnded -> Login)
#
# Uncovered states (2/8):
#     LoginFailed
#     PaymentFailed
#
# Uncovered actions (7/17):
#     cancel order (PaymentFailed -> CartEditing)
#     exit application (LoginFailed -> SessionEnded)
#     login with credentials (Login -> LoginFailed)
#     logout (PaymentFailed -> SessionEnded)
#     process payment (Checkout -> PaymentFailed)
#     retry payment (PaymentFailed -> Checkout)
#     try login again (LoginFailed -> Login)
#
# ============================================================================

*** Settings ***
Library         ShoppingKeywordLibrary.py    browser=chrome    headless=True
Test Setup      Setup Shopping Environment
Test Teardown   Teardown Shopping Environment

*** Variables ***
${VALID_EMAIL}         test@example.com
${VALID_PASSWORD}      password123
${INVALID_EMAIL}       invalid@test.com
${INVALID_PASSWORD}    wrongpassword

*** Test Cases ***
Test 1
  Set Machine Variables  ${VALID_EMAIL}  ${VALID_PASSWORD}  success  1  1
  login with credentials
  add product to cart  1  1
  proceed to checkout
  process payment  success
  logout
  return to login
  login with credentials
  add product to cart  1  1
  proceed to checkout
  process payment  success
  logout
  return to login
  login with credentials
  add product to cart  1  1
  proceed to checkout
  process payment  success
  logout
  return to login
  login with credentials
  add product to cart  1  1

Test 2
  Set Machine Variables  ${VALID_EMAIL}  ${VALID_PASSWORD}  success  1  1
  login with credentials
  add product to cart  1  1
  proceed to checkout
  process payment  success
  logout
  return to login
  login with credentials
  add product to cart  1  1
  proceed to checkout
  process payment  success
  logout
  return to login
  login with credentials
  add product to cart  1  1
  proceed to checkout
  process payment  success
  logout
  return to login
  login with credentials
  logout

Test 3
  Set Machine Variables  ${VALID_EMAIL}  ${VALID_PASSWORD}  success  1  1
  login with credentials
  add product to cart  1  1
  proceed to checkout
  process payment  success
  logout
  return to login
  login with credentials
  add product to cart  1  1
  proceed to checkout
  process payment  success
  logout
  return to login
  login with credentials
  add product to cart  1  1
  proceed to checkout
  cancel checkout
  proceed to checkout
  process payment  success
  logout
  return to login

Test 4
  Set Machine Variables  ${VALID_EMAIL}  ${VALID_PASSWORD}  success  1  1
  login with credentials
  add product to cart  1  1
  proceed to checkout
  process payment  success
  logout
  return to login
  login with credentials
  add product to cart  1  1
  proceed to checkout
  process payment  success
  logout
  return to login
  login with credentials
  add product to cart  1  1
  proceed to checkout
  cancel checkout
  proceed to checkout
  cancel checkout
  proceed to checkout
  process payment  success

Test 5
  Set Machine Variables  ${VALID_EMAIL}  ${VALID_PASSWORD}  success  1  1
  login with credentials
  add product to cart  1  1
  proceed to checkout
  process payment  success
  logout
  return to login
  login with credentials
  add product to cart  1  1
  proceed to checkout
  process payment  success
  logout
  return to login
  login with credentials
  add product to cart  1  1
  proceed to checkout
  cancel checkout
  proceed to checkout
  cancel checkout
  proceed to checkout
  cancel checkout

Test 6
  Set Machine Variables  ${VALID_EMAIL}  ${VALID_PASSWORD}  success  1  1
  login with credentials
  add product to cart  1  1
  proceed to checkout
  process payment  success
  logout
  return to login
  login with credentials
  add product to cart  1  1
  proceed to checkout
  process payment  success
  logout
  return to login
  login with credentials
  add product to cart  1  1
  proceed to checkout
  cancel checkout
  proceed to checkout
  cancel checkout
  proceed to checkout
  logout

Test 7
  Set Machine Variables  ${VALID_EMAIL}  ${VALID_PASSWORD}  success  1  1
  login with credentials
  add product to cart  1  1
  proceed to checkout
  process payment  success
  logout
  return to login
  login with credentials
  add product to cart  1  1
  proceed to checkout
  process payment  success
  logout
  return to login
  login with credentials
  add product to cart  1  1
  proceed to checkout
  cancel checkout
  proceed to checkout
  cancel checkout
  logout
  return to login

Test 8
  Set Machine Variables  ${VALID_EMAIL}  ${VALID_PASSWORD}  success  1  1
  login with credentials
  add product to cart  1  1
  proceed to checkout
  process payment  success
  logout
  return to login
  login with credentials
  add product to cart  1  1
  proceed to checkout
  process payment  success
  logout
  return to login
  login with credentials
  add product to cart  1  1
  proceed to checkout
  cancel checkout
  proceed to checkout
  logout
  return to login
  login with credentials

Test 9
  Set Machine Variables  ${VALID_EMAIL}  ${VALID_PASSWORD}  success  1  1
  login with credentials
  add product to cart  1  1
  proceed to checkout
  process payment  success
  logout
  return to login
  login with credentials
  add product to cart  1  1
  proceed to checkout
  process payment  success
  logout
  return to login
  login with credentials
  add product to cart  1  1
  proceed to checkout
  cancel checkout
  logout
  return to login
  login with credentials
  add product to cart  1  1

Test 10
  Set Machine Variables  ${VALID_EMAIL}  ${VALID_PASSWORD}  success  1  1
  login with credentials
  add product to cart  1  1
  proceed to checkout
  process payment  success
  logout
  return to login
  login with credentials
  add product to cart  1  1
  proceed to checkout
  process payment  success
  logout
  return to login
  login with credentials
  add product to cart  1  1
  proceed to checkout
  cancel checkout
  logout
  return to login
  login with credentials
  logout

Test 11
  Set Machine Variables  ${VALID_EMAIL}  ${VALID_PASSWORD}  success  1  1
  login with credentials
  add product to cart  1  1
  proceed to checkout
  process payment  success
  logout
  return to login
  login with credentials
  add product to cart  1  1
  proceed to checkout
  process payment  success
  logout
  return to login
  login with credentials
  add product to cart  1  1
  proceed to checkout
  logout
  return to login
  login with credentials
  add product to cart  1  1
  proceed to checkout

Test 12
  Set Machine Variables  ${VALID_EMAIL}  ${VALID_PASSWORD}  success  1  1
  login with credentials
  add product to cart  1  1
  proceed to checkout
  process payment  success
  logout
  return to login
  login with credentials
  add product to cart  1  1
  proceed to checkout
  process payment  success
  logout
  return to login
  login with credentials
  add product to cart  1  1
  proceed to checkout
  logout
  return to login
  login with credentials
  add product to cart  1  1
  logout

Test 13
  Set Machine Variables  ${VALID_EMAIL}  ${VALID_PASSWORD}  success  1  1
  login with credentials
  add product to cart  1  1
  proceed to checkout
  process payment  success
  logout
  return to login
  login with credentials
  add product to cart  1  1
  proceed to checkout
  process payment  success
  logout
  return to login
  login with credentials
  add product to cart  1  1
  proceed to checkout
  logout
  return to login
  login with credentials
  logout
  return to login

Test 14
  Set Machine Variables  ${VALID_EMAIL}  ${VALID_PASSWORD}  success  1  1
  login with credentials
  add product to cart  1  1
  proceed to checkout
  process payment  success
  logout
  return to login
  login with credentials
  add product to cart  1  1
  proceed to checkout
  process payment  success
  logout
  return to login
  login with credentials
  add product to cart  1  1
  logout
  return to login
  login with credentials
  add product to cart  1  1
  proceed to checkout
  process payment  success

Test 15
  Set Machine Variables  ${VALID_EMAIL}  ${VALID_PASSWORD}  success  1  1
  login with credentials
  add product to cart  1  1
  proceed to checkout
  process payment  success
  logout
  return to login
  login with credentials
  add product to cart  1  1
  proceed to checkout
  process payment  success
  logout
  return to login
  login with credentials
  add product to cart  1  1
  logout
  return to login
  login with credentials
  add product to cart  1  1
  proceed to checkout
  cancel checkout

Test 16
  Set Machine Variables  ${VALID_EMAIL}  ${VALID_PASSWORD}  success  1  1
  login with credentials
  add product to cart  1  1
  proceed to checkout
  process payment  success
  logout
  return to login
  login with credentials
  add product to cart  1  1
  proceed to checkout
  process payment  success
  logout
  return to login
  login with credentials
  add product to cart  1  1
  logout
  return to login
  login with credentials
  add product to cart  1  1
  proceed to checkout
  logout

Test 17
  Set Machine Variables  ${VALID_EMAIL}  ${VALID_PASSWORD}  success  1  1
  login with credentials
  add product to cart  1  1
  proceed to checkout
  process payment  success
  logout
  return to login
  login with credentials
  add product to cart  1  1
  proceed to checkout
  process payment  success
  logout
  return to login
  login with credentials
  add product to cart  1  1
  logout
  return to login
  login with credentials
  add product to cart  1  1
  logout
  return to login

Test 18
  Set Machine Variables  ${VALID_EMAIL}  ${VALID_PASSWORD}  success  1  1
  login with credentials
  add product to cart  1  1
  proceed to checkout
  process payment  success
  logout
  return to login
  login with credentials
  add product to cart  1  1
  proceed to checkout
  process payment  success
  logout
  return to login
  login with credentials
  add product to cart  1  1
  logout
  return to login
  login with credentials
  logout
  return to login
  login with credentials

Test 19
  Set Machine Variables  ${VALID_EMAIL}  ${VALID_PASSWORD}  success  1  1
  login with credentials
  add product to cart  1  1
  proceed to checkout
  process payment  success
  logout
  return to login
  login with credentials
  add product to cart  1  1
  proceed to checkout
  process payment  success
  logout
  return to login
  login with credentials
  logout
  return to login
  login with credentials
  add product to cart  1  1
  proceed to checkout
  process payment  success
  logout

Test 20
  Set Machine Variables  ${VALID_EMAIL}  ${VALID_PASSWORD}  success  1  1
  login with credentials
  add product to cart  1  1
  proceed to checkout
  process payment  success
  logout
  return to login
  login with credentials
  add product to cart  1  1
  proceed to checkout
  process payment  success
  logout
  return to login
  login with credentials
  logout
  return to login
  login with credentials
  add product to cart  1  1
  proceed to checkout
  cancel checkout
  proceed to checkout

Test 21
  Set Machine Variables  ${VALID_EMAIL}  ${VALID_PASSWORD}  success  1  1
  login with credentials
  add product to cart  1  1
  proceed to checkout
  process payment  success
  logout
  return to login
  login with credentials
  add product to cart  1  1
  proceed to checkout
  process payment  success
  logout
  return to login
  login with credentials
  logout
  return to login
  login with credentials
  add product to cart  1  1
  proceed to checkout
  cancel checkout
  logout

Test 22
  Set Machine Variables  ${VALID_EMAIL}  ${VALID_PASSWORD}  success  1  1
  login with credentials
  add product to cart  1  1
  proceed to checkout
  process payment  success
  logout
  return to login
  login with credentials
  add product to cart  1  1
  proceed to checkout
  process payment  success
  logout
  return to login
  login with credentials
  logout
  return to login
  login with credentials
  add product to cart  1  1
  proceed to checkout
  logout
  return to login

Test 23
  Set Machine Variables  ${VALID_EMAIL}  ${VALID_PASSWORD}  success  1  1
  login with credentials
  add product to cart  1  1
  proceed to checkout
  process payment  success
  logout
  return to login
  login with credentials
  add product to cart  1  1
  proceed to checkout
  process payment  success
  logout
  return to login
  login with credentials
  logout
  return to login
  login with credentials
  add product to cart  1  1
  logout
  return to login
  login with credentials

Test 24
  Set Machine Variables  ${VALID_EMAIL}  ${VALID_PASSWORD}  success  1  1
  login with credentials
  add product to cart  1  1
  proceed to checkout
  process payment  success
  logout
  return to login
  login with credentials
  add product to cart  1  1
  proceed to checkout
  process payment  success
  logout
  return to login
  login with credentials
  logout
  return to login
  login with credentials
  logout
  return to login
  login with credentials
  add product to cart  1  1

Test 25
  Set Machine Variables  ${VALID_EMAIL}  ${VALID_PASSWORD}  success  1  1
  login with credentials
  add product to cart  1  1
  proceed to checkout
  process payment  success
  logout
  return to login
  login with credentials
  add product to cart  1  1
  proceed to checkout
  process payment  success
  logout
  return to login
  login with credentials
  logout
  return to login
  login with credentials
  logout
  return to login
  login with credentials
  logout

Test 26
  Set Machine Variables  ${VALID_EMAIL}  ${VALID_PASSWORD}  success  1  1
  login with credentials
  add product to cart  1  1
  proceed to checkout
  process payment  success
  logout
  return to login
  login with credentials
  add product to cart  1  1
  proceed to checkout
  cancel checkout
  proceed to checkout
  process payment  success
  logout
  return to login
  login with credentials
  add product to cart  1  1
  proceed to checkout
  process payment  success
  logout
  return to login

Test 27
  Set Machine Variables  ${VALID_EMAIL}  ${VALID_PASSWORD}  success  1  1
  login with credentials
  add product to cart  1  1
  proceed to checkout
  process payment  success
  logout
  return to login
  login with credentials
  add product to cart  1  1
  proceed to checkout
  cancel checkout
  proceed to checkout
  process payment  success
  logout
  return to login
  login with credentials
  add product to cart  1  1
  proceed to checkout
  cancel checkout
  proceed to checkout
  process payment  success

Test 28
  Set Machine Variables  ${VALID_EMAIL}  ${VALID_PASSWORD}  success  1  1
  login with credentials
  add product to cart  1  1
  proceed to checkout
  process payment  success
  logout
  return to login
  login with credentials
  add product to cart  1  1
  proceed to checkout
  cancel checkout
  proceed to checkout
  process payment  success
  logout
  return to login
  login with credentials
  add product to cart  1  1
  proceed to checkout
  cancel checkout
  proceed to checkout
  cancel checkout

Test 29
  Set Machine Variables  ${VALID_EMAIL}  ${VALID_PASSWORD}  success  1  1
  login with credentials
  add product to cart  1  1
  proceed to checkout
  process payment  success
  logout
  return to login
  login with credentials
  add product to cart  1  1
  proceed to checkout
  cancel checkout
  proceed to checkout
  process payment  success
  logout
  return to login
  login with credentials
  add product to cart  1  1
  proceed to checkout
  cancel checkout
  proceed to checkout
  logout

Test 30
  Set Machine Variables  ${VALID_EMAIL}  ${VALID_PASSWORD}  success  1  1
  login with credentials
  add product to cart  1  1
  proceed to checkout
  process payment  success
  logout
  return to login
  login with credentials
  add product to cart  1  1
  proceed to checkout
  cancel checkout
  proceed to checkout
  process payment  success
  logout
  return to login
  login with credentials
  add product to cart  1  1
  proceed to checkout
  cancel checkout
  logout
  return to login

Test 31
  Set Machine Variables  ${VALID_EMAIL}  ${VALID_PASSWORD}  success  1  1
  login with credentials
  add product to cart  1  1
  proceed to checkout
  process payment  success
  logout
  return to login
  login with credentials
  add product to cart  1  1
  proceed to checkout
  cancel checkout
  proceed to checkout
  process payment  success
  logout
  return to login
  login with credentials
  add product to cart  1  1
  proceed to checkout
  logout
  return to login
  login with credentials

Test 32
  Set Machine Variables  ${VALID_EMAIL}  ${VALID_PASSWORD}  success  1  1
  login with credentials
  add product to cart  1  1
  proceed to checkout
  process payment  success
  logout
  return to login
  login with credentials
  add product to cart  1  1
  proceed to checkout
  cancel checkout
  proceed to checkout
  process payment  success
  logout
  return to login
  login with credentials
  add product to cart  1  1
  logout
  return to login
  login with credentials
  add product to cart  1  1

Test 33
  Set Machine Variables  ${VALID_EMAIL}  ${VALID_PASSWORD}  success  1  1
  login with credentials
  add product to cart  1  1
  proceed to checkout
  process payment  success
  logout
  return to login
  login with credentials
  add product to cart  1  1
  proceed to checkout
  cancel checkout
  proceed to checkout
  process payment  success
  logout
  return to login
  login with credentials
  add product to cart  1  1
  logout
  return to login
  login with credentials
  logout

Test 34
  Set Machine Variables  ${VALID_EMAIL}  ${VALID_PASSWORD}  success  1  1
  login with credentials
  add product to cart  1  1
  proceed to checkout
  process payment  success
  logout
  return to login
  login with credentials
  add product to cart  1  1
  proceed to checkout
  cancel checkout
  proceed to checkout
  process payment  success
  logout
  return to login
  login with credentials
  logout
  return to login
  login with credentials
  add product to cart  1  1
  proceed to checkout

Test 35
  Set Machine Variables  ${VALID_EMAIL}  ${VALID_PASSWORD}  success  1  1
  login with credentials
  add product to cart  1  1
  proceed to checkout
  process payment  success
  logout
  return to login
  login with credentials
  add product to cart  1  1
  proceed to checkout
  cancel checkout
  proceed to checkout
  process payment  success
  logout
  return to login
  login with credentials
  logout
  return to login
  login with credentials
  add product to cart  1  1
  logout

Test 36
  Set Machine Variables  ${VALID_EMAIL}  ${VALID_PASSWORD}  success  1  1
  login with credentials
  add product to cart  1  1
  proceed to checkout
  process payment  success
  logout
  return to login
  login with credentials
  add product to cart  1  1
  proceed to checkout
  cancel checkout
  proceed to checkout
  process payment  success
  logout
  return to login
  login with credentials
  logout
  return to login
  login with credentials
  logout
  return to login

Test 37
  Set Machine Variables  ${VALID_EMAIL}  ${VALID_PASSWORD}  success  1  1
  login with credentials
  add product to cart  1  1
  proceed to checkout
  process payment  success
  logout
  return to login
  login with credentials
  add product to cart  1  1
  proceed to checkout
  cancel checkout
  proceed to checkout
  cancel checkout
  proceed to checkout
  process payment  success
  logout
  return to login
  login with credentials
  add product to cart  1  1
  proceed to checkout
  process payment  success

Test 38
  Set Machine Variables  ${VALID_EMAIL}  ${VALID_PASSWORD}  success  1  1
  login with credentials
  add product to cart  1  1
  proceed to checkout
  process payment  success
  logout
  return to login
  login with credentials
  add product to cart  1  1
  proceed to checkout
  cancel checkout
  proceed to checkout
  cancel checkout
  proceed to checkout
  process payment  success
  logout
  return to login
  login with credentials
  add product to cart  1  1
  proceed to checkout
  cancel checkout

Test 39
  Set Machine Variables  ${VALID_EMAIL}  ${VALID_PASSWORD}  success  1  1
  login with credentials
  add product to cart  1  1
  proceed to checkout
  process payment  success
  logout
  return to login
  login with credentials
  add product to cart  1  1
  proceed to checkout
  cancel checkout
  proceed to checkout
  cancel checkout
  proceed to checkout
  process payment  success
  logout
  return to login
  login with credentials
  add product to cart  1  1
  proceed to checkout
  logout

Test 40
  Set Machine Variables  ${VALID_EMAIL}  ${VALID_PASSWORD}  success  1  1
  login with credentials
  add product to cart  1  1
  proceed to checkout
  process payment  success
  logout
  return to login
  login with credentials
  add product to cart  1  1
  proceed to checkout
  cancel checkout
  proceed to checkout
  cancel checkout
  proceed to checkout
  process payment  success
  logout
  return to login
  login with credentials
  add product to cart  1  1
  logout
  return to login

Test 41
  Set Machine Variables  ${VALID_EMAIL}  ${VALID_PASSWORD}  success  1  1
  login with credentials
  add product to cart  1  1
  proceed to checkout
  process payment  success
  logout
  return to login
  login with credentials
  add product to cart  1  1
  proceed to checkout
  cancel checkout
  proceed to checkout
  cancel checkout
  proceed to checkout
  process payment  success
  logout
  return to login
  login with credentials
  logout
  return to login
  login with credentials

Test 42
  Set Machine Variables  ${VALID_EMAIL}  ${VALID_PASSWORD}  success  1  1
  login with credentials
  add product to cart  1  1
  proceed to checkout
  process payment  success
  logout
  return to login
  login with credentials
  add product to cart  1  1
  proceed to checkout
  cancel checkout
  proceed to checkout
  cancel checkout
  proceed to checkout
  cancel checkout
  proceed to checkout
  process payment  success
  logout
  return to login
  login with credentials
  add product to cart  1  1

Test 43
  Set Machine Variables  ${VALID_EMAIL}  ${VALID_PASSWORD}  success  1  1
  login with credentials
  add product to cart  1  1
  proceed to checkout
  process payment  success
  logout
  return to login
  login with credentials
  add product to cart  1  1
  proceed to checkout
  cancel checkout
  proceed to checkout
  cancel checkout
  proceed to checkout
  cancel checkout
  proceed to checkout
  process payment  success
  logout
  return to login
  login with credentials
  logout

Test 44
  Set Machine Variables  ${VALID_EMAIL}  ${VALID_PASSWORD}  success  1  1
  login with credentials
  add product to cart  1  1
  proceed to checkout
  process payment  success
  logout
  return to login
  login with credentials
  add product to cart  1  1
  proceed to checkout
  cancel checkout
  proceed to checkout
  cancel checkout
  proceed to checkout
  cancel checkout
  proceed to checkout
  cancel checkout
  proceed to checkout
  process payment  success
  logout
  return to login

Test 45
  Set Machine Variables  ${VALID_EMAIL}  ${VALID_PASSWORD}  success  1  1
  login with credentials
  add product to cart  1  1
  proceed to checkout
  process payment  success
  logout
  return to login
  login with credentials
  add product to cart  1  1
  proceed to checkout
  cancel checkout
  proceed to checkout
  cancel checkout
  proceed to checkout
  cancel checkout
  proceed to checkout
  cancel checkout
  proceed to checkout
  cancel checkout
  proceed to checkout
  process payment  success

Test 46
  Set Machine Variables  ${VALID_EMAIL}  ${VALID_PASSWORD}  success  1  1
  login with credentials
  add product to cart  1  1
  proceed to checkout
  process payment  success
  logout
  return to login
  login with credentials
  add product to cart  1  1
  proceed to checkout
  cancel checkout
  proceed to checkout
  cancel checkout
  proceed to checkout
  cancel checkout
  proceed to checkout
  cancel checkout
  proceed to checkout
  cancel checkout
  proceed to checkout
  cancel checkout

Test 47
  Set Machine Variables  ${VALID_EMAIL}  ${VALID_PASSWORD}  success  1  1
  login with credentials
  add product to cart  1  1
  proceed to checkout
  process payment  success
  logout
  return to login
  login with credentials
  add product to cart  1  1
  proceed to checkout
  cancel checkout
  proceed to checkout
  cancel checkout
  proceed to checkout
  cancel checkout
  proceed to checkout
  cancel checkout
  proceed to checkout
  cancel checkout
  proceed to checkout
  logout

Test 48
  Set Machine Variables  ${VALID_EMAIL}  ${VALID_PASSWORD}  success  1  1
  login with credentials
  add product to cart  1  1
  proceed to checkout
  process payment  success
  logout
  return to login
  login with credentials
  add product to cart  1  1
  proceed to checkout
  cancel checkout
  proceed to checkout
  cancel checkout
  proceed to checkout
  cancel checkout
  proceed to checkout
  cancel checkout
  proceed to checkout
  cancel checkout
  logout
  return to login

Test 49
  Set Machine Variables  ${VALID_EMAIL}  ${VALID_PASSWORD}  success  1  1
  login with credentials
  add product to cart  1  1
  proceed to checkout
  process payment  success
  logout
  return to login
  login with credentials
  add product to cart  1  1
  proceed to checkout
  cancel checkout
  proceed to checkout
  cancel checkout
  proceed to checkout
  cancel checkout
  proceed to checkout
  cancel checkout
  proceed to checkout
  logout
  return to login
  login with credentials

Test 50
  Set Machine Variables  ${VALID_EMAIL}  ${VALID_PASSWORD}  success  1  1
  login with credentials
  add product to cart  1  1
  proceed to checkout
  process payment  success
  logout
  return to login
  login with credentials
  add product to cart  1  1
  proceed to checkout
  cancel checkout
  proceed to checkout
  cancel checkout
  proceed to checkout
  cancel checkout
  proceed to checkout
  cancel checkout
  logout
  return to login
  login with credentials
  add product to cart  1  1

*** Keywords ***
Set Machine Variables
  [Arguments]  ${EMAIL}  ${PASSWORD}  ${PAYMENT}  ${PRODUCT_ID}  ${QUANTITY}
  Set Test Variable  \${EMAIL}
  Set Test Variable  \${PASSWORD}
  Set Test Variable  \${PAYMENT}
  Set Test Variable  \${PRODUCT_ID}
  Set Test Variable  \${QUANTITY}
