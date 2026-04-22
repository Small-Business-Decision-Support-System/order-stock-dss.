import React from 'react';

const Dashboard = () => {

  const stats = {
    totalProducts: 15,
    criticalStock: 3, 
    totalValue: "45,230 TL",
    systemStatus: "Active"
  };

  return (
    <div style={{ padding: '20px' }}>
      <h2 style={{ color: '#2c3e50', marginBottom: '20px' }}>System Overview</h2>
      
      
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '20px' }}>
        
        <div className="card" style={cardStyle('#3498db')}>
          <h3>Total Products</h3>
          <p style={numberStyle}>{stats.totalProducts}</p>
        </div>

        <div className="card" style={cardStyle('#e74c3c')}>
          <h3>Critical Alerts</h3>
          <p style={numberStyle}>{stats.criticalStock}</p>
          <small>Need immediate reorder</small>
        </div>

        <div className="card" style={cardStyle('#27ae60')}>
          <h3>Inventory Value</h3>
          <p style={numberStyle}>{stats.totalValue}</p>
        </div>

        <div className="card" style={cardStyle('#f39c12')}>
          <h3>System Status</h3>
          <p style={numberStyle}>{stats.systemStatus}</p>
        </div>

      </div>

      <div style={{ marginTop: '40px', padding: '20px', backgroundColor: '#fff', borderRadius: '10px', boxShadow: '0 4px 6px rgba(0,0,0,0.1)' }}>
        <h3>Quick Summary</h3>
        <p>The system is currently monitoring 15 grocery items using a <strong>Stochastic Model (20% Variability)</strong>. 
        Safety stocks are calculated to prevent stockouts during lead times.</p>
      </div>
    </div>
  );
};


const cardStyle = (color) => ({
  backgroundColor: color,
  color: 'white',
  padding: '20px',
  borderRadius: '12px',
  boxShadow: '0 4px 8px rgba(0,0,0,0.1)',
  textAlign: 'center'
});

const numberStyle = {
  fontSize: '32px',
  fontWeight: 'bold',
  margin: '10px 0'
};

export default Dashboard;