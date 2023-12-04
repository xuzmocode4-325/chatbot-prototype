import React, {useState} from 'react';
import './App.css';
import logo from './assets/medi-guide-logo.svg';
import send_icon from './assets/send.svg';

const apiEnpoint = process.env.REACT_APP_API_ENDPOINT

const App = () => {
  const [userInput, setUserInput] = useState('');
  const [chatMessages, setChatMessages] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleInputChange = (e) => {
    setUserInput(e.target.value);
  };

  const handleSendMessage = async () => {
    // Add logic to send the user's message (userInput)
    console.log('User Message:', userInput);
    
    // Make API call to Flask server
    try {
      // Set loading state to true
      setLoading(true);

      const response = await fetch(apiEnpoint, {   //process.env.API_ENDPOINT
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ user_input: userInput }),
        timeout: 40000, // Set a timeout in milliseconds
      });

      if (!response.ok) {
        throw new Error('Failed to get a response from the server.');
      }

      const data = await response.json();

      // Update chat messages with the user's input and the chatbot's response
      setChatMessages([
        ...chatMessages,
        { text: userInput, type: 'user' },
        { text: data.output, type: 'bot' },
      ]);

      // Clear the input field after sending the message
      setUserInput('');
    } catch (error) {
      console.error('API Call Error:', error.message);
      // Handle error, display a message to the user, etc.
    } finally {
      // Clear loading state once the API call is complete
      setLoading(false);
      console.log('Loading State:', loading);
    }
  };
  
  return (
    <div className="App">
      <div className="main">
      <div className="site-identity"> 
        <img src={logo} alt="logo" className="logo"/>
        <span>Medi-Guide</span>
      </div>  
        <div className="chat-window">
          {chatMessages.map((message, index) => (
            <div key={index} className={`chat-bubble ${message.type}`} >
              {message.text}
            </div>
          ))}
        </div>
        <div className="chat-footer">
          <div className="input-section">
            <input
              id="user-input"
              name="chat" 
              type="text"  
              className="input-field"
              placeholder="Message Medi-Guide..."
              value={userInput}
              onChange={handleInputChange}
             />
            {/* Display loading indicator if loading is true */}
            {loading && <div className="loading-indicator"></div>}
            <button className="send" onClick={handleSendMessage}>
              <img src={send_icon} alt="send button"/>
            </button>
          </div>
          <p>Medi-Guide is an automated system, 
            and it may not always provide 100% accurate 
            information. The information provided by 
            Medi-Guide is not intended to be a substitute 
            for professional medical advice, diagnosis, 
            or treatment. 
          </p>
        </div>
      </div>
    </div>
  );
};

export default App;
