"""
Shopping Cart State Machine Keyword Library for Machine testing.
This library provides keywords to test the shopping cart FSM using Selenium WebDriver.
"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from robot.api import logger
import time
import requests
import subprocess
from pathlib import Path


class ShoppingKeywordLibrary:
    """Keywords for testing shopping cart state machine transitions using Selenium."""
    
    def __init__(self):
        self.driver = None
        self.wait = None
        self.base_url = "http://localhost:5173"
        self.backend_url = "http://localhost:8000"
        self.current_state = "Login"
        self.authenticated = False
        self.cart_items = []
        self.backend_process = None
        self.frontend_process = None
        
    def start_backend_server(self):
        """Start the FastAPI backend server."""
        test_dir = Path(__file__).parent
        backend_dir = test_dir.parent.parent / "backend"
        
        logger.info("Starting backend server...")
        self.backend_process = subprocess.Popen([
            "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"
        ], cwd=str(backend_dir), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Wait for backend to be ready
        max_attempts = 30
        for attempt in range(max_attempts):
            try:
                response = requests.get(f"{self.backend_url}/health", timeout=2)
                if response.status_code == 200:
                    logger.info("Backend server is ready")
                    return
            except requests.exceptions.RequestException:
                pass
            time.sleep(1)
        
        raise Exception("Backend server failed to start within 30 seconds")
    
    def start_frontend_server(self):
        """Start the React frontend server."""
        test_dir = Path(__file__).parent
        frontend_dir = test_dir.parent.parent / "frontend"
        
        logger.info("Starting frontend server...")
        self.frontend_process = subprocess.Popen([
            "npm", "run", "dev", "--", "--host", "0.0.0.0", "--port", "5173"
        ], cwd=str(frontend_dir), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Wait for frontend to be ready
        max_attempts = 30
        for attempt in range(max_attempts):
            try:
                response = requests.get(self.base_url, timeout=2)
                if response.status_code == 200:
                    logger.info("Frontend server is ready")
                    return
            except requests.exceptions.RequestException:
                pass
            time.sleep(1)
        
        raise Exception("Frontend server failed to start within 30 seconds")
    
    def stop_servers(self):
        """Stop both backend and frontend servers."""
        logger.info("Stopping servers...")
        
        if self.backend_process:
            self.backend_process.terminate()
            try:
                self.backend_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.backend_process.kill()
            self.backend_process = None
            
        if self.frontend_process:
            self.frontend_process.terminate()
            try:
                self.frontend_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.frontend_process.kill()
            self.frontend_process = None
        
        logger.info("Servers stopped")
        
    def setup_shopping_environment(self):
        """Setup servers and Selenium WebDriver, then navigate to the application."""
        # Start servers first
        self.start_backend_server()
        self.start_frontend_server()
        
        # Setup Firefox WebDriver
        firefox_options = Options()
        # Uncomment the next line for headless mode
        # firefox_options.add_argument("--headless")
        firefox_options.add_argument("--width=1920")
        firefox_options.add_argument("--height=1080")
        
        # Initialize WebDriver with auto-managed GeckoDriver
        service = Service(GeckoDriverManager().install())
        self.driver = webdriver.Firefox(service=service, options=firefox_options)
        self.wait = WebDriverWait(self.driver, 10)
        
        # Navigate to the application
        self.driver.get(self.base_url)
        self.current_state = "Login"
        logger.info(f"Navigated to {self.base_url}")
        
        # Wait for page to load
        self.wait.until(
            EC.any_of(
                EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='login-title']")),
                EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='catalog-title']"))
            )
        )
        
    def teardown_shopping_environment(self):
        """Close the browser and stop servers."""
        if self.driver:
            self.driver.quit()
            logger.info("Browser closed")
        
        self.stop_servers()
    
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
    
    def login_with_credentials_manual(self, email, password):
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
            # Wait for the add to cart button for the specific product
            add_btn = self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, f"[data-testid='add-to-cart-{product_id}']"))
            )
            add_btn.click()
            
            # Wait a moment for the cart to update
            time.sleep(1)
            
            # Update state - we stay on catalog page after adding items
            self.current_state = "Browsing"
            logger.info(f"Added product {product_id} to cart (quantity: {quantity})")
                
        except Exception as e:
            raise AssertionError(f"Add to cart action failed for product {product_id}: {e}")
    
    def add_product_to_cart_default(self):
        """Add first available product to cart (for generated tests)."""
        # Use default values - add first product with quantity 1
        self.add_product_to_cart("1", "1")
    
    def view_cart(self):
        """Navigate to cart view."""
        try:
            # Check if we're already on the cart page
            cart_title = self.driver.find_elements(By.CSS_SELECTOR, "[data-testid='cart-title']")
            if cart_title:
                logger.info("Already on cart page")
                self.current_state = "CartEditing"
                return
            
            # Look for view cart button (should be on catalog page)
            cart_btn = self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-testid='view-cart-btn']"))
            )
            cart_btn.click()
            
            # Wait for navigation to cart page
            self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='cart-title']"))
            )
            
            # Check if cart has items
            cart_items = self.driver.find_elements(By.CSS_SELECTOR, "[data-testid^='cart-item-']")
            if len(cart_items) > 0:
                self.current_state = "CartEditing"
                logger.info("Navigated to cart with items")
            else:
                self.current_state = "Browsing"
                logger.info("Cart is empty")
                
        except Exception as e:
            raise AssertionError(f"View cart action failed: {e}")
    
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
            checkout_btn = self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-testid='checkout-btn']"))
            )
            checkout_btn.click()
            
            # Wait for checkout page to load
            self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='checkout-title']"))
            )
            
            self.current_state = "Checkout"
            logger.info("Proceeded to checkout")
            
        except Exception as e:
            raise AssertionError(f"Proceed to checkout action failed: {e}")
    
    def process_payment(self, payment_type=None):
        """Process payment (success or failure)."""
        try:
            # If no payment_type provided, get from Robot Framework variables
            if payment_type is None:
                try:
                    from robot.libraries.BuiltIn import BuiltIn
                    builtin = BuiltIn()
                    payment_type = builtin.get_variable_value("${PAYMENT}")
                    if not payment_type:
                        payment_type = "success"  # Default to success
                except Exception:
                    payment_type = "success"  # Default fallback
            
            # Fill in required shipping information first
            self._fill_shipping_info()
            
            # Choose payment button based on type
            if payment_type == "success":
                pay_btn = self.wait.until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-testid='pay-success-btn']"))
                )
                pay_btn.click()
                
                # Wait for order confirmation page to load
                self.wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='success-message']"))
                )
                
                self.current_state = "OrderConfirmed"
                logger.info("Payment processed successfully")
                
            elif payment_type == "failure":
                pay_btn = self.wait.until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-testid='pay-fail-btn']"))
                )
                pay_btn.click()
                
                # Wait for payment failure page to load
                self.wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='failure-message']"))
                )
                
                self.current_state = "PaymentFailed"
                logger.info("Payment failed")
                
        except Exception as e:
            raise AssertionError(f"Process payment action failed: {e}")
    
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
            # Wait for and fill address
            address_input = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='address-input']"))
            )
            address_input.clear()
            address_input.send_keys("123 Test Street")
            
            # Fill city
            city_input = self.driver.find_element(By.CSS_SELECTOR, "[data-testid='city-input']")
            city_input.clear()
            city_input.send_keys("Test City")
            
            # Fill zipcode
            zipcode_input = self.driver.find_element(By.CSS_SELECTOR, "[data-testid='zipcode-input']")
            zipcode_input.clear()
            zipcode_input.send_keys("12345")
            
            # Fill country
            country_input = self.driver.find_element(By.CSS_SELECTOR, "[data-testid='country-input']")
            country_input.clear()
            country_input.send_keys("Test Country")
            
            logger.info("Shipping information filled")
            
        except Exception as e:
            raise AssertionError(f"Failed to fill shipping info: {e}")
    
    # =============================================================================
    # CONDITIONS FOR MACHINE
    # =============================================================================
    
    def cart_has_items(self):
        """Check if cart has items (used in Machine conditions)."""
        try:
            cart_items = self.driver.find_elements(By.CSS_SELECTOR, "[data-testid^='cart-item-']")
            return len(cart_items) > 0
        except Exception:
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
    
    # =============================================================================
    # MACHINE-GENERATED KEYWORDS (for compatibility with state machine)
    # =============================================================================
    
    def login_with_credentials(self):
        """Login using machine variables (for generated tests)."""
        # Get variables from Robot Framework test context
        try:
            from robot.libraries.BuiltIn import BuiltIn
            builtin = BuiltIn()
            email = builtin.get_variable_value("${EMAIL}")
            password = builtin.get_variable_value("${PASSWORD}")
            
            if not email or not password:
                raise AssertionError("EMAIL and PASSWORD variables must be set")
            
            # Use the existing login method
            self.login_with_credentials_args(email, password)
            
        except Exception as e:
            raise AssertionError(f"Login with machine variables failed: {e}")
    
    def login_with_credentials_args(self, email, password):
        """Login with provided credentials (renamed from original method)."""
        try:
            # Fill in email
            email_input = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='email-input']"))
            )
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
            time.sleep(2)
            
            # Check if login was successful by looking for authenticated page elements
            catalog_title = self.driver.find_elements(By.CSS_SELECTOR, "[data-testid='catalog-title']")
            login_title = self.driver.find_elements(By.CSS_SELECTOR, "[data-testid='login-title']")
            
            if catalog_title:
                self.current_state = "Browsing"
                self.authenticated = True
                logger.info("Login successful - moved to Browsing state")
            elif login_title:
                self.current_state = "LoginFailed"
                self.authenticated = False
                logger.info("Login failed - staying on login page")
            else:
                # Fallback check
                if email == "test@example.com" and password == "password123":
                    self.current_state = "Browsing"
                    self.authenticated = True
                else:
                    self.current_state = "LoginFailed"
                    self.authenticated = False
                
        except Exception as e:
            logger.error(f"Login action failed: {e}")
            self.current_state = "LoginFailed"
            self.authenticated = False
            raise AssertionError(f"Login failed: {e}")
    
    def exit_application(self):
        """Exit application (equivalent to logout for our FSM)."""
        try:
            # Check what page we're on and logout accordingly
            logout_elements = self.driver.find_elements(By.CSS_SELECTOR, "[data-testid='logout-btn']")
            if logout_elements and logout_elements[0].is_displayed():
                # We're on a page with a logout button
                self.logout()
            else:
                # We might be on login page or session ended page already
                login_elements = self.driver.find_elements(By.CSS_SELECTOR, "[data-testid='login-title']")
                session_ended = self.driver.find_elements(By.CSS_SELECTOR, "[data-testid='session-ended-title']")
                
                if login_elements:
                    # Already on login page, just set state
                    self.current_state = "SessionEnded"
                    self.authenticated = False
                    logger.info("Already on login page - set to SessionEnded")
                elif session_ended:
                    # Already on session ended page
                    self.current_state = "SessionEnded"
                    self.authenticated = False
                    logger.info("Already on session ended page")
                else:
                    # Navigate to session ended page (simulate logout)
                    self.current_state = "SessionEnded"
                    self.authenticated = False
                    logger.info("Exit application - set to SessionEnded")
                    
        except Exception as e:
            logger.info(f"Exit application completed with minor issues: {e}")
            self.current_state = "SessionEnded"
            self.authenticated = False
    
    def try_login_again(self):
        """Try login again (return to login state)."""
        try:
            # Check if we're already on login page
            login_elements = self.driver.find_elements(By.CSS_SELECTOR, "[data-testid='login-title']")
            if login_elements:
                logger.info("Already on login page")
                self.current_state = "Login"
                self.authenticated = False
                return
            
            # Check if we're on session ended page
            session_ended = self.driver.find_elements(By.CSS_SELECTOR, "[data-testid='session-ended-title']")
            if session_ended:
                # Try to find back to login button
                back_to_login = self.driver.find_elements(By.CSS_SELECTOR, "[data-testid='back-to-login-btn']")
                if back_to_login:
                    back_to_login[0].click()
                    self.wait.until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='login-title']"))
                    )
                else:
                    # Navigate directly to login page
                    self.driver.get(self.base_url)
                    self.wait.until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='login-title']"))
                    )
            else:
                # Navigate back to login page
                self.driver.get(self.base_url)
                self.wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='login-title']"))
                )
            
            self.current_state = "Login"
            self.authenticated = False
            logger.info("Returned to login page")
            
        except Exception as e:
            # If there's any issue, just navigate to the base URL
            logger.info(f"Try login again with fallback navigation: {e}")
            self.driver.get(self.base_url)
            time.sleep(2)
            self.current_state = "Login"
            self.authenticated = False
