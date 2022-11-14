import axios from 'axios';
import React, { useEffect } from 'react';
import { useState } from 'react';
import { AddToList } from '../addToList/addToList';
import './dataDisplay.css';

export const ShowItemCard = ({ itemId, itemName, itemPrice, itemThumbnail, productPageUrl, userLists, setUserLists }: any) => {
  const [addToCart, setAddToCart] = useState(0);
  const [favorite, setFavorite] = useState(false);
  const [showListModal, setShowListModal] = useState(false);
  const [selectedLists, setSelectedLists] = useState([]);

  const handleFavouriteItemClicked = () => {
    setFavorite(!favorite);
  };
  return (
    <div className="item" id={itemId}>
      <div className="favoriteItem" onClick={handleFavouriteItemClicked}>
        <i className={`${favorite === true && 'redHeartIcon fa-solid'} fa-regular fa-heart`}></i>
      </div>
      <img className="itemThumbnail" src={itemThumbnail} alt="" width={100} height={90} />
      <p className="itemName">{itemName}</p>
      <div className="addItemRow">
        {addToCart === 0 ? (
          <button className="addItemButton itemThumbnail pointerCursor" onClick={() => setAddToCart(addToCart + 1)}>
            <i className="fa-solid fa-plus"> </i> Add
          </button>
        ) : (
          <div className="dynamicAddItemButton itemThumbnailLeft">
            <button className="addItemButtonAction pointerCursor" onClick={() => setAddToCart(addToCart - 1)}>
              <i className="fa-solid fa-minus"> </i>
            </button>
            <span className="itemCount">{addToCart}</span>
            <button className="addItemButtonAction pointerCursor" onClick={() => setAddToCart(addToCart + 1)}>
              <i className="fa-solid fa-plus"> </i>
            </button>
          </div>
        )}
        <p
          className="addToList pointerCursor"
          id={`addToList-${itemId}`}
          onClick={() => {
            setShowListModal(!showListModal);
          }}>
          <u>Add to list</u>
        </p>
      </div>
      {showListModal && (
        <AddToList
          showListModal={showListModal}
          setShowListModal={setShowListModal}
          userLists={userLists}
          setUserLists={setUserLists}
          selectedLists={selectedLists}
          setSelectedLists={setSelectedLists}
          item={{ itemId, itemName }}
        />
      )}
    </div>
  );
};

export const DisplayItems = ({ searchTerm, items, userLists, setUserLists }: any) => {
  const getCurrentLists = () => {
    axios.get('getLists').then(response => {
      const { data } = response;
      setUserLists(
        data.map((item: { [x: string]: any }) => {
          return { listname: item['listname'], listId: item['listId'] };
        }),
      );
    });
  };

  useEffect(() => {
    getCurrentLists();
  }, []);

  return (
    <div>
      {searchTerm.length > 0 && <h1 className="helperDisplayAllItems">Search results for "{searchTerm}"</h1>}

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
                  userLists={userLists}
                  setUserLists={setUserLists}
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
      <img className="noItemsImageIcon" src="fruits.png" alt="" width={50} height={50} />
      <h3>Please search for any product name</h3>
    </div>
  );
};

// export const
