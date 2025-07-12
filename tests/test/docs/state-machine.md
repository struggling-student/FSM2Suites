---
title: Shopping App State Machine
---
stateDiagram-v2
    classDef errorState fill:#ffebee,stroke:#c62828,color:#000
    classDef successState fill:#e8f5e8,stroke:#2e7d32,color:#000
    classDef activeState fill:#e3f2fd,stroke:#1976d2,color:#000
    classDef neutralState fill:#f5f5f5,stroke:#757575,color:#000

    %% Define states with descriptions
    Login: Login
    LoginFailed: LoginFailed
    Browsing: Browsing
    CartEditing: CartEditing
    Checkout: Checkout
    OrderConfirmed: OrderConfirmed
    PaymentFailed: PaymentFailed
    SessionEnded: SessionEnded

    %% Initial state
    [*] --> Login

    %% Login transitions
    Login --> Browsing: login with credentials<br/>(valid email & password)
    Login --> LoginFailed: login with credentials<br/>(invalid credentials)

    %% LoginFailed transitions
    LoginFailed --> Login: try login again
    LoginFailed --> SessionEnded: exit application

    %% Browsing transitions
    Browsing --> CartEditing: add product to cart
    Browsing --> SessionEnded: logout

    %% CartEditing transitions
    CartEditing --> Checkout: proceed to checkout
    CartEditing --> SessionEnded: logout

    %% Checkout transitions
    Checkout --> OrderConfirmed: process payment<br/>(success)
    Checkout --> PaymentFailed: process payment<br/>(failure)
    Checkout --> CartEditing: cancel checkout
    Checkout --> SessionEnded: logout

    %% OrderConfirmed transitions
    OrderConfirmed --> SessionEnded: logout

    %% PaymentFailed transitions
    PaymentFailed --> Checkout: retry payment
    PaymentFailed --> CartEditing: cancel order
    PaymentFailed --> SessionEnded: logout

    %% SessionEnded transitions
    SessionEnded --> Login: return to login
    SessionEnded --> [*]

    %% Apply styles to states
    class Login,Browsing,CartEditing,Checkout activeState
    class LoginFailed,PaymentFailed errorState
    class OrderConfirmed successState
    class SessionEnded neutralState
