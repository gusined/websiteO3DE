import React from 'react';
import { products } from '../data/products';
import '../styles/App.css';

const PrivateDownloads = ({ purchasedProducts }) => {
  const userProducts = products.filter(product => 
    purchasedProducts.includes(product.id)
  );

  const handleDownload = (productId) => {
    const product = products.find(p => p.id === productId);
    alert('Началась загрузка ${product.name}');
  };

  return (
    <div className="private-downloads-page">
      <div className="container">
        <h1>Мои покупки</h1>
        
        {userProducts.length === 0 ? (
          <div className="no-purchases">
            <h2>У вас пока нет покупок</h2>
            <p>Посетите наш магазин, чтобы приобрести продукты</p>
          </div>
        ) : (
          <div className="purchased-products">
            <h2>Доступные для скачивания продукты:</h2>
            <div className="downloads-grid">
              {userProducts.map(product => (
                <div key={product.id} className="download-item">
                  <h3>{product.name}</h3>
                  <p>Версия: {product.latestVersion}</p>
                  <p>Дата покупки: {new Date().toLocaleDateString()}</p>
                  <button 
                    onClick={() => handleDownload(product.id)}
                    className="btn btn-primary"
                  >
                    Скачать
                  </button>
                  <button className="btn btn-secondary">
                    Получить ключ активации
                  </button>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default PrivateDownloads;