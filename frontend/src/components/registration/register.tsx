import { useNavigate } from 'react-router-dom';
import { LogoHeader } from '../header/Header';
import './register.css';

const Register = () => {
  const navigate = useNavigate();
  return (
    <div>
      <LogoHeader />
      <form>
        <div className="registerContainer">
          <h1>Sign Up</h1>
          <p>Please fill in the below details to create an account.</p>

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

          <label htmlFor="psw-retype">
            <b>Retype Password</b>
          </label>
          <input
            className="formField"
            type="password"
            placeholder="Retype Password"
            name="psw-retype"
            id="psw-retype"
            required
          />

          <button type="submit" className="registerbtn">
            Register
          </button>
          <div className="signin">
            <p className="signinText">
              Already have an account?{' '}
              <button
                className="allUnsetButton blueColor"
                onClick={() => navigate('/login')}>
                Sign in
              </button>
              .
            </p>
          </div>
        </div>
      </form>
    </div>
  );
};

export default Register;
