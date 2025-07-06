from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import uuid
from datetime import datetime

app = FastAPI(title="Shopping App API", version="1.0.0")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory data stores
sessions = {}  # session_id -> user_data
products_db = [
    {
        "id": 1,
        "name": "Laptop Pro",
        "description": "High-performance laptop for professionals",
        "price": 1299.99
    },
    {
        "id": 2,
        "name": "Wireless Headphones",
        "description": "Premium noise-cancelling headphones",
        "price": 249.99
    },
    {
        "id": 3,
        "name": "Smart Watch",
        "description": "Advanced fitness and health tracking",
        "price": 399.99
    },
    {
        "id": 4,
        "name": "Tablet",
        "description": "Portable tablet for work and entertainment",
        "price": 599.99
    },
    {
        "id": 5,
        "name": "Gaming Mouse",
        "description": "Precision gaming mouse with RGB lighting",
        "price": 79.99
    },
    {
        "id": 6,
        "name": "Mechanical Keyboard",
        "description": "Premium mechanical keyboard for typing",
        "price": 149.99
    }
]
carts = {}  # session_id -> cart_items

# Pydantic models
class LoginRequest(BaseModel):
    email: str
    password: str

class LoginResponse(BaseModel):
    success: bool
    message: str = ""
    token: str = ""
    user: dict = {}

class Product(BaseModel):
    id: int
    name: str
    description: str
    price: float

class ProductsResponse(BaseModel):
    products: List[Product]

class CartItem(BaseModel):
    id: int
    quantity: int

class CartAddRequest(BaseModel):
    id: int
    quantity: int

class CartRemoveRequest(BaseModel):
    id: int

class CartUpdateRequest(BaseModel):
    id: int
    quantity: int

class CartResponse(BaseModel):
    items: List[dict]
    total: float

class CheckoutStartResponse(BaseModel):
    success: bool
    message: str = ""

class PaymentRequest(BaseModel):
    forceSuccess: bool = True

class PaymentResponse(BaseModel):
    success: bool
    message: str = ""
    orderId: str = ""

class GenericResponse(BaseModel):
    success: bool
    message: str = ""

# Helper functions
def get_session_id() -> str:
    """Generate a new session ID"""
    return str(uuid.uuid4())

def get_current_session():
    """Mock session management - in real app would use proper authentication"""
    # For demo purposes, we'll use a simple session management
    # In a real app, this would validate JWT tokens or session cookies
    return "demo_session"

@app.get("/")
def root():
    return {"message": "Shopping App API", "version": "1.0.0"}

@app.get("/health")
def health():
    """Health check endpoint for testing"""
    return {"status": "healthy", "service": "shopping-api"}

@app.post("/login", response_model=LoginResponse)
def login(request: LoginRequest):
    """Mock login endpoint - accepts any email/password"""
    
    # Simple validation
    if not request.email or not request.password:
        return LoginResponse(
            success=False,
            message="Email and password are required"
        )
    
    # Mock validation - for demo, accept specific credentials or any valid email
    if request.email == "test@example.com" and request.password == "password123":
        # Create session
        session_id = get_session_id()
        user_data = {
            "email": request.email,
            "session_id": session_id
        }
        sessions[session_id] = user_data
        carts[session_id] = []
        
        return LoginResponse(
            success=True,
            message="Login successful",
            token=session_id,
            user={"email": request.email}
        )
    else:
        return LoginResponse(
            success=False,
            message="Invalid email or password"
        )

@app.post("/logout", response_model=GenericResponse)
def logout():
    """Mock logout endpoint"""
    session_id = get_current_session()
    
    # Clean up session data
    if session_id in sessions:
        del sessions[session_id]
    if session_id in carts:
        del carts[session_id]
    
    return GenericResponse(
        success=True,
        message="Logged out successfully"
    )

@app.get("/products", response_model=ProductsResponse)
def get_products():
    """Get list of available products"""
    return ProductsResponse(
        products=[Product(**product) for product in products_db]
    )

@app.post("/cart/add", response_model=GenericResponse)
def add_to_cart(request: CartAddRequest):
    """Add item to cart"""
    session_id = get_current_session()
    
    # Find the product
    product = next((p for p in products_db if p["id"] == request.id), None)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Initialize cart if doesn't exist
    if session_id not in carts:
        carts[session_id] = []
    
    # Check if item already in cart
    existing_item = next((item for item in carts[session_id] if item["id"] == request.id), None)
    
    if existing_item:
        existing_item["quantity"] += request.quantity
    else:
        cart_item = {
            "id": product["id"],
            "name": product["name"],
            "price": product["price"],
            "quantity": request.quantity
        }
        carts[session_id].append(cart_item)
    
    return GenericResponse(
        success=True,
        message=f"Added {request.quantity} {product['name']}(s) to cart"
    )

@app.post("/cart/remove", response_model=GenericResponse)
def remove_from_cart(request: CartRemoveRequest):
    """Remove item from cart"""
    session_id = get_current_session()
    
    if session_id not in carts:
        return GenericResponse(
            success=False,
            message="Cart not found"
        )
    
    # Remove item from cart
    carts[session_id] = [item for item in carts[session_id] if item["id"] != request.id]
    
    return GenericResponse(
        success=True,
        message="Item removed from cart"
    )

@app.post("/cart/update", response_model=GenericResponse)
def update_cart(request: CartUpdateRequest):
    """Update cart item quantity"""
    session_id = get_current_session()
    
    if session_id not in carts:
        return GenericResponse(
            success=False,
            message="Cart not found"
        )
    
    # Find and update item
    for item in carts[session_id]:
        if item["id"] == request.id:
            if request.quantity <= 0:
                # Remove item if quantity is 0 or negative
                carts[session_id] = [i for i in carts[session_id] if i["id"] != request.id]
            else:
                item["quantity"] = request.quantity
            
            return GenericResponse(
                success=True,
                message="Cart updated"
            )
    
    return GenericResponse(
        success=False,
        message="Item not found in cart"
    )

@app.get("/cart", response_model=CartResponse)
def get_cart():
    """Get current cart contents"""
    session_id = get_current_session()
    
    if session_id not in carts:
        return CartResponse(items=[], total=0.0)
    
    cart_items = carts[session_id]
    total = sum(item["price"] * item["quantity"] for item in cart_items)
    
    return CartResponse(
        items=cart_items,
        total=total
    )

@app.post("/checkout/start", response_model=CheckoutStartResponse)
def start_checkout():
    """Start checkout process"""
    session_id = get_current_session()
    
    if session_id not in carts or not carts[session_id]:
        return CheckoutStartResponse(
            success=False,
            message="Cart is empty"
        )
    
    return CheckoutStartResponse(
        success=True,
        message="Checkout started"
    )

@app.post("/checkout/pay", response_model=PaymentResponse)
def process_payment(request: PaymentRequest):
    """Process payment - can be forced to succeed or fail"""
    session_id = get_current_session()
    
    if session_id not in carts or not carts[session_id]:
        return PaymentResponse(
            success=False,
            message="Cart is empty"
        )
    
    if request.forceSuccess:
        # Generate order ID
        order_id = f"ORD{datetime.now().strftime('%Y%m%d%H%M%S')}{uuid.uuid4().hex[:6].upper()}"
        
        # Clear cart after successful payment
        carts[session_id] = []
        
        return PaymentResponse(
            success=True,
            message="Payment processed successfully",
            orderId=order_id
        )
    else:
        return PaymentResponse(
            success=False,
            message="Payment failed. Please try again."
        )

@app.post("/checkout/cancel", response_model=GenericResponse)
def cancel_checkout():
    """Cancel checkout process"""
    return GenericResponse(
        success=True,
        message="Checkout cancelled"
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
