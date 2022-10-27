import React, { useState, useEffect, Dispatch, SetStateAction } from 'react';
import Header from './header/Header';

function App() {
  const [data, setData] = useState({ zipcode: '', query: '' });

  const handleUpdateZipcode = (zipcode: string) => {
    setData({
      ...data,
      zipcode: zipcode,
    });
  };

  const handleUpdateQuery = (query: string) => {
    setData({
      ...data,
      query: query,
    });
  };

  const handleSearchProducts = () => {};

  return (
    <div className="App">
      <Header
        zipcode={data.zipcode}
        query={data.query}
        updateQuery={handleUpdateQuery}
        updateZipcode={handleUpdateZipcode}></Header>
    </div>
  );
}

export default App;
