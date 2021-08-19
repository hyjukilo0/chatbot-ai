import React, { Component } from 'react';
import Messagebox from './Messagebox';
import axios from 'axios';
import './style.css';


class Chatarea extends Component {
    constructor() {
        super();
        this.displayMess = []
        this.state = {
          messageList : this.displayMess,
          message : "",
          image : null,
          answer : ""
        };
    }
    
    handleChange = (e) => {
        this.setState({message:e.target.value});
    }

    handleKeypress = (e) => {
        if (e.keyCode === 13){
            this.appendMess()
        }
    }

    handleImage = (e) => {
        this.setState({
            image: URL.createObjectURL(e.target.files[0])
          })
    }

    appendAns = () => {
        console.log("a: ", this.state.answer)
        if (this.state.answer !== ""){
            this.displayMess.push(<Messagebox mess={this.state.answer}/>)
            this.setState({
                messageList : this.displayMess,
                answer : ""
            });
        }
    }

    postText = () => {
        axios.post('http://127.0.0.1:8000/', this.state.message)
        .then(res => {
            const answer = res.data;
            this.setState({
                answer
            })
            this.appendAns();
            console.log("b: ", this.state.answer)
        })
    }

    appendMess = () => {
        let haveappend = false;
        if (this.state.message !== "" ){
            haveappend = true;
            this.displayMess.push(<Messagebox mess={this.state.message} />);
            this.setState({
                messageList : this.displayMess,
                message : ""
            });
        }
        if (this.state.image !== null){
            haveappend = true;
            this.displayMess.push(<img src={this.state.image}></img>)
            this.setState({
                messageList : this.displayMess,
                image : null
            });
        }
        if (haveappend === true){
            this.postText();
        }
    }
    

    render () {
        return(
            <div>
            <div className="chatarea">
                {this.displayMess}
            </div>
            <div className="message_input">
                <input type="file" onChange={this.handleImage}></input>
                <input type="text" value={this.state.message} onChange={this.handleChange} onKeyDown={this.handleKeypress} className="mess"/>              
                <button onClick={this.appendMess}>Send</button>
            </div>
            </div>
        );
    }
}

export default Chatarea;