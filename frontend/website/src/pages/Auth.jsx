import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import '../styles/App.css';

const Auth = ({ user, login }) => {
  const [isLogin, setIsLogin] = useState(true);
  const [formData, setFormData] = useState({
    email: '',
    username: '',
    password: '',
    confirmPassword: '',
    verificationCode: ''
  });
  const [codeSent, setCodeSent] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    if (user) {
      navigate('/');
    }
  }, [user, navigate]);

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const sendVerificationCode = () => {
    alert('Код верификации отправлен на ${formData.email}');
    setCodeSent(true);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!isLogin) {
      if (formData.password !== formData.confirmPassword) {
        alert('Пароли не совпадают');
        return;
      }
      
      if (!codeSent) {
        sendVerificationCode();
        return;
      }

      if (formData.verificationCode !== '123456') {
        alert('Неверный код верификации');
        return;
      }
    } else {
      if (!codeSent) {
        sendVerificationCode();
        return;
      }

      if (formData.verificationCode !== '123456') {
        alert('Неверный код верификации');
        return;
      }
    }

    const userData = {
      email: formData.email,
      username: formData.username || formData.email.split('@')[0],
      id: Date.now()
    };
    
    login(userData);
    navigate('/');
  };

  return (
    <div className="auth-page">
      <div className="container">
        <div className="auth-form-container">
          <h1>{isLogin ? 'Вход в систему' : 'Регистрация'}</h1>
          
          <form onSubmit={handleSubmit} className="auth-form">
            <div className="form-group">
              <label>Email:</label>
              <input
                type="email"
                name="email"
                value={formData.email}
                onChange={handleChange}
                required
              />
            </div>

            {!isLogin && (
              <div className="form-group">
                <label>Никнейм:</label>
                <input
                  type="text"
                  name="username"
                  value={formData.username}
                  onChange={handleChange}
                  required
                />
              </div>
            )}

            <div className="form-group">
              <label>Пароль:</label>
              <input
                type="password"
                name="password"
                value={formData.password}
                onChange={handleChange}
                required
              />
            </div>

            {!isLogin && (
              <div className="form-group">
                <label>Повторите пароль:</label>
                <input
                  type="password"
                  name="confirmPassword"
                  value={formData.confirmPassword}
                  onChange={handleChange}
                  required
                />
              </div>
            )}

            {codeSent && (
              <div className="form-group">
                <label>Код верификации:</label>
                <input
                  type="text"
                  name="verificationCode"
                  value={formData.verificationCode}
                  onChange={handleChange}
                  placeholder="Введите код из письма"
                  required
                />
                <small>На вашу почту отправлен код подтверждения</small>
              </div>
            )}

            <button type="submit" className="btn btn-primary btn-full">
              {codeSent 
                ? (isLogin ? 'Войти' : 'Зарегистрироваться')
                : 'Получить код верификации'
              }
            </button>
          </form>

          <div className="auth-switch">
            <p>
              {isLogin ? 'Нет аккаунта?' : 'Уже есть аккаунт?'}
              <button 
                onClick={() => {
                  setIsLogin(!isLogin);
                  setCodeSent(false);
                  setFormData({
                    email: '',
                    username: '',
                    password: '',
                    confirmPassword: '',
                    verificationCode: ''
                  });
                }}
                className="link-btn"
              >
                {isLogin ? ' Зарегистрироваться' : ' Войти'}
              </button>
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Auth;