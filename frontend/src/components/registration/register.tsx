import { useNavigate } from 'react-router-dom';
import { LogoHeader } from '../header/Header';
import './register.css';
import toast, { Toaster } from 'react-hot-toast';
import axios from 'axios';
import { useState } from 'react';
import { failedToast, successfulToast } from '../../utils/util';
import TopLoadingBar from '../loadingBar/topLoadingBar';

const Register = () => {
  const [fullName, setfullName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [progress, setProgress] = useState(0);

  const handleSubmit = (e: any) => {
    e.preventDefault();
    if (password !== confirmPassword) {
      toast.error('Passwords donot match, please check!');
    }
    const body = { firstname: fullName, lastname: ' ', password, username: email };
    axios
      .post(process.env.REACT_APP_SERVER_BASE_URL + '/register', body)
      .then(async response => {
        setProgress(100);
        if (response.status === 201) {
          console.log(response);
          successfulToast('Registration is Successfull!');
          // TODO need to find a better way to wait for some time.
          await new Promise(res => setTimeout(res, 1500));
          navigate('/login');
        }
      })
      .catch(error => {
        setProgress(100);
        const { response } = error;
        failedToast(response.data.message);
        console.log(error);
      });
  };

  const navigate = useNavigate();
  return (
    <div>
      <TopLoadingBar progress={progress} setProgress={setProgress} />

      <Toaster />
      <LogoHeader />
      <div className="registration-container">
        <form onSubmit={handleSubmit}>
          <div className="registerContainer">
            <h1>Sign Up</h1>

            <div className="field">
              <i className="fa-solid fa-user fieldIcon"></i>
              <input
                className="formField"
                type="text"
                placeholder="Your Name"
                name="fullName"
                id="fullName"
                value={fullName}
                minLength={2}
                onChange={e => setfullName(e.target.value)}
                required
              />
            </div>

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

            <div className="field">
              <i className="fa-solid fa-repeat fieldIcon"></i>
              <input
                className="formField"
                type="password"
                placeholder="Retype Password"
                name="psw-retype"
                id="psw-retype"
                value={confirmPassword}
                minLength={2}
                onChange={e => setConfirmPassword(e.target.value)}
                required
              />
            </div>

            <button type="submit" className="submitBtn">
              Register
            </button>
            <div className="signin">
              <p className="signinText">
                Already have an account?{' '}
                <button className="allUnsetButton blueColor" onClick={() => navigate('/login')}>
                  Sign in
                </button>
                .
              </p>
            </div>
          </div>
        </form>
        <img src="https://mdbcdn.b-cdn.net/img/Photos/new-templates/bootstrap-registration/draw1.webp" alt="" width={800} height={500} />
      </div>
    </div>
  );
};

export default Register;
