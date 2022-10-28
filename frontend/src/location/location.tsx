import { useState } from 'react';
import Autocomplete from 'react-google-autocomplete';
import './location.css';
const mapsAPIKey = 'AIzaSyBoyEc3RNYZNF1teZIEZDpVjQBgnjE1AEs';

export const GoogleAutoCompleteLocation = ({
  displayLocationPopUp,
  setDisplayLocationPopup,
  setLocation,
  setZipcode,
}: any) => {
  const [displayErrorMessage, setDisplayErrorMessage] = useState(false);

  if (!displayLocationPopUp) {
    return <></>;
  }
  return (
    <div className="googleAutoCompleteLocationDiv" id="abc">
      <div className="locationPopupTitle">
        <div
          className="closePopup"
          onClick={() => setDisplayLocationPopup(!displayLocationPopUp)}>
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
          apiKey={mapsAPIKey}
          onPlaceSelected={place => {
            const zipcodeFromAddress =
              place.formatted_address.match(/\b\d{5}\b/g);
            if (zipcodeFromAddress) {
              setLocation(place.formatted_address);
              setZipcode(place.formatted_address.match(/\b\d{5}\b/g));
              setDisplayLocationPopup(!displayLocationPopUp);
              setDisplayErrorMessage(false);
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
          <i className="fa fa-warning"></i> Please enter a zipcode{' '}
        </h3>
      )}
    </div>
  );
};
