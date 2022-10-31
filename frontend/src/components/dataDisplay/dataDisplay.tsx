import React from 'react';
import { useState } from 'react';
import './dataDisplay.css';

export const ShowItemCard = ({
  itemId,
  itemName,
  itemPrice,
  itemThumbnail,
  productPageUrl,
}: any) => {
  const [addToCart, setAddToCart] = useState(0);
  return (
    <div className="item" id={itemId}>
      <img
        className="itemThumbnail"
        src={itemThumbnail}
        alt=""
        width={80}
        height={80}
      />
      <p className="itemName">{itemName}</p>
      {addToCart === 0 ? (
        <button
          className="addItemButton itemThumbnail pointerCursor"
          onClick={() => setAddToCart(addToCart + 1)}>
          <i className="fa-solid fa-plus"> </i> Add
        </button>
      ) : (
        <div className="dynamicAddItemButton itemThumbnailLeft">
          <button
            className="addItemButtonAction pointerCursor"
            onClick={() => setAddToCart(addToCart - 1)}>
            <i className="fa-solid fa-minus"> </i>
          </button>
          <span className="itemCount">{addToCart}</span>
          <button
            className="addItemButtonAction pointerCursor"
            onClick={() => setAddToCart(addToCart + 1)}>
            <i className="fa-solid fa-plus"> </i>
          </button>
        </div>
      )}
    </div>
  );
};

export const DisplayItems = ({ searchTerm, items }: any) => {
  return (
    <div>
      {searchTerm.length > 0 && (
        <h1 className="helperDisplayAllItems">
          Search results for "{searchTerm}"
        </h1>
      )}

      {items.length === 0 ? (
        <NoItemsToDisplay />
      ) : (
        <div className="displayAllItems flex flex-wrap w-100 flex-grow-0 flex-shrink-0">
          {items.map((item: any) => {
            return (
              <div className="w-25">
                <ShowItemCard
                  itemId={item.itemId}
                  itemName={item.itemName}
                  productPageUrl={item.productPageUrl}
                  itemPrice={item.itemPrice}
                  itemThumbnail={item.itemThumbnail}
                  key={item.itemId}
                />
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
};

export const NoItemsToDisplay = () => {
  return (
    <div className="noItemsToDisplay">
      <img
        className="noItemsImageIcon"
        src="fruits.png"
        alt=""
        width={50}
        height={50}
      />
      <h3>Please search for any product name</h3>
    </div>
  );
};

// export const
