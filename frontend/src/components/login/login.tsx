// import './login.css';

import { useNavigate } from 'react-router-dom';

const LogoHeader = () => {
  const navigate = useNavigate();
  return (
    <div className="header">
      <button className="logo1 allUnsetButton" onClick={() => navigate('/')}>
        <i className="fa-solid fa-cart-shopping fa-2xl"></i>
        <div className="logoTitle">roll</div>
        <div className="logoTitle">cart</div>
      </button>
    </div>
  );
};
const SignIn = () => {
  const navigate = useNavigate();
  return (
    <div>
      <LogoHeader />
      <form>
        <div className="registerContainer">
          <h1>Sign in</h1>

          <label htmlFor="email">
            <b>Email</b>
          </label>
          <input
            className="formField"
            type="text"
            placeholder="Enter Email"
            name="email"
            id="email"
            required
          />

          <label htmlFor="psw">
            <b>Password</b>
          </label>
          <input
            className="formField"
            type="password"
            placeholder="Enter Password"
            name="psw"
            id="psw"
            required
          />

          <button type="submit" className="registerbtn">
            Sign in
          </button>
          <div className="signin">
            <p className="signinText">
              Do not have an account? {'  '}
              <button
                className="allUnsetButton blueColor"
                onClick={() => navigate('/register')}>
                Sign up
              </button>
              .
            </p>
          </div>
        </div>
      </form>
    </div>
  );
};

export default SignIn;
