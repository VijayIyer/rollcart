import axios from 'axios';
import { useEffect, useState } from 'react';
import { useParams, useSearchParams } from 'react-router-dom';
import { setAuthToken } from '../../auth/auth';
import { LogoHeader } from '../header/Header';
import './storePrice.css';

interface storeItem {
  quantity: string;
  itemPrice: string;
  itemName: string;
  itemThumbnail: string;
}

const CartDetails = () => {
  const [cartList, setCartList] = useState([]);
  let { listId } = useParams();
  console.log('Search params are', listId);

  useEffect(() => {
    setAuthToken(localStorage.getItem('token'));
    async function fetchData() {
      const { data } = await axios.get(`/getListItems/${listId}`);
      setCartList(data);
    }
    fetchData();
  }, []);

  return (
    <div>
      <LogoHeader />
      <h1 className="cartCount">Cart({cartList.length} items)</h1>
      <div className="itemPriceStoreContainer">
        {cartList.map((item: storeItem) => (
          <div className="itemPriceBox flex" key={item.itemName.slice(100)}>
            <img src={item.itemThumbnail} alt="" width={100} height={100} />
            <div className="itemNameStore tableItem flex w-60">{item.itemName}</div>
            {/* <div className="itemQuantityStore tableItem flex ml-auto">{item.quantity}</div> */}
            {/* <div className="itemPriceStore tableItem flex ml-auto">{item.itemPrice}$</div> */}
          </div>
        ))}
      </div>
    </div>
  );
};

export default CartDetails;
