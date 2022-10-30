import React, { useState, useEffect, Dispatch, SetStateAction } from 'react';
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
        setProgress={setProgress}></Header>
      {isLoading ? (
        <LoadingBar />
      ) : (
        <DisplayItems
          searchTerm={searchTerm}
          items={itemsToDisplay.result}></DisplayItems>
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
