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
  const [itemIdCreated, setItemIdCreated] = useState(-1);

  const handleFavouriteItemClicked = () => {
    setFavorite(!favorite);
    const favorite_list_id = localStorage.getItem('favorite_list_id');
    if (favorite === false) {
      handleAddItemToList({ listId: favorite_list_id, quantity: 1 });
    } else {
      handleDeleteItemFromList({ listId: favorite_list_id });
    }
  };

  useEffect(() => {
    const cartListId = localStorage.getItem('cart_list_id');
    if (addToCart === 0 && itemIdCreated !== -1) {
      handleDeleteItemFromList({ listId: cartListId });
    } else if (addToCart !== 0) {
      handleAddItemToList({ listId: cartListId, quantity: addToCart });
    }
  }, [addToCart]);

  const handleAddItemToList = ({ listId, quantity }: any) => {
    axios
      .post(`/${listId}/addItem`, {
        item_name: itemName,
        quantity: quantity,
        item_thumbnail: itemThumbnail,
      })
      .then(response => {
        if (response.status === 201) {
          console.log(`Item: ${itemName} added to the cart: ${listId}`);
          const itemId = response.data.split(' ')[1];
          setItemIdCreated(itemId);
          console.log('Response is', response);
        }
      })
      .catch(error => {
        console.log(`Item: ${itemName} was not added to the cart: ${listId}`);
      });
  };

  const handleDeleteItemFromList = ({ listId }: any) => {
    axios
      .delete(`/${listId}/${itemIdCreated}`)
      .then(response => {
        if (response.status === 200) {
          console.log(`Item: ${itemName} deleted from the cart: ${listId}`);
        }
      })
      .catch(error => {
        console.log(`Item: ${itemName} was not deleted from the cart: ${listId}`);
      });
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
          <button
            className="addItemButton itemThumbnail pointerCursor"
            onClick={() => {
              setAddToCart(addToCart + 1);
            }}>
            <i className="fa-solid fa-plus"> </i> Add
          </button>
        ) : (
          <div className="dynamicAddItemButton itemThumbnailLeft">
            <button
              className="addItemButtonAction pointerCursor"
              onClick={() => {
                setAddToCart(addToCart - 1);
              }}>
              <i className="fa-solid fa-minus"> </i>
            </button>
            <span className="itemCount">{addToCart}</span>
            <button
              className="addItemButtonAction pointerCursor"
              onClick={() => {
                setAddToCart(addToCart + 1);
              }}>
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
          item={{ itemId, itemName, itemThumbnail }}
        />
      )}
    </div>
  );
};

export const DisplayItems = ({ searchTerm, items, userLists, setUserLists, setCartCount }: any) => {
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
                  setCartCount={setCartCount}
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
      <h3>Please search for any product</h3>
    </div>
  );
};
