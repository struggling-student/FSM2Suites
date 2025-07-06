# 🚀 Copilot Instructions: Online Shopping App for UI-Based Model-Based Testing

## 💡 Overview

We want to implement a simple but functional web application to demonstrate **model-based testing through the UI** using Selenium. The application is an online shopping platform where users browse products, add items to a cart, proceed to checkout, and complete an order.  

The main goal is to enable automated tests to simulate all FSM paths by interacting with UI elements directly.

---

## 🎯 General Goals

- Create a simple but complete frontend that fully represents FSM states visually and interactively.
- Backend should provide minimal REST API support; no complex authentication or persistence required.
- UI must make **state transitions explicit and testable**, so Selenium can easily detect and verify them.

---

## 🏗️ Backend (API)

### Stack

- Use **Python with FastAPI**.
- Use in-memory data structures only (mock products, session cart).
- No database or real user authentication.

### Key API Endpoints

- `POST /login`: Accepts email and password, returns mock token or success flag.
- `POST /logout`: Invalidates session.
- `GET /products`: Returns mock product list.
- `POST /cart/add`: Add item to cart (id and quantity).
- `POST /cart/remove`: Remove item from cart.
- `POST /cart/update`: Update quantity.
- `GET /cart`: Get cart details.
- `POST /checkout/start`: Start checkout process.
- `POST /checkout/pay`: Simulate payment, accepts forceSuccess flag to simulate success or failure.
- `POST /checkout/cancel`: Cancel checkout.

---

## 💻 Frontend

### Stack

- Use **React** (with Vite or Create React App).
- Plain CSS or minimal styling (no frameworks needed).

### Pages and Visual State Representation

- **Login Page**: Simple form. Once logged in, shows clear indicator (e.g., "State: Browsing").
- **Product Catalog Page**: Displays list of products with "Add to Cart" buttons.
- **Cart Page**: Shows items in the cart, allows updates, and has "Proceed to Checkout" button.
- **Checkout Page**: Simulates shipping/payment, has "Pay" and "Cancel" buttons. Displays explicit message for payment success or failure.
- **Order Summary Page**: Shows summary with "Continue Shopping" and "Logout" buttons.
- **Logout Confirmation / Session Ended**: Explicit page showing "Session Ended" or similar text.

---

## 🔄 State Indication for UI Testing

- Every main state must be **visibly indicated on the UI** (e.g., header text like `State: CartEditing` or `State: Checkout`).
- Each button or action should have clear, unique IDs or data attributes (e.g., `data-testid="add-to-cart"`) so Selenium can reliably locate them.

---

## 🧪 Model-Based Testing Support (Selenium)

- Design UI so each FSM state and transition can be triggered by visible actions (buttons, links).
- Include visible error messages or banners (e.g., "Payment failed. Please retry.") to allow Selenium to verify transitions and negative paths.
- Keep page transitions explicit (no hidden modals or implicit redirects).

---

## ✅ Implementation Style

- Prioritize **clarity over complexity**.
- Use simple React state or Context to maintain FSM states on the frontend.
- Add explicit logs or onscreen text describing the current state to help testing.
- Backend responses should return clear success or failure flags.

---

## 💬 Additional Implementation Notes

- No real authentication; fake login is enough.
- Mock data for products and payment simulation.
- The app must be deployable locally (e.g., `npm run dev` and `uvicorn main:app --reload`).
- No need for database migrations or user management.

---

## 🎁 Example User Journey (FSM-Aligned)

1. User opens app, sees Login Page → logs in → UI updates to "State: Browsing".
2. User views catalog, adds products → "State: CartEditing".
3. User updates cart, proceeds to checkout → "State: Checkout".
4. User pays → success → "State: OrderConfirmed", sees summary.
5. User logs out → "State: Session Ended".

---

**Thank you! This app will be used to demonstrate Selenium-driven model-based testing using explicit UI states.**

