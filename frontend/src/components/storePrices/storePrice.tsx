import axios from 'axios';
import { useEffect, useState } from 'react';
import { LogoHeader } from '../header/Header';
import './storePrice.css';

interface storeItem {
  quantity: string;
  itemPrice: string;
  itemName: string;
  itemThumbnail: string;
}

const StorePrice = () => {
  const [cartList, setCartList] = useState([]);

  useEffect(() => {
    async function fetchData() {
      if (process.env.NODE_ENV !== 'production'){
        const { data } = await axios.get(process.env.REACT_APP_FLASK_API_URL_LOCAL + 'getStoreItems');
        setCartList(data);
      }
      else{
        const { data } = await axios.get(process.env.REACT_APP_FLASK_API_URL_PROD + 'getStoreItems');
        setCartList(data);
      }
    }
    fetchData();
  }, []);

  return (
    <div>
      <LogoHeader />
      <h1 className="cartCount">Cart(4 items)</h1>
      <div className="itemPriceStoreContainer">
        {cartList.map((item: storeItem) => (
          <div className="itemPriceBox flex" key={item.itemName.slice(100)}>
            <img src={item.itemThumbnail} alt="" width={100} height={100} />
            <div className="itemNameStore tableItem flex w-60">
              {item.itemName}
            </div>
            <div className="itemQuantityStore tableItem flex ml-auto">
              {item.quantity}
            </div>
            <div className="itemPriceStore tableItem flex ml-auto">
              {item.itemPrice}$
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default StorePrice;
