import React, { Component } from 'react';
import Messagebox from './Messagebox';
import './Chatarea.css';


class Chatarea extends Component {
    constructor() {
        super();
        this.state = {
          messageList : [],
          message : '',
        };
    }
    
    

    render () {
        const {text} = this.props;
        return(
            <div className="chatarea">
                {text}
            </div>
        );
    }
}

export default Chatarea;