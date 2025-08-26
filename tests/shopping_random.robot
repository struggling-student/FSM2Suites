# ============================================================================
# TEST COVERAGE INFORMATION
# ============================================================================
#
# Covered states (8/8):
#     Browsing
#     CartEditing
#     Checkout
#     Login
#     LoginFailed
#     OrderConfirmed
#     PaymentFailed
#     SessionEnded
#
# Covered actions (17/17):
#     add product to cart  (Browsing -> CartEditing)
#     cancel checkout  (Checkout -> CartEditing)
#     cancel order  (PaymentFailed -> CartEditing)
#     exit application  (LoginFailed -> SessionEnded)
#     login with credentials  (Login -> LoginFailed)
#     login with credentials  (Login -> Browsing)
#     logout  (PaymentFailed -> SessionEnded)
#     logout  (Checkout -> SessionEnded)
#     logout  (OrderConfirmed -> SessionEnded)
#     logout  (CartEditing -> SessionEnded)
#     logout  (Browsing -> SessionEnded)
#     proceed to checkout  (CartEditing -> Checkout)
#     process payment  (Checkout -> PaymentFailed)
#     process payment  (Checkout -> OrderConfirmed)
#     retry payment  (PaymentFailed -> Checkout)
#     return to login  (SessionEnded -> Login)
#     try login again  (LoginFailed -> Login)
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
  Set Machine Variables  ${VALID_EMAIL}  ${INVALID_PASSWORD}  failure  2  1
  login with credentials
  try login again
  login with credentials
  try login again
  login with credentials
  exit application
  return to login
  login with credentials
  exit application
  return to login
  login with credentials
  try login again
  login with credentials
  try login again
  login with credentials
  try login again
  login with credentials
  exit application
  return to login
  login with credentials

Test 2
  Set Machine Variables  ${VALID_EMAIL}  ${INVALID_PASSWORD}  success  2  1
  login with credentials
  exit application
  return to login
  login with credentials
  try login again
  login with credentials
  exit application
  return to login
  login with credentials
  exit application
  return to login
  login with credentials
  try login again
  login with credentials
  exit application
  return to login
  login with credentials
  try login again
  login with credentials
  try login again

Test 3
  Set Machine Variables  ${INVALID_EMAIL}  ${INVALID_PASSWORD}  success  1  1
  login with credentials
  exit application
  return to login
  login with credentials
  exit application
  return to login
  login with credentials
  exit application
  return to login
  login with credentials
  exit application
  return to login
  login with credentials
  try login again
  login with credentials
  exit application
  return to login
  login with credentials
  exit application
  return to login

Test 4
  Set Machine Variables  ${INVALID_EMAIL}  ${INVALID_PASSWORD}  success  1  2
  login with credentials
  try login again
  login with credentials
  exit application
  return to login
  login with credentials
  exit application
  return to login
  login with credentials
  exit application
  return to login
  login with credentials
  exit application
  return to login
  login with credentials
  exit application
  return to login
  login with credentials
  try login again
  login with credentials

Test 5
  Set Machine Variables  ${INVALID_EMAIL}  ${VALID_PASSWORD}  success  2  2
  login with credentials
  try login again
  login with credentials
  exit application
  return to login
  login with credentials
  exit application
  return to login
  login with credentials
  try login again
  login with credentials
  try login again
  login with credentials
  try login again
  login with credentials
  exit application
  return to login
  login with credentials
  exit application
  return to login

Test 6
  Set Machine Variables  ${VALID_EMAIL}  ${VALID_PASSWORD}  success  2  2
  login with credentials
  logout
  return to login
  login with credentials
  add product to cart          2  2
  logout
  return to login
  login with credentials
  logout
  return to login
  login with credentials
  add product to cart          2  2
  proceed to checkout
  logout
  return to login
  login with credentials
  add product to cart          2  2
  logout
  return to login
  login with credentials

Test 7
  Set Machine Variables  ${VALID_EMAIL}  ${VALID_PASSWORD}  failure  1  2
  login with credentials
  add product to cart          1  2
  proceed to checkout
  process payment          failure
  retry payment
  logout
  return to login
  login with credentials
  logout
  return to login
  login with credentials
  logout
  return to login
  login with credentials
  add product to cart          1  2
  logout
  return to login
  login with credentials
  logout
  return to login

Test 8
  Set Machine Variables  ${VALID_EMAIL}  ${INVALID_PASSWORD}  failure  3  1
  login with credentials
  try login again
  login with credentials
  exit application
  return to login
  login with credentials
  try login again
  login with credentials
  exit application
  return to login
  login with credentials
  try login again
  login with credentials
  try login again
  login with credentials
  try login again
  login with credentials
  exit application
  return to login
  login with credentials

Test 9
  Set Machine Variables  ${INVALID_EMAIL}  ${VALID_PASSWORD}  success  3  1
  login with credentials
  try login again
  login with credentials
  exit application
  return to login
  login with credentials
  exit application
  return to login
  login with credentials
  exit application
  return to login
  login with credentials
  exit application
  return to login
  login with credentials
  try login again
  login with credentials
  try login again
  login with credentials
  exit application

Test 10
  Set Machine Variables  ${INVALID_EMAIL}  ${VALID_PASSWORD}  failure  3  1
  login with credentials
  exit application
  return to login
  login with credentials
  exit application
  return to login
  login with credentials
  exit application
  return to login
  login with credentials
  try login again
  login with credentials
  try login again
  login with credentials
  exit application
  return to login
  login with credentials
  try login again
  login with credentials
  exit application

Test 11
  Set Machine Variables  ${VALID_EMAIL}  ${VALID_PASSWORD}  success  2  2
  login with credentials
  add product to cart          2  2
  logout
  return to login
  login with credentials
  add product to cart          2  2
  logout
  return to login
  login with credentials
  add product to cart          2  2
  proceed to checkout
  cancel checkout
  proceed to checkout
  logout
  return to login
  login with credentials
  logout
  return to login
  login with credentials
  add product to cart          2  2

Test 12
  Set Machine Variables  ${INVALID_EMAIL}  ${INVALID_PASSWORD}  success  1  1
  login with credentials
  exit application
  return to login
  login with credentials
  exit application
  return to login
  login with credentials
  exit application
  return to login
  login with credentials
  exit application
  return to login
  login with credentials
  try login again
  login with credentials
  try login again
  login with credentials
  exit application
  return to login
  login with credentials

Test 13
  Set Machine Variables  ${VALID_EMAIL}  ${VALID_PASSWORD}  failure  2  1
  login with credentials
  add product to cart          2  1
  logout
  return to login
  login with credentials
  add product to cart          2  1
  logout
  return to login
  login with credentials
  logout
  return to login
  login with credentials
  add product to cart          2  1
  proceed to checkout
  process payment          failure
  logout
  return to login
  login with credentials
  add product to cart          2  1
  proceed to checkout

Test 14
  Set Machine Variables  ${VALID_EMAIL}  ${VALID_PASSWORD}  failure  1  1
  login with credentials
  logout
  return to login
  login with credentials
  logout
  return to login
  login with credentials
  logout
  return to login
  login with credentials
  add product to cart          1  1
  logout
  return to login
  login with credentials
  logout
  return to login
  login with credentials
  add product to cart          1  1
  proceed to checkout
  process payment          failure

Test 15
  Set Machine Variables  ${INVALID_EMAIL}  ${VALID_PASSWORD}  success  2  2
  login with credentials
  exit application
  return to login
  login with credentials
  exit application
  return to login
  login with credentials
  try login again
  login with credentials
  try login again
  login with credentials
  try login again
  login with credentials
  exit application
  return to login
  login with credentials
  exit application
  return to login
  login with credentials
  try login again

Test 16
  Set Machine Variables  ${INVALID_EMAIL}  ${INVALID_PASSWORD}  failure  3  2
  login with credentials
  exit application
  return to login
  login with credentials
  exit application
  return to login
  login with credentials
  try login again
  login with credentials
  try login again
  login with credentials
  exit application
  return to login
  login with credentials
  try login again
  login with credentials
  try login again
  login with credentials
  try login again
  login with credentials

Test 17
  Set Machine Variables  ${VALID_EMAIL}  ${VALID_PASSWORD}  success  3  1
  login with credentials
  add product to cart          3  1
  logout
  return to login
  login with credentials
  add product to cart          3  1
  logout
  return to login
  login with credentials
  add product to cart          3  1
  proceed to checkout
  cancel checkout
  proceed to checkout
  cancel checkout
  logout
  return to login
  login with credentials
  add product to cart          3  1
  proceed to checkout
  logout

Test 18
  Set Machine Variables  ${VALID_EMAIL}  ${VALID_PASSWORD}  success  3  2
  login with credentials
  logout
  return to login
  login with credentials
  logout
  return to login
  login with credentials
  logout
  return to login
  login with credentials
  add product to cart          3  2
  logout
  return to login
  login with credentials
  add product to cart          3  2
  proceed to checkout
  cancel checkout
  proceed to checkout
  process payment          success
  logout

Test 19
  Set Machine Variables  ${INVALID_EMAIL}  ${INVALID_PASSWORD}  failure  1  1
  login with credentials
  exit application
  return to login
  login with credentials
  exit application
  return to login
  login with credentials
  try login again
  login with credentials
  exit application
  return to login
  login with credentials
  try login again
  login with credentials
  try login again
  login with credentials
  exit application
  return to login
  login with credentials
  exit application

Test 20
  Set Machine Variables  ${INVALID_EMAIL}  ${INVALID_PASSWORD}  failure  2  1
  login with credentials
  try login again
  login with credentials
  exit application
  return to login
  login with credentials
  exit application
  return to login
  login with credentials
  exit application
  return to login
  login with credentials
  exit application
  return to login
  login with credentials
  exit application
  return to login
  login with credentials
  exit application
  return to login

Test 21
  Set Machine Variables  ${INVALID_EMAIL}  ${VALID_PASSWORD}  failure  2  2
  login with credentials
  try login again
  login with credentials
  exit application
  return to login
  login with credentials
  exit application
  return to login
  login with credentials
  exit application
  return to login
  login with credentials
  try login again
  login with credentials
  exit application
  return to login
  login with credentials
  try login again
  login with credentials
  try login again

Test 22
  Set Machine Variables  ${INVALID_EMAIL}  ${VALID_PASSWORD}  success  3  1
  login with credentials
  exit application
  return to login
  login with credentials
  try login again
  login with credentials
  try login again
  login with credentials
  try login again
  login with credentials
  try login again
  login with credentials
  exit application
  return to login
  login with credentials
  exit application
  return to login
  login with credentials
  try login again
  login with credentials

Test 23
  Set Machine Variables  ${VALID_EMAIL}  ${INVALID_PASSWORD}  success  3  1
  login with credentials
  exit application
  return to login
  login with credentials
  try login again
  login with credentials
  exit application
  return to login
  login with credentials
  exit application
  return to login
  login with credentials
  try login again
  login with credentials
  try login again
  login with credentials
  exit application
  return to login
  login with credentials
  try login again

Test 24
  Set Machine Variables  ${INVALID_EMAIL}  ${INVALID_PASSWORD}  success  2  2
  login with credentials
  try login again
  login with credentials
  exit application
  return to login
  login with credentials
  exit application
  return to login
  login with credentials
  try login again
  login with credentials
  exit application
  return to login
  login with credentials
  exit application
  return to login
  login with credentials
  try login again
  login with credentials
  exit application

Test 25
  Set Machine Variables  ${VALID_EMAIL}  ${VALID_PASSWORD}  failure  2  2
  login with credentials
  add product to cart          2  2
  proceed to checkout
  cancel checkout
  logout
  return to login
  login with credentials
  add product to cart          2  2
  proceed to checkout
  process payment          failure
  retry payment
  cancel checkout
  logout
  return to login
  login with credentials
  logout
  return to login
  login with credentials
  add product to cart          2  2
  logout

Test 26
  Set Machine Variables  ${INVALID_EMAIL}  ${VALID_PASSWORD}  success  2  1
  login with credentials
  try login again
  login with credentials
  exit application
  return to login
  login with credentials
  try login again
  login with credentials
  exit application
  return to login
  login with credentials
  try login again
  login with credentials
  try login again
  login with credentials
  try login again
  login with credentials
  try login again
  login with credentials
  exit application

Test 27
  Set Machine Variables  ${VALID_EMAIL}  ${VALID_PASSWORD}  success  2  1
  login with credentials
  add product to cart          2  1
  proceed to checkout
  process payment          success
  logout
  return to login
  login with credentials
  add product to cart          2  1
  logout
  return to login
  login with credentials
  logout
  return to login
  login with credentials
  add product to cart          2  1
  proceed to checkout
  cancel checkout
  proceed to checkout
  cancel checkout
  proceed to checkout

Test 28
  Set Machine Variables  ${INVALID_EMAIL}  ${INVALID_PASSWORD}  success  3  1
  login with credentials
  try login again
  login with credentials
  exit application
  return to login
  login with credentials
  try login again
  login with credentials
  exit application
  return to login
  login with credentials
  exit application
  return to login
  login with credentials
  try login again
  login with credentials
  try login again
  login with credentials
  try login again
  login with credentials

Test 29
  Set Machine Variables  ${INVALID_EMAIL}  ${INVALID_PASSWORD}  success  3  1
  login with credentials
  try login again
  login with credentials
  exit application
  return to login
  login with credentials
  exit application
  return to login
  login with credentials
  try login again
  login with credentials
  try login again
  login with credentials
  try login again
  login with credentials
  exit application
  return to login
  login with credentials
  try login again
  login with credentials

Test 30
  Set Machine Variables  ${INVALID_EMAIL}  ${VALID_PASSWORD}  failure  1  2
  login with credentials
  exit application
  return to login
  login with credentials
  try login again
  login with credentials
  exit application
  return to login
  login with credentials
  exit application
  return to login
  login with credentials
  exit application
  return to login
  login with credentials
  exit application
  return to login
  login with credentials
  exit application
  return to login

Test 31
  Set Machine Variables  ${VALID_EMAIL}  ${INVALID_PASSWORD}  failure  2  2
  login with credentials
  exit application
  return to login
  login with credentials
  exit application
  return to login
  login with credentials
  try login again
  login with credentials
  try login again
  login with credentials
  exit application
  return to login
  login with credentials
  exit application
  return to login
  login with credentials
  exit application
  return to login
  login with credentials

Test 32
  Set Machine Variables  ${VALID_EMAIL}  ${VALID_PASSWORD}  success  2  2
  login with credentials
  logout
  return to login
  login with credentials
  add product to cart          2  2
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
  return to login
  login with credentials
  logout
  return to login
  login with credentials

Test 33
  Set Machine Variables  ${INVALID_EMAIL}  ${VALID_PASSWORD}  failure  2  1
  login with credentials
  try login again
  login with credentials
  try login again
  login with credentials
  exit application
  return to login
  login with credentials
  try login again
  login with credentials
  try login again
  login with credentials
  try login again
  login with credentials
  exit application
  return to login
  login with credentials
  try login again
  login with credentials
  exit application

Test 34
  Set Machine Variables  ${INVALID_EMAIL}  ${INVALID_PASSWORD}  failure  1  1
  login with credentials
  exit application
  return to login
  login with credentials
  try login again
  login with credentials
  try login again
  login with credentials
  exit application
  return to login
  login with credentials
  exit application
  return to login
  login with credentials
  exit application
  return to login
  login with credentials
  try login again
  login with credentials
  try login again

Test 35
  Set Machine Variables  ${VALID_EMAIL}  ${VALID_PASSWORD}  failure  1  2
  login with credentials
  add product to cart          1  2
  logout
  return to login
  login with credentials
  add product to cart          1  2
  logout
  return to login
  login with credentials
  add product to cart          1  2
  logout
  return to login
  login with credentials
  add product to cart          1  2
  logout
  return to login
  login with credentials
  add product to cart          1  2
  logout
  return to login

Test 36
  Set Machine Variables  ${VALID_EMAIL}  ${INVALID_PASSWORD}  failure  1  1
  login with credentials
  exit application
  return to login
  login with credentials
  exit application
  return to login
  login with credentials
  try login again
  login with credentials
  exit application
  return to login
  login with credentials
  exit application
  return to login
  login with credentials
  try login again
  login with credentials
  try login again
  login with credentials
  exit application

Test 37
  Set Machine Variables  ${INVALID_EMAIL}  ${VALID_PASSWORD}  failure  2  2
  login with credentials
  exit application
  return to login
  login with credentials
  exit application
  return to login
  login with credentials
  exit application
  return to login
  login with credentials
  try login again
  login with credentials
  try login again
  login with credentials
  try login again
  login with credentials
  exit application
  return to login
  login with credentials
  exit application

Test 38
  Set Machine Variables  ${VALID_EMAIL}  ${VALID_PASSWORD}  failure  2  2
  login with credentials
  add product to cart          2  2
  logout
  return to login
  login with credentials
  logout
  return to login
  login with credentials
  add product to cart          2  2
  proceed to checkout
  cancel checkout
  proceed to checkout
  process payment          failure
  retry payment
  logout
  return to login
  login with credentials
  logout
  return to login
  login with credentials

Test 39
  Set Machine Variables  ${VALID_EMAIL}  ${VALID_PASSWORD}  success  1  1
  login with credentials
  add product to cart          1  1
  proceed to checkout
  process payment          success
  logout
  return to login
  login with credentials
  add product to cart          1  1
  proceed to checkout
  process payment          success
  logout
  return to login
  login with credentials
  add product to cart          1  1
  proceed to checkout
  cancel checkout
  logout
  return to login
  login with credentials
  add product to cart          1  1

Test 40
  Set Machine Variables  ${VALID_EMAIL}  ${VALID_PASSWORD}  success  2  2
  login with credentials
  add product to cart          2  2
  proceed to checkout
  process payment          success
  logout
  return to login
  login with credentials
  add product to cart          2  2
  logout
  return to login
  login with credentials
  add product to cart          2  2
  logout
  return to login
  login with credentials
  logout
  return to login
  login with credentials
  add product to cart          2  2
  logout

Test 41
  Set Machine Variables  ${INVALID_EMAIL}  ${INVALID_PASSWORD}  failure  1  1
  login with credentials
  try login again
  login with credentials
  exit application
  return to login
  login with credentials
  exit application
  return to login
  login with credentials
  exit application
  return to login
  login with credentials
  try login again
  login with credentials
  exit application
  return to login
  login with credentials
  exit application
  return to login
  login with credentials

Test 42
  Set Machine Variables  ${INVALID_EMAIL}  ${VALID_PASSWORD}  failure  1  1
  login with credentials
  try login again
  login with credentials
  exit application
  return to login
  login with credentials
  exit application
  return to login
  login with credentials
  exit application
  return to login
  login with credentials
  try login again
  login with credentials
  exit application
  return to login
  login with credentials
  try login again
  login with credentials
  try login again

Test 43
  Set Machine Variables  ${INVALID_EMAIL}  ${VALID_PASSWORD}  failure  1  1
  login with credentials
  exit application
  return to login
  login with credentials
  try login again
  login with credentials
  exit application
  return to login
  login with credentials
  exit application
  return to login
  login with credentials
  exit application
  return to login
  login with credentials
  try login again
  login with credentials
  exit application
  return to login
  login with credentials

Test 44
  Set Machine Variables  ${INVALID_EMAIL}  ${VALID_PASSWORD}  failure  2  2
  login with credentials
  exit application
  return to login
  login with credentials
  exit application
  return to login
  login with credentials
  try login again
  login with credentials
  try login again
  login with credentials
  exit application
  return to login
  login with credentials
  exit application
  return to login
  login with credentials
  exit application
  return to login
  login with credentials

Test 45
  Set Machine Variables  ${VALID_EMAIL}  ${INVALID_PASSWORD}  success  1  1
  login with credentials
  try login again
  login with credentials
  try login again
  login with credentials
  try login again
  login with credentials
  try login again
  login with credentials
  exit application
  return to login
  login with credentials
  exit application
  return to login
  login with credentials
  try login again
  login with credentials
  try login again
  login with credentials
  exit application

Test 46
  Set Machine Variables  ${VALID_EMAIL}  ${VALID_PASSWORD}  failure  2  1
  login with credentials
  add product to cart          2  1
  proceed to checkout
  process payment          failure
  cancel order
  proceed to checkout
  process payment          failure
  retry payment
  process payment          failure
  retry payment
  process payment          failure
  cancel order
  proceed to checkout
  logout
  return to login
  login with credentials
  add product to cart          2  1
  logout
  return to login
  login with credentials

Test 47
  Set Machine Variables  ${INVALID_EMAIL}  ${INVALID_PASSWORD}  success  3  1
  login with credentials
  exit application
  return to login
  login with credentials
  exit application
  return to login
  login with credentials
  exit application
  return to login
  login with credentials
  exit application
  return to login
  login with credentials
  try login again
  login with credentials
  try login again
  login with credentials
  exit application
  return to login
  login with credentials

Test 48
  Set Machine Variables  ${VALID_EMAIL}  ${INVALID_PASSWORD}  failure  1  1
  login with credentials
  exit application
  return to login
  login with credentials
  try login again
  login with credentials
  exit application
  return to login
  login with credentials
  try login again
  login with credentials
  try login again
  login with credentials
  try login again
  login with credentials
  exit application
  return to login
  login with credentials
  exit application
  return to login

Test 49
  Set Machine Variables  ${INVALID_EMAIL}  ${VALID_PASSWORD}  success  1  1
  login with credentials
  try login again
  login with credentials
  try login again
  login with credentials
  exit application
  return to login
  login with credentials
  try login again
  login with credentials
  try login again
  login with credentials
  exit application
  return to login
  login with credentials
  try login again
  login with credentials
  try login again
  login with credentials
  exit application

Test 50
  Set Machine Variables  ${INVALID_EMAIL}  ${VALID_PASSWORD}  failure  3  2
  login with credentials
  exit application
  return to login
  login with credentials
  try login again
  login with credentials
  try login again
  login with credentials
  exit application
  return to login
  login with credentials
  try login again
  login with credentials
  try login again
  login with credentials
  exit application
  return to login
  login with credentials
  try login again
  login with credentials

*** Keywords ***
Set Machine Variables
  [Arguments]  ${EMAIL}  ${PASSWORD}  ${PAYMENT}  ${PRODUCT_ID}  ${QUANTITY}
  Set Test Variable  \${EMAIL}
  Set Test Variable  \${PASSWORD}
  Set Test Variable  \${PAYMENT}
  Set Test Variable  \${PRODUCT_ID}
  Set Test Variable  \${QUANTITY}
