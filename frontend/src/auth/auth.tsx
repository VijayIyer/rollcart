import axios from 'axios';

if (process.env.NODE_ENV !== 'production') {
  axios.defaults.baseURL = process.env.REACT_APP_FLASK_API_URL_LOCAL;
} else {
  axios.defaults.baseURL = process.env.REACT_APP_FLASK_API_URL_PROD;
}

console.log('process.env.reactapp', axios.defaults.baseURL);

export const setAuthToken = (token: any) => {
  if (token) {
    axios.defaults.headers.common = {
      'x-access-token': token,
    };
  }
};
