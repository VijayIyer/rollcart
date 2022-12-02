import axios from 'axios';
import { useEffect, useState } from 'react';
import { useLocation, useNavigate, useParams, useSearchParams } from 'react-router-dom';
import { setAuthToken } from '../../auth/auth';
import { LogoHeader } from '../header/Header';
import './storePrice.css';

interface storeItem {
  quantity: string;
  itemPrice: string;
  itemName: string;
  itemThumbnail: string;
}

export const CartDetails = () => {
  const [listItems, setListItems] = useState([]);
  const cart_list_id = localStorage.getItem('cart_list_id');

  useEffect(() => {
    setAuthToken(localStorage.getItem('token'));
    async function fetchData() {
      const { data } = await axios.get(`/getListItems/${cart_list_id}`);
      setListItems(data);
    }
    fetchData();
  }, []);

  return (
    <div>
      <LogoHeader />
      <ShowItemsInList listItems={listItems} listName="Cart" listId={cart_list_id} />
    </div>
  );
};

export const ListDetails = () => {
  const [listItems, setListItems] = useState([]);
  const { listId } = useParams();
  const location = useLocation();
  console.log(location);
  let { listName } = location.state;

  useEffect(() => {
    setAuthToken(localStorage.getItem('token'));
    async function fetchData() {
      const { data } = await axios.get(`/getListItems/${listId}`);
      setListItems(data);
    }
    fetchData();
  }, []);

  return (
    <div>
      <LogoHeader />
      <ShowItemsInList listItems={listItems} listName={listName} listId={listId} />
    </div>
  );
};

const ShowItemsInList = ({ listItems, listName, listId }: any) => {
  const navigate = useNavigate();

  return (
    <div>
      <div className="showItemsHeader">
        <h1 className="listCount">
          {listName}({listItems.length} {listItems.length > 1 ? 'items' : 'item'})
        </h1>
        <button className="comparePrices" onClick={() => navigate(`/storePrices/${listId}`, { state: { listName: listName } })}>
          <div>
            <p className="comparePricesTitle">Shop my {listName} list</p>
            <p className="comparePricesFooter"> (Compare prices)</p>
          </div>
        </button>
      </div>
      <div className="itemPriceStoreContainer">
        <div className="tableTitle flex">
          <h3>Name</h3>
          <h3>Quantity</h3>
        </div>
        {listItems.map((item: storeItem) => (
          <div className="itemPriceBox flex" key={item.itemName.slice(100)}>
            <img src={item.itemThumbnail} alt="" width={100} height={100} />
            <div className="itemNameStore tableItem flex w-60">{item.itemName}</div>
            <div className="itemQuantityStore tableItem flex ml-auto">{item.quantity}</div>
          </div>
        ))}
      </div>
    </div>
  );
};
