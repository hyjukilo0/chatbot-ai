import React from 'react';
import './App.css';

import Chatarea from './components/Chatroom/Chatarea';

class App extends React.Component {
  render() {
    return (
      <div>
        <Chatarea user="khách 1" />
      </div>
    )
  }
}

export default App;

