import axios from 'axios';

export const setAuthToken = (token: any) => {
  if (token) {
    axios.defaults.headers.common = {
      'x-access-token': token,
    };
  }
};
