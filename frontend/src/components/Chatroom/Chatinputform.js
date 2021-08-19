import axios from 'axios';
import React, { Component } from 'react';
import Chatarea from './Chatarea';

let textInput = React.createRef();

class Chatinputform extends Component {
    constructor() {
        super();
        this.state = {
            text : '',
            image : null,
        };
      }


    
    
    handleChange = () => {
        this.setState({text : textInput.current.value});
        console.log('state: ', this.state);
        console.log(textInput.current.value);
    }

    // handle = (e) => {
    //     this.setState({text:e.target.value})
    // }

    render () {
        return(
            <>
            <Chatarea text={this.state.text} image={this.state.image}></Chatarea>
            <div className="message_input">
                <input type="file" ></input>
                <input type="text" ref={textInput} className="mess" placeholder="Type your message here"/>              
                <button onClick={this.handleChange}>Send</button>
            </div>
            </>
        );
    }
}

export default Chatinputform;

/*class App extends React.Component {
  
    constructor(props) {
      super(props);
      this.state = {
        text : '',
        output : '',
      };
      this.postText = this.postText.bind(this);
      this.handleChange = this.handleChange.bind(this)
    }
  
    handleChange(e){
      this.setState({text:e.target.value})
    }
  
    handleResponse(response){
      const state = this.state
      const data = response.data
    }
  
    postText(){
      axios.post('http://127.0.0.1:8000/', this.state.text)
      .then(res => {
        const output = res.data;
        this.setState({output})
      })
    }
  
    getIntent(){
      axios.get('http://127.0.0.1:8000/')
      .then(res => {
        console.log(res.data)
      })
    }
  
    render() {
      return(
        <div>
          <input type="text" value={this.state.text} onChange={this.handleChange} style={{width: "300px", margin:"10px"}}></input>
          <button onClick={this.postText}>Submit</button>
          <h2 style={{margin:"10px"}}>Intent: {this.state.output}</h2>
        </div>
      );
    }
  }
  
  export default App;*/