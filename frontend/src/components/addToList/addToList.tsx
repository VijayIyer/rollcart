import axios from 'axios';
import { useEffect, useState } from 'react';
import { Toaster } from 'react-hot-toast';
import { failedToast, successfulToast } from '../../utils/util';
import './addToList.css';
import { AddToListRow } from './addToListRow';

export const AddToList = ({ showListModal, setShowListModal, userLists, setUserLists, selectedLists, setSelectedLists, item }: any) => {
  const handleAddToListButtonClicked = (selectedLists: any) => {
    // console.log('new item is', newListName);
    for (let i = 0; i < selectedLists.length; i = i + 1) {
      const { listId, listname } = selectedLists[i];
      axios
        .post(`/${listId}/addItem`, {
          item_name: item.itemName,
          quantity: 1,
          item_thumbnail: item.itemThumbnail,
        })
        .then(response => {
          if (response.status === 201) {
            successfulToast(item.itemName + ' added to the ' + listname + '!');
          }
        })
        .catch(error => {
          failedToast(`${item.itemName} + ' was not added to the ${listname}, please try again!`);
        });
    }
  };

  return showListModal ? (
    <div className="addtolist-container">
      <Toaster />
      <div className="addtolistPopupTitle">
        <div className="closePopup" onClick={() => setShowListModal(false)}>
          <i className="fa-solid fa-xmark fa-xl closePopupButton"></i>
        </div>
        <h1 className="addtolistTitle">Add to List</h1>
      </div>
      {userLists.length === 0 ? (
        <p>Please create a new list from the manage lists selection!</p>
      ) : (
        <div>
          <p>Please select one or multiple lists!</p>
          <div className="userlistdetails">
            {userLists.map(({ listId, listname }: any) => {
              return <AddToListRow listId={listId} listname={listname} setSelectedLists={setSelectedLists} selectedLists={selectedLists} />;
            })}
          </div>
          <div className="addToListButton">
            <button
              className="button-3"
              onClick={() => {
                handleAddToListButtonClicked(selectedLists);
              }}>
              Add
            </button>
          </div>
        </div>
      )}
    </div>
  ) : (
    <></>
  );
};
