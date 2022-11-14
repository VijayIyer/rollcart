import { useState } from 'react';

export const AddToListRow = ({ listId, listname, selectedLists, setSelectedLists }: any) => {
  const [checked, setChecked] = useState(false);

  const handleUserListItemClicked = (listId: string, listname: string) => {
    // console.log(e);
    setChecked(!checked);
    if (checked === false) {
      const index = selectedLists.findIndex((list: any) => list.listId === listId);
      if (index === -1) {
        setSelectedLists(selectedLists.concat({ listId, listname }));
      }
    } else {
      //   const index = selectedLists.findIndex((list: any) => list.listId === listId);
      setSelectedLists(selectedLists.filter((list: any) => list.listId !== listId));
    }
    console.log(selectedLists);
  };

  return (
    <div key={listId} id={listId} className={`addtolistRow`} onClick={() => handleUserListItemClicked(listId, listname)}>
      <input type="checkbox" checked={checked} />
      <div className="addtolistRowName">{listname}</div>
    </div>
  );
};
