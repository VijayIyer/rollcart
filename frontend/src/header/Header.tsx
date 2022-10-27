import React, { useState } from 'react';
import './Header.css';
import axios from 'axios';

interface appProps {
  zipcode: string;
  query: string;
  updateQuery: (s: string) => void;
  updateZipcode: (s: string) => void;
}

function Header(props: appProps) {
  return (
    <div className="header">
      <a href="#/" className="logo">
        <i className="fa-solid fa-cart-shopping fa-2xl"></i>
        <div className="logoTitle">roll</div>
        <div className="logoTitle">cart</div>
      </a>
      <SearchBar updateQuery={props.updateQuery}></SearchBar>
      <Address></Address>
      <AddList></AddList>
      <Login></Login>
    </div>
  );
}

function SearchBar({ updateQuery }: any) {
  const [isLoading, setIsLoading] = useState(false);
  const [err, setErr] = useState('');

  // const handleSearchItemClicked = async (e: any) => {
  //   setIsLoading(true);
  //   try {
  //     const { data } = await axios.get(
  //       'http://127.0.0.1:5000/walmartTest?q=chicken&zipcode=47408',
  //     );
  //     setData(data);
  //     console.log(data);
  //   } catch (error: any) {
  //     console.log(error);
  //     setErr(error);
  //   } finally {
  //     setIsLoading(false);
  //   }
  // };
  const handleChange = (e: any) => {
    updateQuery(e.target.value);
  };
  const handleSearchItemClicked = (e: any) => {
    // set;
  };
  return (
    <div className="searchBar">
      <div className="searchBarForm">
        <input
          className="searchBarInput"
          placeholder="Search products"
          onChange={handleChange}></input>
        <button className="searchButton" onClick={handleSearchItemClicked}>
          <i className="fa-solid fa-magnifying-glass"></i>
        </button>
      </div>
    </div>
  );
}

function Address() {
  return (
    <div className="addressBar">
      <button className="addressBarButton">
        <i className="fa-solid fa-location-dot"> </i>
        <span className="address"> 120 Kingson Drive South</span>
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
