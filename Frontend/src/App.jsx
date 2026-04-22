import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import Dashboard from './components/Dashboard';
import ProductList from './components/ProductList';
import './App.css'; 

function App() {
  return (
    <Router>
      <div className="app-container" style={{ display: 'flex', minHeight: '100vh', backgroundColor: '#f4f7f6' }}>
        
        
        <nav style={{ width: '250px', backgroundColor: '#2c3e50', padding: '20px', color: 'white' }}>
          <h2>📦 DSS System</h2>
          <ul style={{ listStyleType: 'none', padding: 0, marginTop: '30px' }}>
            <li style={{ marginBottom: '15px' }}>
              <Link to="/" style={{ color: 'white', textDecoration: 'none', fontSize: '18px' }}>📊 Dashboard</Link>
            </li>
            <li>
              <Link to="/products" style={{ color: 'white', textDecoration: 'none', fontSize: '18px' }}>📋 Inventory List</Link>
            </li>
          </ul>
        </nav>

        
        <div className="main-content" style={{ flex: 1, padding: '30px' }}>
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/products" element={<ProductList />} />
          </Routes>
        </div>

      </div>
    </Router>
  );
}

export default App;