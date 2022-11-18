import React, { useState, useEffect, Dispatch, SetStateAction } from 'react';
import { Toaster } from 'react-hot-toast';
import { useLocation } from 'react-router-dom';
import { setAuthToken } from './auth/auth';
import { DisplayItems } from './components/dataDisplay/dataDisplay';
import Header from './components/header/Header';
import { LoadingBar } from './components/loadingBar/loadingBar';
import TopLoadingBar from './components/loadingBar/topLoadingBar';
import { GoogleAutoCompleteLocation } from './components/location/location';

function App() {
  const [zipcode, setZipcode] = useState('47408');
  const [query, setQuery] = useState('');
  const [searchTerm, setSearchTerm] = useState('');
  const [itemsToDisplay, setItemsToDisplay] = useState({ result: [] });
  const [displayLocationPopUp, setDisplayLocationPopup] = useState(false);
  const [location, setLocation] = useState('120 Kingston Drive South, 47408');
  const [isLoading, setIsLoading] = useState(false);
  const [progress, setProgress] = useState(0);
  const [userLists, setUserLists] = useState([]);
  const [token, setToken] = useState('');

  useEffect(() => {
    if (localStorage.getItem('token')) {
      setToken(localStorage.getItem('token') as string);
      setAuthToken(localStorage.getItem('token'));
    }
  }, []);

  useEffect(() => {
    setSearchTerm(query);
  }, [itemsToDisplay]);

  return (
    <div className="App">
      <TopLoadingBar progress={progress} setProgress={setProgress} />
      <Header
        zipcode={zipcode}
        query={query}
        setQuery={setQuery}
        setItemsToDisplay={setItemsToDisplay}
        location={location}
        setDisplayLocationPopup={setDisplayLocationPopup}
        setIsLoading={setIsLoading}
        setProgress={setProgress}
        userLists={userLists}
        setUserLists={setUserLists}></Header>
      {isLoading ? (
        <LoadingBar />
      ) : (
        <DisplayItems searchTerm={searchTerm} items={itemsToDisplay.result} userLists={userLists} setUserLists={setUserLists}></DisplayItems>
      )}
      <GoogleAutoCompleteLocation
        displayLocationPopUp={displayLocationPopUp}
        setDisplayLocationPopup={setDisplayLocationPopup}
        setLocation={setLocation}
        setZipcode={setZipcode}></GoogleAutoCompleteLocation>
    </div>
  );
}

export default App;
