import React, { Component } from 'react';
import Messagebox from './Messagebox';
import axios from 'axios';
import ReactScrollableFeed from 'react-scrollable-feed';
import './style.css';


class Chatarea extends Component {
    constructor() {
        super();
        this.displayMess = []
        this.state = {
          messageList : this.displayMess,
          message : "",
          image : null,
          imageURL : null,
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
            imageURL: URL.createObjectURL(e.target.files[0]),
            image: e.target.files[0]
          })
    }

    appendAns = () => {
        console.log("a: ", this.state.answer)
        if (this.state.answer !== ""){
            this.displayMess.push(<Messagebox mess={this.state.answer} self="message botmessage"/>)
            this.setState({
                messageList : this.displayMess,
                answer : ""
            });
        }
    }

    postText = () => {
        let messagepost = new FormData();
        messagepost.append('user', this.props.customer)
        messagepost.append('message', this.state.message);
        messagepost.append('image', this.state.image);
        axios.post('http://127.0.0.1:8000/', messagepost)
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
            this.displayMess.push(<Messagebox mess={this.state.message} self="message mymessage"/>);
            this.setState({
                messageList : this.displayMess,
                message : ""
            });
        }
        if (this.state.image !== null){
            haveappend = true;
            this.displayMess.push(<Messagebox mess={<img src={this.state.imageURL} style={{width: '90%'}}></img>} self="message mymessage"/>)
            this.setState({
                messageList : this.displayMess,
                image : null,
                imageURL : null
            });
        }
        if (haveappend === true){
            this.postText();
        }
    }
    

    render () {
        return(
            <div className="chat-container">
            <div className="chat-area">
                
                <ReactScrollableFeed className="chat-area">{this.displayMess.map(mes => mes)}</ReactScrollableFeed>
            </div>
            <div className="message-input">
                <div className="image-container">
                    <input type="file" id="image-inputfield" onChange={this.handleImage} accept="image/*"></input>
                    <label for="image-inputfield"><svg className="icon-upload-image" ></svg></label>
                </div>
                <div className="inputfield-container"><input type="text" className="mess-inputfield" value={this.state.message} onChange={this.handleChange} onKeyDown={this.handleKeypress}/></div>              
                <div className="send-container"><button className="send-mes" onClick={this.appendMess}>Send</button></div>
            </div>
            </div>
        );
    }
}

export default Chatarea;