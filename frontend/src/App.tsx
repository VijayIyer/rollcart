import axios from 'axios';
import React, { useState, useEffect, Dispatch, SetStateAction } from 'react';
import { DisplayItems } from './dataDisplay/dataDisplay';
import Header from './header/Header';
import { LoadingBar } from './loadingBar/loadingBar';
import { GoogleAutoCompleteLocation } from './location/location';

function App() {
  const [zipcode, setZipcode] = useState('47408');
  const [query, setQuery] = useState('');
  const [searchTerm, setSearchTerm] = useState('');
  const [itemsToDisplay, setItemsToDisplay] = useState({ result: [] });
  const [displayLocationPopUp, setDisplayLocationPopup] = useState(false);
  const [location, setLocation] = useState('120 Kingston Drive South, 47408');
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    setSearchTerm(query);
  }, [itemsToDisplay]);

  return (
    <div className="App">
      <Header
        zipcode={zipcode}
        query={query}
        setQuery={setQuery}
        setItemsToDisplay={setItemsToDisplay}
        location={location}
        setDisplayLocationPopup={setDisplayLocationPopup}
        setIsLoading={setIsLoading}></Header>
      {isLoading ? (
        <LoadingBar />
      ) : (
        <DisplayItems
          searchTerm={searchTerm}
          items={itemsToDisplay.result}></DisplayItems>
      )}
      {/* <DisplayItems
        searchTerm={searchTerm}
        items={itemsToDisplay.result}></DisplayItems> */}
      <GoogleAutoCompleteLocation
        displayLocationPopUp={displayLocationPopUp}
        setDisplayLocationPopup={setDisplayLocationPopup}
        setLocation={setLocation}
        setZipcode={setZipcode}></GoogleAutoCompleteLocation>
    </div>
  );
}

export default App;
