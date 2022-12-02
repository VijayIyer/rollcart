import axios from 'axios';
import React, { useEffect, useState } from 'react';
import { useLocation, useNavigate, useParams } from 'react-router-dom';
import { setAuthToken } from '../../auth/auth';
import { LogoHeader } from '../header/Header';
import './allstorePrices.css';

interface StorePriceItem {
  store_name: string;
  total_price: string;
  distanceInMiles: string;
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
  const [cheapestStore, setCheapestStore] = useState(-1);
  const [nearestStore, setNearestStore] = useState(-1);

  useEffect(() => {
    setAuthToken(localStorage.getItem('token'));
    axios.get('/testtt').then(response => {
      const { data } = response;
      setPrices(data);
      setCheapestStore(Math.min(...data.map((item: any) => parseInt(item.total_price, 10))));
      setNearestStore(Math.min(...data.map((item: any) => parseInt(item.distanceInMiles, 10))));
    });
  }, []);

  return (
    <div>
      <LogoHeader />
      <p className="allstorePriceTitle">Price Comparison</p>
      <div className="allstorePricesContainer">
        <div className="listName">
          <span>{listName}</span>
        </div>
        <div className="listCreatedDate">
          <span>Nov, 3, 2022</span>
        </div>
        <div className="allstorePricesDiv" onClick={() => navigate('/store/walmart')}>
          {prices.map((ele: StorePriceItem) => (
            <div className="allstorePricesBox" key={ele.store_name}>
              <img className="allstoreImage" src={`/${ele.store_name.toLowerCase()}.png`} alt="" width={70} height={70} />
              <div className="allstoreDetails">
                <p className="allstoreName">{capitalize(ele.store_name)}</p>
                <p className="allstorePrice">
                  <i className="fa-solid fa-dollar-sign"></i> {parseFloat(ele.total_price).toFixed(2)}
                </p>
                <p className="allstoreDistance">
                  <i className="fa-solid fa-location-dot"></i> {parseFloat(ele.distanceInMiles).toFixed(2)} miles
                </p>
              </div>
              {cheapestStore === parseInt(ele.total_price, 10) && <div className="stack-top">Cheapest</div>}
              {nearestStore === parseInt(ele.distanceInMiles, 10) && <div className="stack-top">Nearest</div>}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default AllStorePrices;
