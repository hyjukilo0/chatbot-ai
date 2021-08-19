import React, { Component } from 'react';
import './style.css';

class Messagebox extends Component {
    render () {
        return (
            <div className="message" >{this.props.mess}</div>
        );
    }
}

export default Messagebox;