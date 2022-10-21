import React, {useState, useEffect} from 'react';
import logo from './logo.svg';
import './App.css';

function App() {
  const [data, setData] = useState();

  useEffect(() => {
    fetch("/intro").then(
      res => res.json()
    ).then(
      data => {
        setData(data)
        console.log(data)
      }
    )
  })

  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.tsx</code> and save to reload.
        </p>
        <div>
          {(typeof data === 'undefined') ? (
            <a
            className="App-link"
            href="https://reactjs.org"
            target="_blank"
            rel="noopener noreferrer"
            >
              Testing Grocery-budget app
            </a>
          ) : (
            data["welcomeMessage"]
          )}
          
        </div>
      </header>
    </div>
  );
}

export default App;
