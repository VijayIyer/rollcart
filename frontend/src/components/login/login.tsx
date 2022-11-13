// import './login.css';

import axios from 'axios';
import { useState } from 'react';
import toast, { Toaster } from 'react-hot-toast';
import { useNavigate } from 'react-router-dom';
import { failedToast, successfulToast } from '../../utils/util';
import { LogoHeader } from '../header/Header';
import TopLoadingBar from '../loadingBar/topLoadingBar';
import './login.css';

const SignIn = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [progress, setProgress] = useState(0);

  const handleSubmit = (e: any) => {
    //console.log('what am i?', process.env.REACT_APP_SERVER_BASE_URL);
    e.preventDefault();
    const authData = { username: email, password };
    let baseUri;
    if (process.env.NODE_ENV !== 'production'){
      baseUri = process.env.REACT_APP_SERVER_BASE_URL_LOCAL
    }
    else{
      baseUri = process.env.REACT_APP_SERVER_BASE_URL_PROD
    }
    axios
      .post(baseUri + '/login', {}, { auth: authData })
      .then(async response => {
        setProgress(100);
        if (response.status === 201) {
          const { data } = response;
          successfulToast(data.message);
          await new Promise(res => setTimeout(res, 1000));
          localStorage.setItem('token', data.token);
          localStorage.setItem('userId', email);
          navigate('/', { state: { email, token: data.token } });
        }
      })
      .catch(error => {
        setProgress(100);
        console.log('Error is', error);
        const { response } = error;
        failedToast(response.data.message);
      });
  };

  const navigate = useNavigate();
  return (
    <div>
      <TopLoadingBar progress={progress} setProgress={setProgress} />
      <Toaster />
      <LogoHeader />
      <div className="signInContainer">
        <img src="login.png" alt="" width={600} height={600} />
        <form onSubmit={handleSubmit}>
          <div className="signInForm">
            <h1>Hello,</h1>
            <h2>Welcome back!</h2>

            <div className="field">
              <i className="fa-solid fa-envelope fieldIcon"></i>
              <input
                className="formField"
                type="email"
                placeholder="Your Email"
                name="email"
                id="email"
                value={email}
                required
                onChange={e => setEmail(e.target.value)}
              />
            </div>

            {/* <input className="formField" type="password" placeholder="Enter Password" name="psw" id="psw" required /> */}
            <div className="field">
              <i className="fa-solid fa-lock fieldIcon"></i>
              <input
                className="formField"
                type="password"
                placeholder="Enter Password"
                name="psw"
                id="psw"
                value={password}
                minLength={2}
                onChange={e => setPassword(e.target.value)}
                required
              />
            </div>

            <button type="submit" className="submitBtn">
              Sign in
            </button>
            <div className="signin">
              <p className="signinText">
                Do not have an account? {'  '}
                <button className="allUnsetButton blueColor " onClick={() => navigate('/register')}>
                  Sign up
                </button>
                .
              </p>
            </div>
          </div>
        </form>
      </div>
    </div>
  );
};

export default SignIn;
