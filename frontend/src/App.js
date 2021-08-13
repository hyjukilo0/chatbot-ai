import axios from 'axios';
import React from 'react';
import './App.css';

class App extends React.Component {
  
  constructor(props) {
    super(props);
    this.state = {
      text : '',
      output : '',
    };
    this.postText = this.postText.bind(this);
    this.handleChange = this.handleChange.bind(this)
  }


  

  /*componentDidMount() {

      let data ;

      axios.get('http://localhost:8000/')
      .then(res => {
          data = res.data;
          this.setState({
              details : data    
          });
      })
      .catch((err) => console.log(err));
  }*/

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

export default App;

