# Shopping App Frontend

A React-based shopping application designed for model-based testing with Selenium.

## Features

- **FSM State Management**: Clear visual indication of current application state
- **Test-Friendly UI**: All buttons and elements have unique `data-testid` attributes
- **Complete Shopping Flow**: Login → Browse → Cart → Checkout → Order Confirmation
- **Error Handling**: Payment failure simulation and error display
- **Responsive Design**: Works on desktop and mobile devices

## States

The application follows these FSM states:

1. **Login**: User authentication page
2. **Browsing**: Product catalog view
3. **CartEditing**: Shopping cart management
4. **Checkout**: Order processing and payment
5. **OrderConfirmed**: Successful order completion
6. **PaymentFailed**: Payment failure handling
7. **SessionEnded**: Logout confirmation

## Development

```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build
```

## Testing

The application is designed with Selenium testing in mind:

- State indicators are clearly visible in the header
- All interactive elements have `data-testid` attributes
- Error messages and success states are prominently displayed
- Payment can be forced to succeed or fail for testing negative paths

## Demo Credentials

- Email: `test@example.com`
- Password: `password123`

## API Integration

The frontend expects a backend API running on `http://localhost:8000` with the following endpoints:

- `POST /login` - User authentication
- `GET /products` - Product catalog
- `POST /cart/add` - Add items to cart
- `POST /cart/remove` - Remove items from cart
- `POST /cart/update` - Update cart quantities
- `GET /cart` - Get cart contents
- `POST /checkout/start` - Begin checkout process
- `POST /checkout/pay` - Process payment
- `POST /checkout/cancel` - Cancel checkout
- `POST /logout` - User logout+ Vite

This template provides a minimal setup to get React working in Vite with HMR and some ESLint rules.

Currently, two official plugins are available:

- [@vitejs/plugin-react](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react) uses [Babel](https://babeljs.io/) for Fast Refresh
- [@vitejs/plugin-react-swc](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react-swc) uses [SWC](https://swc.rs/) for Fast Refresh

## Expanding the ESLint configuration

If you are developing a production application, we recommend using TypeScript with type-aware lint rules enabled. Check out the [TS template](https://github.com/vitejs/vite/tree/main/packages/create-vite/template-react-ts) for information on how to integrate TypeScript and [`typescript-eslint`](https://typescript-eslint.io) in your project.
