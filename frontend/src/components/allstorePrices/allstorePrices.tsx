import axios from 'axios';
import React, { useEffect, useState } from 'react';
import { useLocation, useNavigate, useParams } from 'react-router-dom';
import { setAuthToken } from '../../auth/auth';
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
  const { listId } = useParams();
  const location = useLocation();
  const { listName } = location.state;
  const [prices, setPrices] = useState([]);

  useEffect(() => {
    setAuthToken(localStorage.getItem('token'));
    async function fetchData() {
      const { data } = await axios.get(`/${listId}/getPrices?zipcode={47408}`);
      setPrices(data);
    }
    fetchData();
  }, []);

  return (
    <div>
      <LogoHeader />
      <div className="allstorePricesContainer">
        <div className="listName">
          <span>{listName}</span>
        </div>
        <div className="listCreatedDate">
          <span>Nov, 3, 2022</span>
        </div>
        <div className="allstorePricesDiv" onClick={() => navigate('/store/walmart')}>
          {prices.map((ele: StorePriceItem) => (
            <div className="allstorePricesBox" key={ele.store}>
              <img className="allstoreImage" src={`./${ele.store}.png`} alt="" width={50} height={50} />
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
