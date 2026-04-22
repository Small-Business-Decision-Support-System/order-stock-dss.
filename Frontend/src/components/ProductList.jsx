import React from 'react';

const ProductList = () => {
  
  const products = [
    { name: "Pasta 500g", stock: 149, rop: 86, ss: 11.0, abc: "A", status: "Warning" },
    { name: "Black Tea 500g", stock: 118, rop: 13, ss: 3.3, abc: "A", status: "Safe" },
    { name: "Sunflower Oil 1L", stock: 171, rop: 16, ss: 2.8, abc: "A", status: "Safe" },
    { name: "Milk 1L", stock: 175, rop: 13, ss: 2.3, abc: "A", status: "Safe" },
    { name: "White Sugar 1kg", stock: 101, rop: 65, ss: 9.2, abc: "B", status: "Critical" },
    { name: "Butter 250g", stock: 76, rop: 43, ss: 6.8, abc: "C", status: "Critical" },
    { name: "Olive Oil 1L", stock: 139, rop: 57, ss: 7.4, abc: "B", status: "Safe" },
  ];

  return (
    <div style={{ padding: '20px' }}>
      <h2 style={{ color: '#2c3e50' }}>Inventory Product List (Stochastic Model)</h2>
      <p>Demand Variability: <strong>20%</strong> | Service Level: <strong>95%</strong></p>
      
      <table style={{ width: '100%', borderCollapse: 'collapse', marginTop: '20px', backgroundColor: 'white' }}>
        <thead>
          <tr style={{ backgroundColor: '#2c3e50', color: 'white', textAlign: 'left' }}>
            <th style={tableHeader}>Product Name</th>
            <th style={tableHeader}>Category (ABC)</th>
            <th style={tableHeader}>Current Stock</th>
            <th style={tableHeader}>ROP</th>
            <th style={tableHeader}>Safety Stock</th>
            <th style={tableHeader}>Status</th>
          </tr>
        </thead>
        <tbody>
          {products.map((prod, index) => (
            <tr key={index} style={{ borderBottom: '1px solid #ddd' }}>
              <td style={tableCell}>{prod.name}</td>
              <td style={tableCell}><strong>{prod.abc}</strong></td>
              <td style={tableCell}>{prod.stock}</td>
              <td style={tableCell}>{prod.rop}</td>
              <td style={tableCell}>{prod.ss}</td>
              <td style={tableCell}>
                <span style={statusBadge(prod.status)}>{prod.status}</span>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

const tableHeader = { padding: '12px', border: '1px solid #ddd' };
const tableCell = { padding: '12px', border: '1px solid #ddd' };

const statusBadge = (status) => ({
  padding: '5px 10px',
  borderRadius: '15px',
  fontSize: '12px',
  fontWeight: 'bold',
  color: 'white',
  backgroundColor: status === 'Critical' ? '#e74c3c' : status === 'Warning' ? '#f39c12' : '#27ae60'
});

export default ProductList;