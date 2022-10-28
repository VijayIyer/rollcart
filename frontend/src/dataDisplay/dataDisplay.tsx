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
      <img src={itemThumbnail} alt="" width={80} height={80} />
      <p className="itemName">{itemName}</p>
      {addToCart === 0 ? (
        <button
          className="addItemButton"
          onClick={() => setAddToCart(addToCart + 1)}>
          <i className="fa-solid fa-plus"> </i> Add
        </button>
      ) : (
        <div className="dynamicAddItemButton">
          <button
            className="addItemButtonAction"
            onClick={() => setAddToCart(addToCart - 1)}>
            <i className="fa-solid fa-minus"> </i>
          </button>
          <span className="itemCount">{addToCart}</span>
          <button
            className="addItemButtonAction"
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

      <div className="displayAllItems flex flex-wrap w-100 flex-grow-0 flex-shrink-0">
        {items.map((item: any) => {
          console.log(item);
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
    </div>
  );
};
