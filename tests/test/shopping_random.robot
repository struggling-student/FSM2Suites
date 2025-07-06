*** Settings ***
Library         ShoppingKeywordLibrary.py
Test Setup      Setup Shopping Environment
Test Teardown   Teardown Shopping Environment

*** Variables ***
${VALID_EMAIL}        test@example.com
${VALID_PASSWORD}     password123
${INVALID_EMAIL}      invalid@example.com
${INVALID_PASSWORD}   wrongpassword

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
#     logout  (Browsing -> SessionEnded)
#     logout  (CartEditing -> SessionEnded)
#     proceed to checkout  (CartEditing -> Checkout)
#     cancel checkout  (Checkout -> CartEditing)
#     logout  (Checkout -> SessionEnded)
#     process payment  (Checkout -> PaymentFailed)
#     process payment  (Checkout -> OrderConfirmed)
#     login with credentials  (Login -> Browsing)
#     login with credentials  (Login -> LoginFailed)
#     exit application  (LoginFailed -> SessionEnded)
#     try login again  (LoginFailed -> Login)
#     logout  (OrderConfirmed -> SessionEnded)
#     cancel order  (PaymentFailed -> CartEditing)
#     logout  (PaymentFailed -> SessionEnded)
#     retry payment  (PaymentFailed -> Checkout)
#     return to login  (SessionEnded -> Login)
#
# ============================================================================

*** Test Cases ***
Test 1
  Set Machine Variables  ${VALID_EMAIL}  ${VALID_PASSWORD}  failure  2  1
  login with credentials
  add product to cart  2  1
  logout
  return to login
  login with credentials
  logout
  return to login
  login with credentials
  logout
  return to login
  login with credentials
  add product to cart  2  1
  proceed to checkout
  process payment  failure
  logout
  return to login
  login with credentials
  logout
  return to login
  login with credentials

Test 2
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
  logout
  return to login
  login with credentials
  add product to cart  3  2
  logout
  return to login
  login with credentials
  add product to cart  3  2
  logout
  return to login

Test 3
  Set Machine Variables  ${INVALID_EMAIL}  ${VALID_PASSWORD}  failure  3  1
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
  return to login
  login with credentials
  exit application
  return to login
  login with credentials
  exit application
  return to login
  login with credentials
  try login again

Test 4
  Set Machine Variables  ${INVALID_EMAIL}  ${VALID_PASSWORD}  success  2  1
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

Test 5
  Set Machine Variables  ${INVALID_EMAIL}  ${INVALID_PASSWORD}  failure  2  2
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
  exit application
  return to login

Test 6
  Set Machine Variables  ${INVALID_EMAIL}  ${VALID_PASSWORD}  success  1  1
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
  try login again
  login with credentials

Test 7
  Set Machine Variables  ${INVALID_EMAIL}  ${VALID_PASSWORD}  failure  1  2
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
  exit application
  return to login
  login with credentials
  try login again
  login with credentials
  try login again
  login with credentials

Test 8
  Set Machine Variables  ${INVALID_EMAIL}  ${INVALID_PASSWORD}  success  3  2
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
  return to login
  login with credentials
  exit application
  return to login
  login with credentials
  exit application

Test 9
  Set Machine Variables  ${INVALID_EMAIL}  ${INVALID_PASSWORD}  failure  3  2
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
  try login again
  login with credentials
  try login again
  login with credentials
  try login again

Test 10
  Set Machine Variables  ${INVALID_EMAIL}  ${INVALID_PASSWORD}  success  3  2
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

Test 11
  Set Machine Variables  ${INVALID_EMAIL}  ${INVALID_PASSWORD}  success  2  2
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
  try login again
  login with credentials

Test 12
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

Test 13
  Set Machine Variables  ${VALID_EMAIL}  ${INVALID_PASSWORD}  failure  3  2
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
  try login again
  login with credentials
  try login again

Test 14
  Set Machine Variables  ${INVALID_EMAIL}  ${INVALID_PASSWORD}  failure  1  2
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
  login with credentials
  try login again
  login with credentials

Test 15
  Set Machine Variables  ${VALID_EMAIL}  ${INVALID_PASSWORD}  success  3  2
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

Test 16
  Set Machine Variables  ${VALID_EMAIL}  ${INVALID_PASSWORD}  success  1  1
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
  try login again
  login with credentials
  exit application
  return to login
  login with credentials

Test 17
  Set Machine Variables  ${VALID_EMAIL}  ${INVALID_PASSWORD}  failure  1  2
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
  try login again
  login with credentials

Test 18
  Set Machine Variables  ${INVALID_EMAIL}  ${INVALID_PASSWORD}  failure  3  1
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
  exit application
  return to login

Test 19
  Set Machine Variables  ${VALID_EMAIL}  ${VALID_PASSWORD}  success  3  2
  login with credentials
  logout
  return to login
  login with credentials
  logout
  return to login
  login with credentials
  add product to cart  3  2
  logout
  return to login
  login with credentials
  add product to cart  3  2
  logout
  return to login
  login with credentials
  logout
  return to login
  login with credentials
  logout
  return to login

Test 20
  Set Machine Variables  ${INVALID_EMAIL}  ${INVALID_PASSWORD}  failure  1  2
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

Test 21
  Set Machine Variables  ${INVALID_EMAIL}  ${INVALID_PASSWORD}  failure  1  2
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
  return to login
  login with credentials
  exit application
  return to login

Test 22
  Set Machine Variables  ${INVALID_EMAIL}  ${VALID_PASSWORD}  failure  2  1
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
  try login again
  login with credentials
  exit application
  return to login
  login with credentials

Test 23
  Set Machine Variables  ${INVALID_EMAIL}  ${VALID_PASSWORD}  success  1  2
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
  login with credentials
  exit application
  return to login

Test 24
  Set Machine Variables  ${VALID_EMAIL}  ${VALID_PASSWORD}  success  1  2
  login with credentials
  add product to cart  1  2
  proceed to checkout
  logout
  return to login
  login with credentials
  add product to cart  1  2
  proceed to checkout
  cancel checkout
  logout
  return to login
  login with credentials
  logout
  return to login
  login with credentials
  add product to cart  1  2
  proceed to checkout
  cancel checkout
  proceed to checkout
  logout

Test 25
  Set Machine Variables  ${VALID_EMAIL}  ${INVALID_PASSWORD}  success  3  2
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
  try login again

Test 26
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

Test 27
  Set Machine Variables  ${INVALID_EMAIL}  ${VALID_PASSWORD}  failure  1  1
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
  try login again
  login with credentials
  exit application
  return to login
  login with credentials
  exit application

Test 28
  Set Machine Variables  ${INVALID_EMAIL}  ${VALID_PASSWORD}  success  3  1
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
  return to login
  login with credentials
  try login again
  login with credentials
  exit application
  return to login

Test 29
  Set Machine Variables  ${VALID_EMAIL}  ${VALID_PASSWORD}  success  3  1
  login with credentials
  logout
  return to login
  login with credentials
  logout
  return to login
  login with credentials
  add product to cart  3  1
  proceed to checkout
  process payment  success
  logout
  return to login
  login with credentials
  add product to cart  3  1
  proceed to checkout
  process payment  success
  logout
  return to login
  login with credentials
  logout

Test 30
  Set Machine Variables  ${INVALID_EMAIL}  ${VALID_PASSWORD}  success  1  1
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
  exit application
  return to login
  login with credentials
  exit application
  return to login

Test 31
  Set Machine Variables  ${INVALID_EMAIL}  ${INVALID_PASSWORD}  success  2  1
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
  try login again

Test 32
  Set Machine Variables  ${VALID_EMAIL}  ${VALID_PASSWORD}  failure  3  2
  login with credentials
  add product to cart  3  2
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
  logout
  return to login
  login with credentials

Test 33
  Set Machine Variables  ${VALID_EMAIL}  ${VALID_PASSWORD}  failure  2  1
  login with credentials
  logout
  return to login
  login with credentials
  add product to cart  2  1
  proceed to checkout
  process payment  failure
  cancel order
  logout
  return to login
  login with credentials
  logout
  return to login
  login with credentials
  logout
  return to login
  login with credentials
  add product to cart  2  1
  logout
  return to login

Test 34
  Set Machine Variables  ${INVALID_EMAIL}  ${VALID_PASSWORD}  success  1  1
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
  try login again
  login with credentials
  exit application

Test 35
  Set Machine Variables  ${INVALID_EMAIL}  ${INVALID_PASSWORD}  success  3  2
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
  login with credentials
  try login again
  login with credentials
  try login again
  login with credentials

Test 36
  Set Machine Variables  ${VALID_EMAIL}  ${VALID_PASSWORD}  failure  2  2
  login with credentials
  add product to cart  2  2
  proceed to checkout
  process payment  failure
  retry payment
  cancel checkout
  proceed to checkout
  process payment  failure
  retry payment
  process payment  failure
  cancel order
  proceed to checkout
  cancel checkout
  proceed to checkout
  process payment  failure
  logout
  return to login
  login with credentials
  logout
  return to login

Test 37
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

Test 38
  Set Machine Variables  ${VALID_EMAIL}  ${VALID_PASSWORD}  success  3  1
  login with credentials
  logout
  return to login
  login with credentials
  add product to cart  3  1
  logout
  return to login
  login with credentials
  add product to cart  3  1
  proceed to checkout
  process payment  success
  logout
  return to login
  login with credentials
  add product to cart  3  1
  proceed to checkout
  process payment  success
  logout
  return to login
  login with credentials

Test 39
  Set Machine Variables  ${INVALID_EMAIL}  ${INVALID_PASSWORD}  success  3  2
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
  login with credentials
  exit application

Test 40
  Set Machine Variables  ${INVALID_EMAIL}  ${VALID_PASSWORD}  failure  2  1
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
  return to login
  login with credentials
  exit application
  return to login

Test 41
  Set Machine Variables  ${VALID_EMAIL}  ${INVALID_PASSWORD}  success  1  2
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

Test 42
  Set Machine Variables  ${INVALID_EMAIL}  ${INVALID_PASSWORD}  success  2  1
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
  return to login
  login with credentials
  exit application

Test 43
  Set Machine Variables  ${VALID_EMAIL}  ${INVALID_PASSWORD}  success  3  2
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
  exit application
  return to login
  login with credentials
  try login again
  login with credentials
  try login again

Test 44
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
  exit application
  return to login
  login with credentials
  try login again
  login with credentials

Test 45
  Set Machine Variables  ${INVALID_EMAIL}  ${INVALID_PASSWORD}  failure  3  1
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
  try login again
  login with credentials
  try login again
  login with credentials
  exit application
  return to login
  login with credentials

Test 46
  Set Machine Variables  ${VALID_EMAIL}  ${VALID_PASSWORD}  failure  1  2
  login with credentials
  logout
  return to login
  login with credentials
  add product to cart  1  2
  logout
  return to login
  login with credentials
  add product to cart  1  2
  proceed to checkout
  process payment  failure
  logout
  return to login
  login with credentials
  add product to cart  1  2
  logout
  return to login
  login with credentials
  add product to cart  1  2
  logout

Test 47
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

Test 48
  Set Machine Variables  ${INVALID_EMAIL}  ${VALID_PASSWORD}  success  2  1
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

Test 49
  Set Machine Variables  ${VALID_EMAIL}  ${INVALID_PASSWORD}  failure  3  2
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
  exit application
  return to login
  login with credentials
  try login again
  login with credentials
  try login again
  login with credentials
  exit application
  return to login

*** Keywords ***
Set Machine Variables
  [Arguments]  ${EMAIL}  ${PASSWORD}  ${PAYMENT}  ${PRODUCT_ID}  ${QUANTITY}
  Set Test Variable  \${EMAIL}
  Set Test Variable  \${PASSWORD}
  Set Test Variable  \${PAYMENT}
  Set Test Variable  \${PRODUCT_ID}
  Set Test Variable  \${QUANTITY}
