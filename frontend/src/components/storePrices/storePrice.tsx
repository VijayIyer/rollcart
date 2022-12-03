import { CircularProgress } from '@mui/material';
import axios from 'axios';
import { useEffect, useState } from 'react';
import { useLocation, useNavigate, useParams, useSearchParams } from 'react-router-dom';
import { setAuthToken } from '../../auth/auth';
import { LogoHeader } from '../header/Header';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';
import './storePrice.css';

interface storeItem {
  quantity: string;
  itemPrice: string;
  itemName: string;
  itemThumbnail: string;
}

export const CartDetails = () => {
  const [listItems, setListItems] = useState([]);
  const location = useLocation();
  const state = location.state;
  const [isLoading, setIsLoading] = useState(true);
  const cart_list_id = localStorage.getItem('cart_list_id');

  useEffect(() => {
    setIsLoading(true);
    setAuthToken(localStorage.getItem('token'));
    axios
      .get(`/getListItems/${cart_list_id}`)
      .then(response => {
        setListItems(response.data);
      })
      .finally(() => {
        setIsLoading(false);
      });
  }, []);

  return (
    <div>
      <LogoHeader />
      <ShowItemsInList listItems={listItems} listName="Cart" listId={cart_list_id} isLoading={isLoading} />
    </div>
  );
};

export const ListDetails = () => {
  const [listItems, setListItems] = useState([]);
  const { listId } = useParams();
  const location = useLocation();
  const [isLoading, setIsLoading] = useState(false);
  let { listName } = location.state;

  useEffect(() => {
    setIsLoading(true);
    setAuthToken(localStorage.getItem('token'));
    axios
      .get(`/getListItems/${listId}`)
      .then(response => {
        setListItems(response.data);
      })
      .finally(() => {
        setIsLoading(false);
      });
    setIsLoading(false);
  }, []);

  return (
    <div>
      <LogoHeader />
      <ShowItemsInList listItems={listItems} listName={listName} listId={listId} isLoading={isLoading} />
    </div>
  );
};

const ShowItemsInList = ({ listItems, listName, listId, isLoading }: any) => {
  const navigate = useNavigate();

  console.log('isLoading is', isLoading);
  return (
    <div>
      {isLoading === false ? (
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
            <TableContainer component={Paper} sx={{ width: 1200 }}>
              <Table aria-label="simple table" size="medium">
                <TableHead>
                  <TableRow>
                    <TableCell>Image</TableCell>
                    <TableCell align="left">Product Name</TableCell>
                    <TableCell align="center">Quantity</TableCell>
                    {/* <TableCell align="right">Total Price</TableCell>
                    <TableCell align="right">Take to website</TableCell> */}
                  </TableRow>
                </TableHead>
                <TableBody>
                  {listItems.map((item: storeItem) => (
                    <TableRow key={item.itemName} sx={{ '&:last-child td, &:last-child th': { border: 0 } }}>
                      <TableCell component="th" scope="row">
                        <img src={item.itemThumbnail} alt="" width={100} height={100} />
                      </TableCell>
                      <TableCell sx={{ fontSize: '1rem' }} align="left">
                        {item.itemName}
                      </TableCell>

                      <TableCell sx={{ fontSize: '1rem' }} align="right">
                        {item.quantity}
                      </TableCell>
                      <TableCell sx={{ fontSize: '1rem' }} align="center">
                        <i className="fa-solid fa-trash"></i>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </TableContainer>
          </div>
        </div>
      ) : (
        <div className="loading-bar">
          <CircularProgress />
          <p className="allstorePricesWaitMessage">Please wait. While we get your cart ready!</p>
        </div>
      )}
    </div>
  );
};
