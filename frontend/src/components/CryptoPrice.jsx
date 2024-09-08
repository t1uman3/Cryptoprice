import React, { useEffect, useState } from 'react';
import axios from 'axios';

const CryptoPrice = () => {
   const [prices, setPrices] = useState({ bitcoin: { usd: null, rub: null }, ethereum: { usd: null, rub: null }, ton: { usd: null, rub: null }, });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchPrices = async () => {
      try {
        const response = await axios.get('http://127.0.0.1:8000/crypto');
        setPrices(response.data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };
    fetchPrices();
  }, []);

  if (loading) return <div className="body flex justify-end bg-gray-100 p-6">
      <div className="w-1/4">
        <div className="BitcoinPrice bg-white p-6 rounded-lg shadow-lg mb-4">
          <h1 className="text-2xl font-bold mb-4">Loading...</h1>
          <p className="text-lg">...</p>
          <p className="text-lg">...</p>
        </div>
      </div>
    </div>;
  if (error) return <div className="body flex justify-end bg-gray-100 p-6">
      <div className="w-1/4">
        <div className="BitcoinPrice bg-white p-6 rounded-lg shadow-lg mb-4">
          <h1 className="text-2xl font-bold mb-4">Error</h1>
          <p className="text-lg">...</p>
          <p className="text-lg">...</p>
        </div>
      </div>
    </div>;

  return (
    <div className="body flex justify-end bg-gray-100 p-6">
      <div className="w-1/4">
        <div className="BitcoinPrice bg-white p-6 rounded-lg shadow-lg mb-4">
          <h1 className="text-2xl font-bold mb-4">Bitcoin Prices</h1>
          <p className="text-lg">USD: ${prices.bitcoin.usd.toLocaleString(undefined, {
            minimumFractionDigits: 2,
            maximumFractionDigits: 2
          })}</p>
          <p className="text-lg">RUB: ₽{prices.bitcoin.rub.toLocaleString(undefined, {
            minimumFractionDigits: 2,
            maximumFractionDigits: 2
          })}</p>
        </div>
        <div className="BitcoinPrice bg-white p-6 rounded-lg shadow-lg mb-4">
          <h1 className="text-2xl font-bold mb-4">Ethereum Prices</h1>
          <p className="text-lg">USD: ${prices.ethereum.usd.toLocaleString(undefined, {
            minimumFractionDigits: 2,
            maximumFractionDigits: 2
          })}</p>
          <p className="text-lg">RUB: ₽{prices.ethereum.rub.toLocaleString(undefined, {
            minimumFractionDigits: 2,
            maximumFractionDigits: 2
          })}</p>
        </div>
        <div className="BitcoinPrice bg-white p-6 rounded-lg shadow-lg mb-4">
          <h1 className="text-2xl font-bold mb-4">Ethereum Prices</h1>
          <p className="text-lg">USD: ${prices.ton.usd.toLocaleString(undefined, {
            minimumFractionDigits: 2,
            maximumFractionDigits: 2
          })}</p>
          <p className="text-lg">RUB: ₽{prices.ton.rub.toLocaleString(undefined, {
            minimumFractionDigits: 2,
            maximumFractionDigits: 2
          })}</p>
        </div>
      </div>
    </div>
  );
};

export default CryptoPrice;
