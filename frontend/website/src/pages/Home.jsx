import React from 'react';
import { Link } from 'react-router-dom';
import '../styles/App.css';

const Home = () => {
  return (
    <div className="home-page">
      {/* Анимированный GIF/видео фон */}
      <section className="hero-section">
        <div className="hero-background">
          {/* Замените путь на ваш GIF */}
          <img 
            src="/animations/background-animation.gif" 
            alt="Анимированный фон"
            className="background-animation"
          />
        </div>
        <div className="hero-content">
          <h1>Добро пожаловать в SoftwareStore</h1>
          <p>Инновационные программные решения для бизнеса и личного использования</p>
          <div className="hero-buttons">
            <Link to="/products" className="btn btn-primary btn-large">
              Изучить продукты
            </Link>
            <Link to="/trial-download" className="btn btn-secondary btn-large">
              Скачать пробные версии
            </Link>
          </div>
        </div>
      </section>

      {/* Краткая информация о продуктах */}
      <section className="products-preview">
        <div className="container">
          <h2>Наши продукты</h2>
          <div className="preview-grid">
            <div className="preview-item">
              <h3>Антивирус Pro</h3>
              <p>Полная защита вашего компьютера от вирусов и вредоносных программ</p>
            </div>
            <div className="preview-item">
              <h3>3D Engine Ultra</h3>
              <p>Мощный движок для создания потрясающих 3D приложений и игр</p>
            </div>
            <div className="preview-item">
              <h3>OS Nova</h3>
              <p>Современная операционная система с интуитивным интерфейсом</p>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
};

export default Home;