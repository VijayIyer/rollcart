import axios from 'axios';
import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { LogoHeader } from '../header/Header';
import './allstorePrices.css';

interface StorePriceItem {
  store: string;
  price: string;
}

function capitalize(word: string) {
  return word[0].toUpperCase() + word.substring(1).toLowerCase();
}

const AllStorePrices = () => {
  const navigate = useNavigate();
  const [prices, setPrices] = useState([]);

  useEffect(() => {
    async function fetchData() {
<<<<<<< HEAD
      const { data } = await axios.get('/getPrices/3');
      setPrices(data);
=======
      if (process.env.NODE_ENV !== 'production'){
        const { data } = await axios.get(process.env.REACT_APP_FLASK_API_URL_LOCAL + 'getPrices/3');
        setPrices(data);
      }
      else{
        const { data } = await axios.get(process.env.REACT_APP_FLASK_API_URL_PROD + 'getPrices/3');
        setPrices(data);
      }
>>>>>>> 95da4b15 (Updated config for frontend)
    }
    fetchData();
  }, []);

  return (
    <div>
      <LogoHeader />
      <div className="allstorePricesContainer">
        <div className="listName">
          <span>List Name goes here</span>
        </div>
        <div className="listCreatedDate">
          <span>Nov, 3, 2022</span>
        </div>
        <div
          className="allstorePricesDiv"
          onClick={() => navigate('/store/walmart')}>
          {prices.map((ele: StorePriceItem) => (
            <div className="allstorePricesBox" key={ele.store}>
              <img
                className="allstoreImage"
                src={`./${ele.store}.png`}
                alt=""
                width={50}
                height={50}
              />
              <div className="allstoreDetails">
                <p className="allstoreName">{capitalize(ele.store)}</p>
                <p className="allstorePrice">${ele.price}</p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default AllStorePrices;
