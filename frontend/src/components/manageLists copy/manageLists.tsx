import axios from 'axios';
import { JSXElementConstructor, Key, ReactElement, ReactFragment, useEffect, useState } from 'react';
import { Toaster } from 'react-hot-toast';
import { failedToast, successfulToast } from '../../utils/util';
// import './manageLists.css';

export const ManageLists = ({ showListModal, setShowListModal, userLists, setUserLists, selectedList, setSelectedList }: any) => {
  const [newListName, setNewListName] = useState('');

  const getCurrentLists = () => {
    axios.get(process.env.REACT_APP_SERVER_BASE_URL + '/getLists').then(response => {
      const { data } = response;
      console.log('data is', data);
      setUserLists(
        data.map((item: { [x: string]: any }) => {
          return { listname: item['listname'], listId: item['listId'] };
        }),
      );
    });
  };

  const deleteUserListItem = (e: any) => {
    // TODO will implement this once the backend api is completed
  };

  useEffect(() => {
    getCurrentLists();
  }, []);

  //   const availableLists = ['List name-1', 'List name-2', 'List name-3', 'List name-4'];

  const handleUserListItemClicked = (listId: string, listname: string) => {
    // console.log(e);
    setSelectedList({ listId, listname });
  };

  const handleAddNewUserListClicked = () => {
    console.log('new item is', newListName);
    axios
      .post(process.env.REACT_APP_SERVER_BASE_URL + '/addList', {
        listname: newListName,
      })
      .then(response => {
        if (response.status === 201) {
          successfulToast(newListName + ' added to the list!');
          setUserLists(
            userLists.concat({
              listname: newListName,
              listId: response.data.listId,
            }),
          );
        }
      })
      .catch(error => {
        failedToast(newListName + ' was not added to the list, please try again!');
      });
  };

  return showListModal ? (
    <div className="userlist-container">
      <Toaster />
      <div className="userlistPopupTitle">
        <div className="closePopup" onClick={() => setShowListModal(false)}>
          <i className="fa-solid fa-xmark fa-xl closePopupButton"></i>
        </div>
        <h1 className="addressTitle">Add to List</h1>
      </div>
      {userLists.length === 0 ? (
        <p>Please create a new list item!</p>
      ) : selectedList ? (
        <p>{selectedList.listname} is selected!</p>
      ) : (
        <p>Please select an item</p>
      )}

      <div className="userlistdetails">
        {userLists.map(({ listId, listname }: any) => {
          return (
            <div
              key={listId}
              id={listId}
              className={`userlistItem ${selectedList == listId && 'listSelected'}`}
              onClick={() => handleUserListItemClicked(listId, listname)}>
              <div className="userlistName">{listname}</div>
              <div className="closePopup1 red">
                <i className="fa-solid fa-xmark fa-xl closePopupButton"></i>
              </div>
            </div>
          );
        })}
      </div>
      <div className="addUserList">
        <input
          className="inputAddUserList"
          type="text"
          placeholder="Your new list name"
          value={newListName}
          onChange={e => setNewListName(e.target.value)}
        />
        <button className="button-3" onClick={handleAddNewUserListClicked}>
          Add
        </button>
      </div>
    </div>
  ) : (
    <></>
  );
};
