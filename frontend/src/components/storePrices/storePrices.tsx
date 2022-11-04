import axios from 'axios';
import React, { useEffect, useState } from 'react';
import { LogoHeader } from '../header/Header';
import './storePrices.css';

interface StorePriceItem {
  store: string;
  price: string;
}

function capitalize(word: string) {
  return word[0].toUpperCase() + word.substring(1).toLowerCase();
}

const StorePrices = () => {
  const [prices, setPrices] = useState([]);

  useEffect(() => {
    async function fetchData() {
      const { data } = await axios.get('http://127.0.0.1:5000/getPrices/3');
      setPrices(data);
    }
    fetchData();
  }, []);

  return (
    <div>
      <LogoHeader />
      <div className="storePricesContainer">
        <div className="listName">
          <span>List Name goes here</span>
        </div>
        <div className="listCreatedDate">
          <span>Nov, 3, 2022</span>
        </div>
        <div className="storePricesDiv">
          {prices.map((ele: StorePriceItem) => (
            <div className="storePricesBox">
              <img
                className="storeImage"
                src={`./${ele.store}.png`}
                alt=""
                width={50}
                height={50}
              />
              <div className="storeDetails">
                <p className="storeName">{capitalize(ele.store)}</p>
                <p className="storePrice">${ele.price}</p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default StorePrices;
