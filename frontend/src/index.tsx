import '@fontsource/roboto/300.css';
import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import reportWebVitals from './reportWebVitals';
import App from './App';
import { createBrowserRouter, RouterProvider } from 'react-router-dom';
import ErrorPage from './routes/errorPage/errorPage';
import Register from './components/registration/register';
import SignIn from './components/login/login';
import AllStorePrices from './components/allstorePrices/allstorePrices';
import { CartDetails, ListDetails } from './components/storePrices/storePrice';

const root = ReactDOM.createRoot(document.getElementById('root') as HTMLElement);

const router = createBrowserRouter([
  {
    path: '/',
    element: <App />,
    errorElement: <ErrorPage />,
  },
  {
    path: '/login',
    element: <SignIn />,
    errorElement: <ErrorPage />,
  },
  {
    path: '/register',
    element: <Register />,
    errorElement: <ErrorPage />,
  },
  {
    path: '/storePrices/:listId',
    element: <AllStorePrices />,
    errorElement: <ErrorPage />,
  },
  {
    path: '/cartDetails',
    element: <CartDetails />,
    errorElement: <ErrorPage />,
  },
  {
    path: '/listDetails/:listId',
    element: <ListDetails />,
    errorElement: <ErrorPage />,
  },
]);

root.render(
  <React.StrictMode>
    <RouterProvider router={router} />
  </React.StrictMode>,
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
