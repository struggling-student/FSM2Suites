# ============================================================================
# TEST COVERAGE INFORMATION
# ============================================================================
#
# Covered states (6/8):
#     Browsing
#     CartEditing
#     Checkout
#     Login
#     LoginFailed
#     SessionEnded
#
# Covered actions (10/17):
#     add product to cart  (Browsing -> CartEditing)
#     cancel checkout  (Checkout -> CartEditing)
#     exit application  (LoginFailed -> SessionEnded)
#     login with credentials  (Login -> Browsing)
#     login with credentials  (Login -> LoginFailed)
#     logout  (Browsing -> SessionEnded)
#     logout  (CartEditing -> SessionEnded)
#     proceed to checkout  (CartEditing -> Checkout)
#     return to login  (SessionEnded -> Login)
#     try login again  (LoginFailed -> Login)
#
# Uncovered states (2/8):
#     OrderConfirmed
#     PaymentFailed
#
# Uncovered actions (7/17):
#     cancel order (PaymentFailed -> CartEditing)
#     logout (OrderConfirmed -> SessionEnded)
#     logout (PaymentFailed -> SessionEnded)
#     logout (Checkout -> SessionEnded)
#     process payment (Checkout -> OrderConfirmed)
#     process payment (Checkout -> PaymentFailed)
#     retry payment (PaymentFailed -> Checkout)
#
# ============================================================================

*** Settings ***
Library         ../ShoppingKeywordLibrary.py    browser=chrome    headless=True
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
  add product to cart          1  1
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
  logout
  return to login
  login with credentials
  add product to cart          1  1
  logout
  return to login
  login with credentials
  logout

Test 2
  Set Machine Variables  ${INVALID_EMAIL}  ${INVALID_PASSWORD}  failure  2  1
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
  exit application
  return to login
  login with credentials

Test 3
  Set Machine Variables  ${INVALID_EMAIL}  ${VALID_PASSWORD}  failure  3  2
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
  exit application
  return to login
  login with credentials

Test 4
  Set Machine Variables  ${VALID_EMAIL}  ${INVALID_PASSWORD}  success  3  2
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

Test 5
  Set Machine Variables  ${VALID_EMAIL}  ${INVALID_PASSWORD}  failure  1  2
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

Test 6
  Set Machine Variables  ${INVALID_EMAIL}  ${VALID_PASSWORD}  success  2  2
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
  exit application

Test 7
  Set Machine Variables  ${INVALID_EMAIL}  ${VALID_PASSWORD}  success  1  2
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
  exit application
  return to login

Test 8
  Set Machine Variables  ${VALID_EMAIL}  ${VALID_PASSWORD}  success  2  2
  login with credentials
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
  logout
  return to login
  login with credentials
  add product to cart          2  2
  proceed to checkout

Test 9
  Set Machine Variables  ${VALID_EMAIL}  ${VALID_PASSWORD}  success  3  1
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
  add product to cart          3  1
  logout
  return to login
  login with credentials
  logout
  return to login
  login with credentials
  logout
  return to login
  login with credentials

*** Keywords ***
Set Machine Variables
  [Arguments]  ${EMAIL}  ${PASSWORD}  ${PAYMENT}  ${PRODUCT_ID}  ${QUANTITY}
  Set Test Variable  \${EMAIL}
  Set Test Variable  \${PASSWORD}
  Set Test Variable  \${PAYMENT}
  Set Test Variable  \${PRODUCT_ID}
  Set Test Variable  \${QUANTITY}
