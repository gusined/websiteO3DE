import React from 'react';
import { Link } from 'react-router-dom';
import '../styles/componets.css';

const ProductCard = ({ product, onPurchase, showPurchase = true }) => {
    return (
        <div className="product-card">
            <div className="product-image">
                <img src={product.image} alt={product.name} />
                </div>
                <div className="product-info">
                    <h3>{product.name}</h3>
                    <p className="product-description">{product.description}</p>
                    <div className="product-price">${product.price}</div>
                    <div className="product-actions">
                        <Link to={'products/${product.id}'} className="btn btn-secondary">
                        Подробнее
                        </Link>
                        {showPurchase && onPurchase && (
                            <button
                            onClick={() => onPurchase(product.id)}
                            className="btn btn-primary"
                            >
                                Купить
                                </button>
                        )}
                        </div>
                    </div>
            </div>
    );
};

export default ProductCard;