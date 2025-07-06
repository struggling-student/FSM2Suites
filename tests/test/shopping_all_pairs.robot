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
# Covered states (7/8):
#     Browsing
#     CartEditing
#     Checkout
#     Login
#     LoginFailed
#     OrderConfirmed
#     SessionEnded
#
# Covered actions (13/17):
#     add product to cart  (Browsing -> CartEditing)
#     logout  (Browsing -> SessionEnded)
#     logout  (CartEditing -> SessionEnded)
#     proceed to checkout  (CartEditing -> Checkout)
#     cancel checkout  (Checkout -> CartEditing)
#     logout  (Checkout -> SessionEnded)
#     process payment  (Checkout -> OrderConfirmed)
#     login with credentials  (Login -> LoginFailed)
#     login with credentials  (Login -> Browsing)
#     exit application  (LoginFailed -> SessionEnded)
#     try login again  (LoginFailed -> Login)
#     logout  (OrderConfirmed -> SessionEnded)
#     return to login  (SessionEnded -> Login)
#
# Uncovered states (1/8):
#     PaymentFailed
#
# Uncovered actions (4/17):
#     process payment (Checkout -> PaymentFailed)
#     cancel order (PaymentFailed -> CartEditing)
#     logout (PaymentFailed -> SessionEnded)
#     retry payment (PaymentFailed -> Checkout)
#
# ============================================================================

*** Test Cases ***
Test 1
  Set Machine Variables  ${VALID_EMAIL}  ${VALID_PASSWORD}  success  1  1
  login with credentials
  add product to cart  1  1
  proceed to checkout
  cancel checkout
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
  add product to cart  1  1
  proceed to checkout
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

Test 3
  Set Machine Variables  ${INVALID_EMAIL}  ${VALID_PASSWORD}  failure  3  2
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

Test 4
  Set Machine Variables  ${VALID_EMAIL}  ${INVALID_PASSWORD}  success  3  2
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
  try login again
  login with credentials
  try login again
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

Test 6
  Set Machine Variables  ${INVALID_EMAIL}  ${VALID_PASSWORD}  success  2  2
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

Test 7
  Set Machine Variables  ${INVALID_EMAIL}  ${VALID_PASSWORD}  success  1  2
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
  exit application
  return to login

Test 8
  Set Machine Variables  ${VALID_EMAIL}  ${VALID_PASSWORD}  success  2  2
  login with credentials
  logout
  return to login
  login with credentials
  add product to cart  2  2
  proceed to checkout
  logout
  return to login
  login with credentials
  add product to cart  2  2
  logout
  return to login
  login with credentials
  add product to cart  2  2
  proceed to checkout
  logout
  return to login
  login with credentials
  logout
  return to login

Test 9
  Set Machine Variables  ${VALID_EMAIL}  ${VALID_PASSWORD}  success  3  1
  login with credentials
  add product to cart  3  1
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
  logout
  return to login
  login with credentials
  add product to cart  3  1
  proceed to checkout
  cancel checkout

*** Keywords ***
Set Machine Variables
  [Arguments]  ${EMAIL}  ${PASSWORD}  ${PAYMENT}  ${PRODUCT_ID}  ${QUANTITY}
  Set Test Variable  \${EMAIL}
  Set Test Variable  \${PASSWORD}
  Set Test Variable  \${PAYMENT}
  Set Test Variable  \${PRODUCT_ID}
  Set Test Variable  \${QUANTITY}
