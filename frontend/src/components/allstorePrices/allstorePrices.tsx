import axios from 'axios';
import React, { useEffect, useState } from 'react';
import { useLocation, useNavigate, useParams } from 'react-router-dom';
import { setAuthToken } from '../../auth/auth';
import { LogoHeader } from '../header/Header';
import './allstorePrices.css';
import CircularProgress from '@mui/material/CircularProgress';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';

interface itemDetails {
  item_name: string;
  item_thumbnail: string;
}

interface StorePriceItem {
  store_name: string;
  total_price: string;
  distanceInMiles: string;
  unavailableItems: itemDetails[];
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
  const [isLoading, setIsLoading] = useState(false);
  const zipcode = localStorage.getItem('zipcode') || '47408';
  const lat = localStorage.getItem('lat') || '39.165';
  const long = localStorage.getItem('long') || '-86.4932';
  const [retailerSelected, setRetailerSelected] = useState('');
  const [unavailableItems, setUnavailableItems] = useState([] as any);

  useEffect(() => {
    setIsLoading(true);
    setAuthToken(localStorage.getItem('token'));
    axios
      .get(`${listId}/getPrices?zipcode=${zipcode}&lat=${lat}&long=${long}`)
      // .get(`testtt`)
      .then(response => {
        const { data } = response;
        setPrices(data);
        setCheapestStore(Math.min(...data.map((item: any) => parseFloat(item.total_price))));
        setNearestStore(Math.min(...data.map((item: any) => parseFloat(item.distanceInMiles))));
      })
      .finally(() => {
        setIsLoading(false);
      });
  }, []);

  return (
    <div>
      <LogoHeader />
      <p className="allstorePriceTitle">Price Comparison</p>
      {isLoading === true ? (
        <div className="loading-bar">
          <CircularProgress />
          <p className="allstorePricesWaitMessage">Hang tight!. We are fetching best products for you.</p>
        </div>
      ) : (
        <div className="allstorePricesContainer">
          <div className="listName">
            <span>{listName}</span>
          </div>
          <div className="listCreatedDate">
            <span>Nov, 3, 2022</span>
          </div>
          <div className="allstorePricesDiv">
            {prices.map((ele: StorePriceItem) => (
              <div
                className="allstorePricesBox"
                key={ele.store_name}
                onClick={() => {
                  setRetailerSelected(ele.store_name);
                  setUnavailableItems(ele.unavailableItems);
                }}>
                <img className="allstoreImage" src={`/${ele.store_name.toLowerCase()}.png`} alt="" width={70} height={70} />
                <div className="allstoreDetails">
                  <p className="allstoreName">{capitalize(ele.store_name)}</p>
                  <p className="allstorePrice">
                    <i className="fa-solid fa-dollar-sign"></i> {parseFloat(ele.total_price).toFixed(2)}
                  </p>
                  <p className="allstoreDistance">
                    <i className="fa-solid fa-location-dot"></i> {parseFloat(ele.distanceInMiles).toFixed(2)} miles
                  </p>
                  {!ele.unavailableItems || ele.unavailableItems.length === 0 ? (
                    <p className="allAvailable">
                      <i className="fa-solid fa-circle-info"> </i> All items are available
                    </p>
                  ) : (
                    <p className="unavailableItems">
                      <i className="fa-solid fa-circle-info"> </i> {ele.unavailableItems.length}{' '}
                      {ele.unavailableItems.length === 1 ? ' item is unavailable' : ' items are unavailable'}
                    </p>
                  )}
                </div>
                {cheapestStore === parseFloat(ele.total_price) && parseFloat(ele.total_price) > 0 && <div className="stack-top">Cheapest</div>}
                {parseFloat(ele.total_price) > 0 &&
                  nearestStore === parseFloat(ele.distanceInMiles) &&
                  ele.distanceInMiles &&
                  parseFloat(ele.distanceInMiles) > 0 && <div className="stack-top">Nearest</div>}
                {ele.unavailableItems && ele?.unavailableItems.length === 0 && <div className="stack-top green">All available</div>}
              </div>
            ))}
          </div>
        </div>
      )}
      <IndividualStorePrices retailerSelected={retailerSelected} listId={listId} unavailableItems={unavailableItems} />
    </div>
  );
};

interface individualStoreItem {
  retailerSelected: string;
  listId: any;
  unavailableItems: any;
}

export const IndividualStorePrices = ({ retailerSelected, listId, unavailableItems }: individualStoreItem) => {
  const [items, setItems] = useState([]);
  const [isloading, setIsLoading] = useState(true);

  useEffect(() => {
    if (retailerSelected === '') {
      return;
    }
    setIsLoading(true);
    axios
      .get(`${listId}/${retailerSelected}/getPrices`)
      .then(response => {
        setItems(response.data);
        setIsLoading(false);
      })
      .finally(() => {
        setIsLoading(false);
      });
  }, [retailerSelected]);

  return (
    <div className="table">
      {isloading === false ? (
        <div>
          <div className="storeDetails">
            <div className="storeTableHeader">Items information in {retailerSelected}</div>
          </div>

          <TableContainer component={Paper} sx={{ width: 1200 }}>
            <Table aria-label="simple table" size="medium">
              <TableHead>
                <TableRow>
                  <TableCell>Image</TableCell>
                  <TableCell align="left">Product Name</TableCell>
                  <TableCell align="center">Status</TableCell>
                  <TableCell align="right">Total Price</TableCell>
                  <TableCell align="right">Take to website</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {items.map((item: any) => (
                  <TableRow key={item.itemName} sx={{ '&:last-child td, &:last-child th': { border: 0 } }}>
                    <TableCell component="th" scope="row">
                      <img src={item.item_image} alt="" width={100} height={100} />
                    </TableCell>
                    <TableCell sx={{ fontSize: '1rem' }} align="left">
                      {item.itemName}
                    </TableCell>
                    <TableCell sx={{ fontSize: '1rem' }} align="center">
                      <i className="fa-regular fa-circle-check bg-green"></i>
                    </TableCell>
                    <TableCell sx={{ fontSize: '1rem' }} align="right">
                      {item.totalPrice}
                    </TableCell>
                    <TableCell sx={{ fontSize: '1rem' }} align="center">
                      <a href={item.item_url}>Link</a>
                    </TableCell>
                  </TableRow>
                ))}
                {unavailableItems.map((item: any) => (
                  <TableRow key={item.item_name} sx={{ '&:last-child td, &:last-child th': { border: 0 } }}>
                    <TableCell component="th" scope="row">
                      <img src={item.item_thumbnail} alt="" width={100} height={100} />
                    </TableCell>
                    <TableCell sx={{ fontSize: '1rem' }} align="left">
                      {item.item_name}
                    </TableCell>
                    <TableCell sx={{ fontSize: '1rem' }} align="center">
                      <i className="fa-solid fa-ban bg-red"></i>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
        </div>
      ) : (
        <div>
          {retailerSelected !== '' ? (
            <div className="loading-bar">
              <CircularProgress />
              <p className="allstorePricesWaitMessage">Hang tight!. We are retrieving products from {retailerSelected}.</p>
            </div>
          ) : (
            <></>
          )}
        </div>
      )}
    </div>
  );
};

export default AllStorePrices;
