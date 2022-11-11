import { useRouteError } from 'react-router-dom';
import './errorPage.css';

const ErrorPage = () => {
  const error: any = useRouteError();
  return (
    <div id="errorPage">
      <h1>Oops!</h1>
      <p>This page is under construction!</p>
      <p>
        Error:<i> {error.statusText || error.message}</i>
      </p>
    </div>
  );
};

export default ErrorPage;
