*** Settings ***
Library         ShoppingKeywordLibrary.py    browser=chrome    headless=True
Test Setup      Setup Shopping Environment
Test Teardown   Teardown Shopping Environment

*** Variables ***
${VALID_EMAIL}      test@example.com
${VALID_PASSWORD}   password123

*** Test Cases ***
Test Basic Login Flow
    [Documentation]    Test basic login functionality
    Assert Page Displays Login Form
    Assert User Is Not Authenticated
    Login With Credentials Manual    ${VALID_EMAIL}    ${VALID_PASSWORD}
    Assert User Is Authenticated
    Assert Products Are Displayed

Test Add Product To Cart
    [Documentation]    Test adding a product to cart
    Login With Credentials Manual    ${VALID_EMAIL}    ${VALID_PASSWORD}
    Assert Products Are Displayed
    Add Product To Cart    1    1
    Assert Cart Contains Items
    View Cart
    Assert Cart Total Is Calculated

Test Complete Shopping Flow
    [Documentation]    Test complete shopping workflow
    Login With Credentials Manual    ${VALID_EMAIL}    ${VALID_PASSWORD}
    
    # Browse and add product
    Add Product To Cart    1    1
    View Cart
    Assert Cart Contains Items
    
    # Proceed to checkout
    Proceed To Checkout
    Assert Checkout Form Is Displayed
    Assert Order Summary Is Shown
    
    # Complete payment
    Process Payment    success
    Assert Order Confirmation Is Displayed
    Assert Order Details Are Shown
    Assert Cart Is Empty

Test Payment Failure Flow
    [Documentation]    Test payment failure and retry
    Login With Credentials Manual    ${VALID_EMAIL}    ${VALID_PASSWORD}
    
    # Add product and checkout
    Add Product To Cart    2    1
    View Cart
    Proceed To Checkout
    
    # Fail payment
    Process Payment    failure
    Assert Payment Error Is Displayed
    Assert Retry Option Is Available
    
    # Retry payment successfully
    Retry Payment
    Process Payment    success
    Assert Order Confirmation Is Displayed

Test Logout Flow
    [Documentation]    Test logout functionality
    Login With Credentials Manual    ${VALID_EMAIL}    ${VALID_PASSWORD}
    
    # Logout from browsing state
    Logout
    Assert Logout Confirmation Is Displayed
    Assert Login Option Is Available
    
    # Return to login
    Return To Login
    Assert Page Displays Login Form
