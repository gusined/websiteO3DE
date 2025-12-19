import React from 'react';
import '../styles/components.css';

const Footer = () => {
    return(
        <footer className="footer">
            <div className="container">
                <div className="footer-content">
                    <div className="footer-section">
                        <h4>SoftwareStore</h4>
                        <p>Лучшие продукты для ваших нужд</p>
                        </div>
                        <div className="fooetr-section">
                            <h4> Email: support@softwarestore.com</h4>
                            <p>Телефон: +7(999) 123-45-67</p>
                            </div>
                            <div className="footer-section">
                                <h4>Продукты</h4>
                                <ul>
                                    <li>Антивирус</li>
                                    <li>3D Движок</li>
                                    <li>Операционая система</li>
                                    </ul>
                                </div>
                    </div>
                    <div className="footer-bottom"></div>
                    <p>&copy; 2024 SoftwareStore. Все права защещены.</p>
                </div>
            </footer>
    );
};

export default Footer;