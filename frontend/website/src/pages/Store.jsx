import React, { useState } from 'react';
import { products } from '../data/products';
import ProductCard from '../components/ProductCard';
import '../styles/App.css';

const Store = ({ user, addPurchase }) => {
  const [selectedProduct, setSelectedProduct] = useState(null);
  const [paymentMethod, setPaymentMethod] = useState('card');

  const handlePurchase = (productId) => {
    if (!user) {
      alert('Для покупки необходимо войти в систему');
      return;
    }
    setSelectedProduct(products.find(p => p.id === productId));
  };

  const processPayment = async () => {
    alert('Перенаправление на систему оплаты ${paymentMethod}...');
    
    await new Promise(resolve => setTimeout(resolve, 1000));
    
    addPurchase(selectedProduct.id);
    setSelectedProduct(null);
    alert('Покупка успешно завершена! Теперь продукт доступен в разделе "Мои покупки"');
  };

  return (
    <div className="store-page">
      <div className="container">
        <h1>Магазин продуктов</h1>
        
        <div className="store-grid">
          {products.map(product => (
            <ProductCard 
              key={product.id}
              product={product}
              onPurchase={handlePurchase}
            />
          ))}
        </div>

        {/* Модальное окно оплаты */}
        {selectedProduct && (
          <div className="modal-overlay">
            <div className="modal">
              <h2>Оформление покупки</h2>
              <div className="purchase-details">
                <h3>{selectedProduct.name}</h3>
                <p className="price">${selectedProduct.price}</p>
              </div>
              
              <div className="payment-methods">
                <h4>Выберите способ оплаты:</h4>
                <div className="payment-options">
                  <label>
                    <input
                      type="radio"
                      value="card"
                      checked={paymentMethod === 'card'}
                      onChange={(e) => setPaymentMethod(e.target.value)}
                    />
                    Банковская карта
                  </label>
                  <label>
                    <input
                      type="radio"
                      value="paypal"
                      checked={paymentMethod === 'paypal'}
                      onChange={(e) => setPaymentMethod(e.target.value)}
                    />
                    PayPal
                  </label>
                  <label>
                    <input
                      type="radio"
                      value="crypto"
                      checked={paymentMethod === 'crypto'}
                      onChange={(e) => setPaymentMethod(e.target.value)}
                    />
                    Криптовалюта
                  </label>
                </div>
              </div>

              <div className="modal-actions">
                <button 
                  onClick={processPayment}
                  className="btn btn-primary"
                >
                  Перейти к оплате
                </button>
                <button 
                  onClick={() => setSelectedProduct(null)}
                  className="btn btn-secondary"
                >
                  Отмена
                </button>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default Store;