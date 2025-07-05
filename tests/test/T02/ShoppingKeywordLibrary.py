"""
Shopping Cart State Machine Keyword Library for RoboMachine testing.
This library provides keywords to test the shopping cart FSM using Selenium WebDriver.
"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from robot.api import logger
import time


class ShoppingKeywordLibrary:
    """Keywords for testing shopping cart state machine transitions using Selenium."""
    
    def __init__(self):
        self.driver = None
        self.wait = None
        self.base_url = "http://localhost:5173"
        self.current_state = "Login"
        self.authenticated = False
        self.cart_items = []
        
    def setup_shopping_environment(self):
        """Setup Selenium WebDriver and navigate to the application."""
        # Setup Chrome options for headless testing (optional)
        chrome_options = Options()
        # Uncomment the next line for headless mode
        # chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        # Initialize WebDriver
        self.driver = webdriver.Chrome(options=chrome_options)
        self.wait = WebDriverWait(self.driver, 10)
        
        # Navigate to the application
        self.driver.get(self.base_url)
        self.current_state = "Login"
        logger.info(f"Navigated to {self.base_url}")
        
    def teardown_shopping_environment(self):
        """Close the browser and cleanup."""
        if self.driver:
            self.driver.quit()
            logger.info("Browser closed")
    
    # =============================================================================
    # ASSERTION KEYWORDS
    # =============================================================================
    
    def assert_page_displays_login_form(self):
        """Assert that the login form is displayed."""
        try:
            login_title = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='login-title']"))
            )
            email_input = self.driver.find_element(By.CSS_SELECTOR, "[data-testid='email-input']")
            password_input = self.driver.find_element(By.CSS_SELECTOR, "[data-testid='password-input']")
            login_btn = self.driver.find_element(By.CSS_SELECTOR, "[data-testid='login-btn']")
            
            assert login_title.is_displayed(), "Login title not displayed"
            assert email_input.is_displayed(), "Email input not displayed"
            assert password_input.is_displayed(), "Password input not displayed"
            assert login_btn.is_displayed(), "Login button not displayed"
            
            logger.info("Login form is properly displayed")
        except Exception as e:
            raise AssertionError(f"Login form assertion failed: {e}")
    
    def assert_user_is_not_authenticated(self):
        """Assert that user is not authenticated."""
        self.authenticated = False
        # Check that we're on login page or session ended page
        try:
            # Look for login form or session ended message
            login_elements = self.driver.find_elements(By.CSS_SELECTOR, "[data-testid='login-title']")
            session_ended = self.driver.find_elements(By.CSS_SELECTOR, "[data-testid='session-ended-title']")
            
            assert len(login_elements) > 0 or len(session_ended) > 0, "User appears to be authenticated"
            logger.info("User is not authenticated")
        except Exception as e:
            raise AssertionError(f"Authentication assertion failed: {e}")
    
    def assert_user_is_authenticated(self):
        """Assert that user is authenticated."""
        try:
            # Look for user info or any authenticated page elements
            user_info = self.driver.find_elements(By.CSS_SELECTOR, "[data-testid='user-info']")
            catalog_title = self.driver.find_elements(By.CSS_SELECTOR, "[data-testid='catalog-title']")
            cart_title = self.driver.find_elements(By.CSS_SELECTOR, "[data-testid='cart-title']")
            
            assert len(user_info) > 0 or len(catalog_title) > 0 or len(cart_title) > 0, "User is not authenticated"
            self.authenticated = True
            logger.info("User is authenticated")
        except Exception as e:
            raise AssertionError(f"Authentication assertion failed: {e}")
    
    def assert_products_are_displayed(self):
        """Assert that products are displayed in the catalog."""
        try:
            catalog_title = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='catalog-title']"))
            )
            products = self.driver.find_elements(By.CSS_SELECTOR, "[data-testid^='product-']")
            
            assert catalog_title.is_displayed(), "Catalog title not displayed"
            assert len(products) > 0, "No products displayed"
            
            logger.info(f"Products catalog displayed with {len(products)} products")
        except Exception as e:
            raise AssertionError(f"Products assertion failed: {e}")
    
    def assert_cart_is_accessible(self):
        """Assert that cart button is accessible."""
        try:
            cart_btn = self.driver.find_element(By.CSS_SELECTOR, "[data-testid='view-cart-btn']")
            assert cart_btn.is_displayed(), "Cart button not displayed"
            logger.info("Cart is accessible")
        except Exception as e:
            raise AssertionError(f"Cart accessibility assertion failed: {e}")
    
    def assert_cart_contains_items(self):
        """Assert that cart contains items."""
        try:
            cart_items = self.driver.find_elements(By.CSS_SELECTOR, "[data-testid^='cart-item-']")
            assert len(cart_items) > 0, "Cart is empty"
            self.cart_items = cart_items
            logger.info(f"Cart contains {len(cart_items)} items")
        except Exception as e:
            raise AssertionError(f"Cart items assertion failed: {e}")
    
    def assert_cart_total_is_calculated(self):
        """Assert that cart total is properly calculated."""
        try:
            total_element = self.driver.find_element(By.CSS_SELECTOR, "[data-testid='total-price']")
            assert total_element.is_displayed(), "Cart total not displayed"
            
            total_text = total_element.text
            assert "Total:" in total_text, "Total label not found"
            assert "$" in total_text, "Currency symbol not found"
            
            logger.info(f"Cart total displayed: {total_text}")
        except Exception as e:
            raise AssertionError(f"Cart total assertion failed: {e}")
    
    def assert_checkout_form_is_displayed(self):
        """Assert that checkout form is displayed."""
        try:
            checkout_title = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='checkout-title']"))
            )
            address_input = self.driver.find_element(By.CSS_SELECTOR, "[data-testid='address-input']")
            pay_btn = self.driver.find_element(By.CSS_SELECTOR, "[data-testid='pay-success-btn']")
            
            assert checkout_title.is_displayed(), "Checkout title not displayed"
            assert address_input.is_displayed(), "Address input not displayed"
            assert pay_btn.is_displayed(), "Pay button not displayed"
            
            logger.info("Checkout form is displayed")
        except Exception as e:
            raise AssertionError(f"Checkout form assertion failed: {e}")
    
    def assert_order_summary_is_shown(self):
        """Assert that order summary is shown in checkout."""
        try:
            order_total = self.driver.find_element(By.CSS_SELECTOR, "[data-testid='order-total']")
            assert order_total.is_displayed(), "Order total not displayed"
            logger.info("Order summary is shown")
        except Exception as e:
            raise AssertionError(f"Order summary assertion failed: {e}")
    
    def assert_order_confirmation_is_displayed(self):
        """Assert that order confirmation is displayed."""
        try:
            success_message = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='success-message']"))
            )
            order_id = self.driver.find_element(By.CSS_SELECTOR, "[data-testid='order-id']")
            
            assert success_message.is_displayed(), "Success message not displayed"
            assert order_id.is_displayed(), "Order ID not displayed"
            
            logger.info("Order confirmation is displayed")
        except Exception as e:
            raise AssertionError(f"Order confirmation assertion failed: {e}")
    
    def assert_order_details_are_shown(self):
        """Assert that order details are shown."""
        try:
            order_date = self.driver.find_element(By.CSS_SELECTOR, "[data-testid='order-date']")
            order_total = self.driver.find_element(By.CSS_SELECTOR, "[data-testid='order-total']")
            
            assert order_date.is_displayed(), "Order date not displayed"
            assert order_total.is_displayed(), "Order total not displayed"
            
            logger.info("Order details are shown")
        except Exception as e:
            raise AssertionError(f"Order details assertion failed: {e}")
    
    def assert_cart_is_empty(self):
        """Assert that cart is empty."""
        try:
            # Check for empty cart message or no cart items
            empty_cart = self.driver.find_elements(By.CSS_SELECTOR, "[data-testid='empty-cart']")
            cart_items = self.driver.find_elements(By.CSS_SELECTOR, "[data-testid^='cart-item-']")
            
            assert len(empty_cart) > 0 or len(cart_items) == 0, "Cart is not empty"
            logger.info("Cart is empty")
        except Exception as e:
            raise AssertionError(f"Empty cart assertion failed: {e}")
    
    def assert_payment_error_is_displayed(self):
        """Assert that payment error is displayed."""
        try:
            failure_message = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='failure-message']"))
            )
            assert failure_message.is_displayed(), "Payment error message not displayed"
            logger.info("Payment error is displayed")
        except Exception as e:
            raise AssertionError(f"Payment error assertion failed: {e}")
    
    def assert_retry_option_is_available(self):
        """Assert that retry payment option is available."""
        try:
            retry_btn = self.driver.find_element(By.CSS_SELECTOR, "[data-testid='retry-payment-btn']")
            assert retry_btn.is_displayed(), "Retry payment button not displayed"
            logger.info("Retry option is available")
        except Exception as e:
            raise AssertionError(f"Retry option assertion failed: {e}")
    
    def assert_logout_confirmation_is_displayed(self):
        """Assert that logout confirmation is displayed."""
        try:
            session_ended = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='session-ended-message']"))
            )
            assert session_ended.is_displayed(), "Session ended message not displayed"
            logger.info("Logout confirmation is displayed")
        except Exception as e:
            raise AssertionError(f"Logout confirmation assertion failed: {e}")
    
    def assert_login_option_is_available(self):
        """Assert that login option is available."""
        try:
            login_btn = self.driver.find_element(By.CSS_SELECTOR, "[data-testid='back-to-login-btn']")
            assert login_btn.is_displayed(), "Back to login button not displayed"
            logger.info("Login option is available")
        except Exception as e:
            raise AssertionError(f"Login option assertion failed: {e}")
    
    # =============================================================================
    # ACTION KEYWORDS
    # =============================================================================
    
    def login_with_credentials(self, email, password):
        """Login with provided credentials."""
        try:
            # Fill in email
            email_input = self.driver.find_element(By.CSS_SELECTOR, "[data-testid='email-input']")
            email_input.clear()
            email_input.send_keys(email)
            
            # Fill in password
            password_input = self.driver.find_element(By.CSS_SELECTOR, "[data-testid='password-input']")
            password_input.clear()
            password_input.send_keys(password)
            
            # Click login button
            login_btn = self.driver.find_element(By.CSS_SELECTOR, "[data-testid='login-btn']")
            login_btn.click()
            
            # Wait a moment for the response
            time.sleep(1)
            
            # Check if login was successful
            if email == "test@example.com" and password == "password123":
                self.current_state = "Browsing"
                self.authenticated = True
                logger.info("Login successful")
            else:
                self.current_state = "Login"
                self.authenticated = False
                logger.info("Login failed")
                
        except Exception as e:
            logger.error(f"Login action failed: {e}")
            raise
    
    def add_product_to_cart(self, product_id, quantity):
        """Add a product to cart."""
        try:
            # Find and click the add to cart button for the specific product
            add_btn = self.driver.find_element(By.CSS_SELECTOR, f"[data-testid='add-to-cart-{product_id}']")
            add_btn.click()
            
            # Wait for the action to complete
            time.sleep(1)
            
            # Update state
            if product_id in [1, 2, 3, 4, 5, 6] and quantity > 0:
                self.current_state = "CartEditing"
                logger.info(f"Added product {product_id} to cart")
            else:
                logger.info(f"Failed to add product {product_id} to cart")
                
        except Exception as e:
            logger.error(f"Add to cart action failed: {e}")
            # Stay in current state if action fails
    
    def view_cart(self):
        """Navigate to cart view."""
        try:
            cart_btn = self.driver.find_element(By.CSS_SELECTOR, "[data-testid='view-cart-btn']")
            cart_btn.click()
            
            # Wait for navigation
            time.sleep(1)
            
            # Check if cart has items
            cart_items = self.driver.find_elements(By.CSS_SELECTOR, "[data-testid^='cart-item-']")
            if len(cart_items) > 0:
                self.current_state = "CartEditing"
                logger.info("Navigated to cart with items")
            else:
                self.current_state = "Browsing"
                logger.info("Cart is empty, staying in browsing")
                
        except Exception as e:
            logger.error(f"View cart action failed: {e}")
    
    def continue_shopping(self):
        """Continue shopping from cart."""
        try:
            continue_btn = self.driver.find_element(By.CSS_SELECTOR, "[data-testid='continue-shopping-btn']")
            continue_btn.click()
            
            time.sleep(1)
            self.current_state = "Browsing"
            logger.info("Continued shopping")
            
        except Exception as e:
            logger.error(f"Continue shopping action failed: {e}")
    
    def update_item_quantity(self, item_id, quantity):
        """Update quantity of an item in cart."""
        try:
            quantity_input = self.driver.find_element(By.CSS_SELECTOR, f"[data-testid='quantity-{item_id}']")
            quantity_input.clear()
            quantity_input.send_keys(str(quantity))
            
            # Trigger change event (e.g., by pressing Enter or clicking outside)
            quantity_input.send_keys("\n")
            
            time.sleep(1)
            
            # Check resulting state
            cart_items = self.driver.find_elements(By.CSS_SELECTOR, "[data-testid^='cart-item-']")
            if quantity == 0 and len(cart_items) == 0:
                self.current_state = "Browsing"
                logger.info("Item removed, cart empty, moved to browsing")
            elif quantity > 0:
                self.current_state = "CartEditing"
                logger.info(f"Updated item {item_id} quantity to {quantity}")
            else:
                self.current_state = "CartEditing"
                logger.info("Quantity updated, staying in cart")
                
        except Exception as e:
            logger.error(f"Update quantity action failed: {e}")
    
    def remove_item_from_cart(self, item_id):
        """Remove an item from cart."""
        try:
            remove_btn = self.driver.find_element(By.CSS_SELECTOR, f"[data-testid='remove-{item_id}']")
            remove_btn.click()
            
            time.sleep(1)
            
            # Check if cart is now empty
            cart_items = self.driver.find_elements(By.CSS_SELECTOR, "[data-testid^='cart-item-']")
            if len(cart_items) == 0:
                self.current_state = "Browsing"
                logger.info("Item removed, cart empty, moved to browsing")
            else:
                self.current_state = "CartEditing"
                logger.info(f"Removed item {item_id} from cart")
                
        except Exception as e:
            logger.error(f"Remove item action failed: {e}")
    
    def proceed_to_checkout(self):
        """Proceed to checkout from cart."""
        try:
            checkout_btn = self.driver.find_element(By.CSS_SELECTOR, "[data-testid='checkout-btn']")
            checkout_btn.click()
            
            time.sleep(1)
            self.current_state = "Checkout"
            logger.info("Proceeded to checkout")
            
        except Exception as e:
            logger.error(f"Proceed to checkout action failed: {e}")
    
    def process_payment(self, payment_type):
        """Process payment (success or failure)."""
        try:
            # Fill in required shipping information first
            self._fill_shipping_info()
            
            # Choose payment button based on type
            if payment_type == "success":
                pay_btn = self.driver.find_element(By.CSS_SELECTOR, "[data-testid='pay-success-btn']")
                pay_btn.click()
                
                time.sleep(2)  # Wait for payment processing
                self.current_state = "OrderConfirmed"
                logger.info("Payment processed successfully")
                
            elif payment_type == "failure":
                pay_btn = self.driver.find_element(By.CSS_SELECTOR, "[data-testid='pay-fail-btn']")
                pay_btn.click()
                
                time.sleep(2)  # Wait for payment processing
                self.current_state = "PaymentFailed"
                logger.info("Payment failed")
                
        except Exception as e:
            logger.error(f"Process payment action failed: {e}")
    
    def cancel_checkout(self):
        """Cancel checkout process."""
        try:
            cancel_btn = self.driver.find_element(By.CSS_SELECTOR, "[data-testid='cancel-checkout-btn']")
            cancel_btn.click()
            
            time.sleep(1)
            
            # Check if cart has items to determine next state
            cart_items = self.driver.find_elements(By.CSS_SELECTOR, "[data-testid^='cart-item-']")
            if len(cart_items) > 0:
                self.current_state = "CartEditing"
                logger.info("Checkout cancelled, returned to cart")
            else:
                self.current_state = "Browsing"
                logger.info("Checkout cancelled, cart empty, moved to browsing")
                
        except Exception as e:
            logger.error(f"Cancel checkout action failed: {e}")
    
    def retry_payment(self):
        """Retry payment from failed payment state."""
        try:
            retry_btn = self.driver.find_element(By.CSS_SELECTOR, "[data-testid='retry-payment-btn']")
            retry_btn.click()
            
            time.sleep(1)
            self.current_state = "Checkout"
            logger.info("Retrying payment")
            
        except Exception as e:
            logger.error(f"Retry payment action failed: {e}")
    
    def cancel_order(self):
        """Cancel order from failed payment state."""
        try:
            cancel_btn = self.driver.find_element(By.CSS_SELECTOR, "[data-testid='cancel-order-btn']")
            cancel_btn.click()
            
            time.sleep(1)
            
            # Check cart state
            cart_items = self.driver.find_elements(By.CSS_SELECTOR, "[data-testid^='cart-item-']")
            if len(cart_items) > 0:
                self.current_state = "CartEditing"
                logger.info("Order cancelled, returned to cart")
            else:
                self.current_state = "Browsing"
                logger.info("Order cancelled, moved to browsing")
                
        except Exception as e:
            logger.error(f"Cancel order action failed: {e}")
    
    def logout(self):
        """Logout from any authenticated state."""
        try:
            logout_btn = self.driver.find_element(By.CSS_SELECTOR, "[data-testid='logout-btn']")
            logout_btn.click()
            
            time.sleep(1)
            self.current_state = "SessionEnded"
            self.authenticated = False
            logger.info("User logged out")
            
        except Exception as e:
            logger.error(f"Logout action failed: {e}")
    
    def return_to_login(self):
        """Return to login from session ended state."""
        try:
            login_btn = self.driver.find_element(By.CSS_SELECTOR, "[data-testid='back-to-login-btn']")
            login_btn.click()
            
            time.sleep(1)
            self.current_state = "Login"
            logger.info("Returned to login")
            
        except Exception as e:
            logger.error(f"Return to login action failed: {e}")
    
    # =============================================================================
    # HELPER METHODS
    # =============================================================================
    
    def _fill_shipping_info(self):
        """Fill in shipping information for checkout."""
        try:
            address_input = self.driver.find_element(By.CSS_SELECTOR, "[data-testid='address-input']")
            city_input = self.driver.find_element(By.CSS_SELECTOR, "[data-testid='city-input']")
            zipcode_input = self.driver.find_element(By.CSS_SELECTOR, "[data-testid='zipcode-input']")
            country_input = self.driver.find_element(By.CSS_SELECTOR, "[data-testid='country-input']")
            
            address_input.clear()
            address_input.send_keys("123 Test Street")
            
            city_input.clear()
            city_input.send_keys("Test City")
            
            zipcode_input.clear()
            zipcode_input.send_keys("12345")
            
            country_input.clear()
            country_input.send_keys("Test Country")
            
            logger.info("Shipping information filled")
            
        except Exception as e:
            logger.error(f"Failed to fill shipping info: {e}")
    
    # =============================================================================
    # CONDITIONS FOR ROBOMACHINE
    # =============================================================================
    
    def cart_has_items(self):
        """Check if cart has items (used in RoboMachine conditions)."""
        try:
            cart_items = self.driver.find_elements(By.CSS_SELECTOR, "[data-testid^='cart-item-']")
            return len(cart_items) > 0
        except:
            return False
    
    def cart_becomes_empty(self):
        """Check if cart becomes empty after an action."""
        return not self.cart_has_items()
    
    def cart_has_other_items(self):
        """Check if cart has other items after removing one."""
        return self.cart_has_items()
    
    def cart_is_empty(self):
        """Check if cart is empty."""
        return not self.cart_has_items()
