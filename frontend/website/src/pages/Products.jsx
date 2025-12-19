import React, { useState } from 'react';
import { products } from '../data/products';
import '../styles/App.css';

const Products = () => {
  const [activeTab, setActiveTab] = useState('overview');

  return (
    <div className="products-page">
      <div className="container">
        <h1>Наши продукты</h1>
        
        {/* Навигация по табам */}
        <div className="tabs">
          <button 
            className={activeTab === 'overview' ? 'tab active' : 'tab'}
            onClick={() => setActiveTab('overview')}
          >
            Обзор продуктов
          </button>
          <button 
            className={activeTab === 'details' ? 'tab active' : 'tab'}
            onClick={() => setActiveTab('details')}
          >
            Подробная информация
          </button>
          <button 
            className={activeTab === 'updates' ? 'tab active' : 'tab'}
            onClick={() => setActiveTab('updates')}
          >
            Обновления и патчи
          </button>
          <button 
            className={activeTab === 'instructions' ? 'tab active' : 'tab'}
            onClick={() => setActiveTab('instructions')}
          >
            Инструкции
          </button>
        </div>

        {/* Контент табов */}
        <div className="tab-content">
          {activeTab === 'overview' && (
            <div className="products-grid">
              {products.map(product => (
                <div key={product.id} className="product-overview">
                  <h3>{product.name}</h3>
                  <p>{product.fullDescription}</p>
                  <ul>
                    {product.features.map((feature, index) => (
                      <li key={index}>{feature}</li>
                    ))}
                  </ul>
                </div>
              ))}
            </div>
          )}

          {activeTab === 'details' && (
            <div className="detailed-info">
              {products.map(product => (
                <div key={product.id} className="product-detail">
                  <h3>{product.name}</h3>
                  <div className="specs">
                    <h4>Характеристики:</h4>
                    <ul>
                      {product.specifications.map((spec, index) => (
                        <li key={index}>{spec}</li>
                      ))}
                    </ul>
                  </div>
                </div>
              ))}
            </div>
          )}

          {activeTab === 'updates' && (
            <div className="updates-info">
              <h3>Последние обновления</h3>
              {products.map(product => (
                <div key={product.id} className="update-item">
                  <h4>{product.name}</h4>
                  <div className="update-version">Версия {product.latestVersion}</div>
                  <p>{product.updateNotes}</p>
                </div>
              ))}
            </div>
          )}

          {activeTab === 'instructions' && (
            <div className="instructions-info">
              <h3>Инструкции по использованию</h3>
              {products.map(product => (
                <div key={product.id} className="instruction-item">
                  <h4>{product.name}</h4>
                  <div className="instruction-steps">
                    {product.instructions.map((step, index) => (
                      <div key={index} className="step">
                        <strong>Шаг {index + 1}:</strong> {step}
                      </div>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Products;