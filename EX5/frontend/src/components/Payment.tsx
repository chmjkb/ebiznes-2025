import React, { useState } from 'react';
import '@/styles/Payment.css'; // Make sure this path matches your file structure
import axios from 'axios';
import { useCartContext } from '@/context/CartContext';

export default function Payments() {
  const { cartValue, clearCart } = useCartContext();
  const [formData, setFormData] = useState({
    cardNumber: '',
    cardHolder: '',
    expirationDate: '',
    cvv: '',
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await axios.post('http://localhost:8080/payments', { ...formData, amount: cartValue });
      clearCart();
    } catch (e) {
      console.error(e);
    }
  };

  return (
    <div>
      <h1>You're due: {cartValue}zł</h1>
      <p>Please enter your payment details below:</p>
      <div className="payment-container">
        <form onSubmit={handleSubmit} className="payment-form">
          <div className="form-group">
            <label>Card Number</label>
            <input
              type="text"
              name="cardNumber"
              value={formData.cardNumber}
              onChange={handleChange}
              placeholder="1234 5678 9012 3456"
              required
            />
          </div>
          <div className="form-group">
            <label>Name on Card</label>
            <input
              type="text"
              name="cardHolder"
              value={formData.cardHolder}
              onChange={handleChange}
              placeholder="John Doe"
              required
            />
          </div>
          <div className="form-row">
            <div className="form-group half-width">
              <label>Expiry</label>
              <input
                type="text"
                name="expirationDate"
                value={formData.expirationDate}
                onChange={handleChange}
                placeholder="MM/YY"
                required
              />
            </div>
            <div className="form-group half-width">
              <label>CVV</label>
              <input
                type="text"
                name="cvv"
                value={formData.cvv}
                onChange={handleChange}
                placeholder="123"
                required
              />
            </div>
          </div>
          <button type="submit" className="submit-button">
            Submit Payment
          </button>
        </form>
      </div>
    </div>
  );
}
