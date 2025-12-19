import React from 'react';
import { useParams, Link } from 'react-router-dom';
import { products } from '../data/products';
import '../styles/App.css';

const ProductDetails = () => {
  const { id } = useParams();
  const product = products.find(p => p.id === parseInt(id));

  if (!product) {
    return (
      <div className="container">
        <h1>Продукт не найден</h1>
        <Link to="/products" className="btn btn-primary">
          Вернуться к продуктам
        </Link>
      </div>
    );
  }

  return (
    <div className="product-details-page">
      <div className="container">
        <div className="product-detail-header">
          <h1>{product.name}</h1>
          <Link to="/products" className="btn btn-secondary">
            ← Назад к продуктам
          </Link>
        </div>

        <div className="product-detail-content">
          <div className="product-image-large">
            <img src={product.image} alt={product.name} />
          </div>
          
          <div className="product-info-detailed">
            <h2>Описание</h2>
            <p>{product.fullDescription}</p>
            
            <h3>Основные возможности:</h3>
            <ul>
              {product.features.map((feature, index) => (
                <li key={index}>{feature}</li>
              ))}
            </ul>

            <h3>Характеристики:</h3>
            <ul>
              {product.specifications.map((spec, index) => (
                <li key={index}>{spec}</li>
              ))}
            </ul>

            <div className="product-actions-detailed">
              <Link to="/store" className="btn btn-primary btn-large">
                Купить за ${product.price}
              </Link>
              {product.hasTrial && (
                <Link to="/trial-download" className="btn btn-secondary">
                  Скачать пробную версию
                </Link>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ProductDetails;