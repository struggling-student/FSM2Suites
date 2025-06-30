import React, { useState, useEffect } from 'react';
import { useApp } from '../context/AppContext';
import ApiService from '../services/api';

function ProductCatalogPage() {
  const { products, setProducts, addToCart, cart, logout, viewCart } = useApp();
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    loadProducts();
  }, []);

  const loadProducts = async () => {
    setIsLoading(true);
    try {
      const result = await ApiService.getProducts();
      setProducts(result.products || []);
    } catch (error) {
      console.error('Failed to load products:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleAddToCart = (product) => {
    addToCart({
      id: product.id,
      name: product.name,
      price: product.price,
      quantity: 1
    });
  };

  const getTotalItems = () => {
    return cart.reduce((total, item) => total + item.quantity, 0);
  };

  return (
    <div className="page product-catalog-page">
      <div className="page-header">
        <h2 data-testid="catalog-title">Product Catalog</h2>
        <div className="page-actions">
          <button
            className="cart-btn"
            data-testid="view-cart-btn"
            onClick={viewCart}
          >
            Cart ({getTotalItems()})
          </button>
          <button
            className="logout-btn"
            data-testid="logout-btn"
            onClick={logout}
          >
            Logout
          </button>
        </div>
      </div>

      {isLoading ? (
        <div className="loading" data-testid="loading">Loading products...</div>
      ) : (
        <div className="products-grid">
          {products.map((product) => (
            <div key={product.id} className="product-card" data-testid={`product-${product.id}`}>
              <h3 className="product-name">{product.name}</h3>
              <p className="product-description">{product.description}</p>
              <p className="product-price">${product.price.toFixed(2)}</p>
              <button
                className="add-to-cart-btn"
                data-testid={`add-to-cart-${product.id}`}
                onClick={() => handleAddToCart(product)}
              >
                Add to Cart
              </button>
            </div>
          ))}
        </div>
      )}

      {products.length === 0 && !isLoading && (
        <div className="no-products" data-testid="no-products">
          No products available
        </div>
      )}
    </div>
  );
}

export default ProductCatalogPage;
