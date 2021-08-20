import React, { Component } from 'react';
import './style.css';

class Messagebox extends Component {
    render () {
        return (
            <div className={this.props.self} >{this.props.mess}</div>
        );
    }
}

export default Messagebox;