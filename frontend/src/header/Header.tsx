import React, { useState } from 'react';
import './Header.css';
import axios from 'axios';

interface appProps {
  zipcode: string;
  query: string;
  location: string;
  setQuery: any;
  setItemsToDisplay: any;
  setDisplayLocationPopup: any;
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
        query={props.query}></SearchBar>
      <Address
        setDisplayLocationPopup={props.setDisplayLocationPopup}
        location={props.location}></Address>
      <AddList></AddList>
      <Login></Login>
    </div>
  );
}

function SearchBar({ setQuery, setItemsToDisplay, zipcode, query }: any) {
  const handleSearchProductsClicked = async () => {
    try {
      const { data } = await axios.get(
        `http://127.0.0.1:5000/walmartTest?q=${query}&zipcode=${47408}`,
      );
      setItemsToDisplay({ result: data });
    } catch (error: any) {
      console.log(error);
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
        <input
          className="searchBarInput"
          placeholder="Search products"
          onChange={handleChange}
          onKeyDown={handleKeyDown}></input>
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
      <button
        className="addressBarButton"
        onClick={() => setDisplayLocationPopup(true)}>
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
        <i className="fa-solid fa-cart-plus"></i>
        <span> Add List</span>
      </button>
    </div>
  );
}

function Login() {
  return (
    <div className="login">
      <button className="loginButton actionButton">
        <i className="fa-solid fa-user"></i>
        <span> Login</span>
      </button>
    </div>
  );
}

export default Header;
