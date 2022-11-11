import React, { useState } from 'react';
import './Header.css';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import { clearBrowserLocalStorage } from '../../utils/util';

interface appProps {
  zipcode: string;
  query: string;
  location: string;
  setQuery: any;
  setItemsToDisplay: any;
  setDisplayLocationPopup: any;
  setIsLoading: any;
  setProgress: any;
}

function Header(props: appProps) {
  return (
    <div className="header">
      <a href="#/" className="logo">
        <i className="fa-solid fa-cart-shopping fa-2xl"></i>
        <div className="logoTitle">roll</div>
        <div className="logoTitle">cart</div>
      </a>
      <SearchBar
        setQuery={props.setQuery}
        setItemsToDisplay={props.setItemsToDisplay}
        zipcode={props.zipcode}
        query={props.query}
        setIsLoading={props.setIsLoading}
        setProgress={props.setProgress}></SearchBar>
      <Address setDisplayLocationPopup={props.setDisplayLocationPopup} location={props.location}></Address>
      <AddList></AddList>
      <Login></Login>
      <StorePrices></StorePrices>
    </div>
  );
}

function SearchBar({ setQuery, setItemsToDisplay, zipcode, query, setIsLoading, setProgress }: any) {
  const handleSearchProductsClicked = async () => {
    try {
      setProgress(30);
      setIsLoading(true);
      const { data } = await axios.get(`http://127.0.0.1:5000/walmartTest?q=${query}&zipcode=${zipcode}`);
      setItemsToDisplay({ result: data });
    } catch (error: any) {
      console.log(error);
    } finally {
      setIsLoading(false);
      setProgress(100);
    }
  };

  const handleChange = (e: any) => {
    setQuery(e.target.value);
  };

  const handleKeyDown = (e: any) => {
    if (e.key === 'Enter') {
      handleSearchProductsClicked();
    }
  };

  return (
    <div className="searchBar">
      <div className="searchBarForm">
        <input className="searchBarInput" placeholder="Search products" onChange={handleChange} onKeyDown={handleKeyDown}></input>
        <button className="searchButton" onClick={handleSearchProductsClicked}>
          <i className="fa-solid fa-magnifying-glass"></i>
        </button>
      </div>
    </div>
  );
}

function Address({ setDisplayLocationPopup, location }: any) {
  return (
    <div className="addressBar">
      <button className="addressBarButton" onClick={() => setDisplayLocationPopup(true)}>
        <i className="fa-solid fa-location-dot"> </i>
        <span className="address"> {location}</span>
      </button>
    </div>
  );
}

function AddList() {
  return (
    <div className="addList">
      <button className="addListButton actionButton">
        <i className="fa-regular fa-rectangle-list"></i>
        <span> Lists</span>
      </button>
    </div>
  );
}

function Login() {
  const [showLoggedInUserOptions, setShowLoggedInUserOptions] = useState(false);
  const navigate = useNavigate();

  const handleOnchange = (e: any) => {
    console.log(e);
  };

  const userName = localStorage.getItem('userId')?.split('@')[0];

  const handleLoggedInUserClicked = () => {
    setShowLoggedInUserOptions(!showLoggedInUserOptions);
  };

  return (
    <div className="login">
      {userName ? (
        <div>
          <button className="loginButton actionButton userButton" onClick={handleLoggedInUserClicked}>
            <i className="fa-solid fa-user fa-1x"></i>{' '}
            <span>
              {'Hi, ' + userName} <i className="fa-solid fa-caret-down"></i>
            </span>
          </button>
          {showLoggedInUserOptions && (
            <div className="userOptions">
              <p className="userOptionRow">View lists</p>
              <hr />
              <p
                className="userOptionRow"
                onClick={() => {
                  clearBrowserLocalStorage();
                  navigate('/');
                  document.location.reload();
                }}>
                Logout
              </p>
            </div>
          )}
        </div>
      ) : (
        <div className="login">
          <button className="loginButton actionButton" onClick={() => navigate('/login')}>
            <i className="fa-solid fa-user"></i>
            <span> Login</span>
          </button>
        </div>
      )}
    </div>
  );
}

function StorePrices() {
  const navigate = useNavigate();

  return (
    <div className="storePrices">
      <span className="storePricesButton" onClick={() => navigate('/storePrices')}>
        <span id="storePrices" className="fa-stack fa-2x has-badge" data-count="0">
          <i className="fa fa-circle fa-stack-2x"></i>
          <i className="fa fa-shopping-cart fa-stack-1x"></i>
        </span>
      </span>
    </div>
  );
}

// Simple header for other pages. It only has the logo in the center.
export const LogoHeader = () => {
  const navigate = useNavigate();
  return (
    <div className="header">
      <button className="logo1 allUnsetButton" onClick={() => navigate('/')}>
        <i className="fa-solid fa-cart-shopping fa-2xl"></i>
        <div className="logoTitle">roll</div>
        <div className="logoTitle">cart</div>
      </button>
    </div>
  );
};

export default Header;
