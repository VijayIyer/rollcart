import axios from 'axios';
import { useEffect, useState } from 'react';
import { Toaster } from 'react-hot-toast';
import { useNavigate } from 'react-router-dom';
import { failedToast, successfulToast } from '../../utils/util';
import './manageLists.css';

export const ManageLists = ({ showListModal, setShowListModal, userLists, setUserLists }: any) => {
  const [newListName, setNewListName] = useState('');
  const navigate = useNavigate();

  const getCurrentLists = () => {
    axios.get('getLists').then(response => {
      const { data } = response;
      setUserLists(data);
    });
  };

  useEffect(() => {
    getCurrentLists();
  }, []);

  const handleAddNewUserListClicked = () => {
    axios
      .post('/addList', {
        listname: newListName,
      })
      .then(response => {
        const { data } = response;
        if (response.status === 201) {
          successfulToast(newListName + ' added to the list!');
          setNewListName('');
        }
        setUserLists(
          userLists.concat({
            listId: data.listId,
            listname: newListName,
          }),
        );
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
        <h1 className="addressTitle">Manage Lists</h1>
      </div>

      <div className="userlistdetails">
        {userLists.map((item: any) => {
          return (
            <div className="userlistItemContainer">
              <div key={item.listId} className={`userlistItem`}>
                <div className="closePopup1 red">
                  <i className="fa-solid fa-xmark fa-xl closePopupButton"></i>
                </div>
                <div className="userlistName">{item.listname}</div>
              </div>
              <button
                className="button-3 viewItemsButton"
                onClick={() => {
                  navigate(`/listDetails/${item.listId}`, { state: { listName: item.listname } });
                }}>
                View Items
              </button>
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
