import React, { useState } from 'react';
import { products } from '../data/products';
import '../styles/App.css';

const TrialDownload = () => {
  const [downloading, setDownloading] = useState(null);

  const trialProducts = products.filter(product => product.hasTrial);

  const handleDownload = async (productId) => {
    setDownloading(productId);
    
    await new Promise(resolve => setTimeout(resolve, 2000));
    
    alert('Началась загрузка пробной версии ${products.find(p => p.id === productId).name}');
    setDownloading(null);
  };

  return (
    <div className="trial-download-page">
      <div className="container">
        <h1>Пробные версии продуктов</h1>
        <p>Скачайте пробные версии наших продуктов для тестирования</p>
        
        <div className="trial-products">
          {trialProducts.map(product => (
            <div key={product.id} className="trial-product-card">
              <div className="trial-product-info">
                <h3>{product.name}</h3>
                <p>{product.trialDescription}</p>
                <div className="trial-details">
                  <strong>Срок действия:</strong> {product.trialPeriod}
                  <br />
                  <strong>Ограничения:</strong> {product.trialLimitations}
                </div>
                <button
                  onClick={() => handleDownload(product.id)}
                  disabled={downloading === product.id}
                  className="btn btn-primary btn-large"
                >
                  {downloading === product.id ? 'Загрузка...' : 'Скачать пробную версию'}
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default TrialDownload;