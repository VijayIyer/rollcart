import { useState } from 'react';
import Autocomplete from 'react-google-autocomplete';
import './location.css';
const mapsAPIKey = 'AIzaSyBoyEc3RNYZNF1teZIEZDpVjQBgnjE1AEs';

export const GoogleAutoCompleteLocation = ({ displayLocationPopUp, setDisplayLocationPopup, setLocation, setZipcode }: any) => {
  const [displayErrorMessage, setDisplayErrorMessage] = useState(false);

  if (!displayLocationPopUp) {
    return <></>;
  }
  return (
    <div className="googleAutoCompleteLocationDiv" id="abc">
      <div className="locationPopupTitle">
        <div className="closePopup" onClick={() => setDisplayLocationPopup(!displayLocationPopUp)}>
          <i className="fa-solid fa-xmark fa-xl closePopupButton"></i>
        </div>
        <h1 className="addressTitle">Choose Zipcode</h1>
      </div>

      <div className="autocompleteReactDiv">
        <Autocomplete
          style={{
            width: '500px',
            height: '40px',
            padding: '5px 10px',
            fontSize: '16px',
            borderRadius: '5px',
          }}
          placeholder="Enter a zipcode"
          apiKey={mapsAPIKey}
          onPlaceSelected={place => {
            const lat = place.geometry.location.lat();
            const long = place.geometry.location.lng();
            localStorage.setItem('lat', lat);
            localStorage.setItem('long', long);
            console.log(lat, long);
            const zipcodeFromAddress = place.formatted_address.match(/[a-zA-Z]{2} \b\d{5}\b/g);
            if (zipcodeFromAddress) {
              setLocation(place.formatted_address.slice(0, -5));
              setZipcode(zipcodeFromAddress[0].slice(3));
              setDisplayLocationPopup(!displayLocationPopUp);
              setDisplayErrorMessage(false);

              localStorage.setItem('zipcode', zipcodeFromAddress[0].slice(3));
              localStorage.setItem('location', place.formatted_address.slice(0, -5));
            } else {
              setDisplayErrorMessage(true);
            }
          }}
          options={{
            types: ['geocode'],
            componentRestrictions: { country: 'us' },
          }}
        />
      </div>
      {displayErrorMessage && (
        <h3 className="errorMessage">
          <i className="fa fa-warning"></i> Please enter a zipcode
        </h3>
      )}
    </div>
  );
};
