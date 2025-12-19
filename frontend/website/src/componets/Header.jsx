import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import '../styles/components.css';

const Header = ({ user, logout }) => {
  const location = useLocation();

  return (
    <header className="header">
      <div className="container">
        <div className="logo">
          <Link to="/">SoftwareStore</Link>
        </div>
        <nav className="nav">
          <Link to="/" className={location.pathname === '/' ? 'active' : ''}>
            Главная
          </Link>
          <Link to="/products" className={location.pathname === '/products' ? 'active' : ''}>
            Продукты
          </Link>
          <Link to="/trial-download" className={location.pathname === '/trial-download' ? 'active' : ''}>
            Пробные версии
          </Link>
          <Link to="/store" className={location.pathname === '/store' ? 'active' : ''}>
            Магазин
          </Link>
          {user && (
            <Link to="/private-downloads" className={location.pathname === '/private-downloads' ? 'active' : ''}>
              Мои покупки
            </Link>
          )}
          <Link to="/auth" className={location.pathname === '/auth' ? 'active' : ''}>
            {user ? 'Выйти (${user.username})' : 'Вход/Регистрация'}
          </Link>
          {user && (
            <button onClick={logout} className="logout-btn">
              Выйти
            </button>
          )}
        </nav>
      </div>
    </header>
  );
};

export default Header;