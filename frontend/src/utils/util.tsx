import toast from 'react-hot-toast';

export const successfulToast = (message: string) => {
  toast.success(message);
};

export const failedToast = (message: string) => {
  toast.error(message);
};

export const clearBrowserLocalStorage = () => {
  localStorage.removeItem('userId');
  localStorage.removeItem('token');
  localStorage.removeItem('favorite_list_id');
  localStorage.removeItem('cart_list_id');
};
