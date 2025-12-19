import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Header from './components/Header';
import Footer from './components/Footer';
import Home from './pages/Home';
import Products from './pages/Products';
import TrialDownload from './pages/TrialDownload';
import Store from './pages/Store';
import PrivateDownloads from './pages/PrivateDownloads';
import Auth from './pages/Auth';
import ProductDetails from './pages/ProductDetails';
import './styles/App.css';

function App() {
  const [user, setUser] = useState(null);
  const [purchasedProducts, setPurchasedProducts] = useState([]);

  useEffect(() => {
    const savedUser = localStorage.getItem('user');
    const savedPurchases = localStorage.getItem('purchasedProducts');
    
    if (savedUser) {
      setUser(JSON.parse(savedUser));
    }
    if (savedPurchases) {
      setPurchasedProducts(JSON.parse(savedPurchases));
    }
  }, []);

  const login = (userData) => {
    setUser(userData);
    localStorage.setItem('user', JSON.stringify(userData));
  };

  const logout = () => {
    setUser(null);
    setPurchasedProducts([]);
    localStorage.removeItem('user');
    localStorage.removeItem('purchasedProducts');
  };

  const addPurchase = (productId) => {
    const newPurchases = [...purchasedProducts, productId];
    setPurchasedProducts(newPurchases);
    localStorage.setItem('purchasedProducts', JSON.stringify(newPurchases));
  };

  return (
    <Router>
      <div className="App">
        <Header user={user} logout={logout} />
        <main className="main-content">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/products" element={<Products />} />
            <Route path="/products/:id" element={<ProductDetails />} />
            <Route path="/trial-download" element={<TrialDownload />} />
            <Route 
              path="/store" 
              element={<Store user={user} addPurchase={addPurchase} />} 
            />
            <Route 
              path="/private-downloads" 
              element={
                user ? (
                  <PrivateDownloads purchasedProducts={purchasedProducts} />
                ) : (
                  <Navigate to="/auth" replace />
                )
              } 
            />
            <Route 
              path="/auth" 
              element={<Auth user={user} login={login} />} 
            />
          </Routes>
        </main>
        <Footer />
      </div>
    </Router>
  );
}

export default App;