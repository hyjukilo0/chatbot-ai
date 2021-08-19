import axios from 'axios';
import React from 'react';
import './App.css';

import Chatarea from './components/Chatroom/Chatarea';
import Chatinputform from './components/Chatroom/Chatinputform';

class App extends React.Component {
  render() {
    return (
      <div>
        <Chatinputform />
      </div>
    )
  }
}

export default App;

