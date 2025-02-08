import React, { useState } from 'react';
import axios from 'axios';
import './App.css';
import Typewriter from './TypeWriter';

const App = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);

  const sendMessage = async () => {
    if (input.trim() === '') return;

    const newUserMessage = { role: 'user', content: input };
    setMessages((prevMessages) => [...prevMessages, newUserMessage]);
    setLoading(true);
    const currentInput = input;
    setInput('');

    try {
      const response = await axios.post('http://127.0.0.1:5000/chat', { message: currentInput });
      const botReply = response.data.response;
      const newBotMessage = { role: 'assistant', content: botReply };
      setMessages((prevMessages) => [...prevMessages, newBotMessage]);
    } catch (error) {
      console.error('Error:', error);
      setMessages((prevMessages) => [
        ...prevMessages,
        { role: 'assistant', content: "Une erreur est survenue." },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const renderMessageContent = (content) => {
    return <Typewriter text={content} speed={30} />;
  };

  return (
    <div className="app-container">
      <div className="chat-container">
        <div className="chat-box">
          {messages.map((msg, index) => (
            <div key={index} className={`message ${msg.role}`}>
              <p>
                {msg.role === 'assistant'
                  ? renderMessageContent(msg.content)
                  : msg.content}
              </p>
            </div>
          ))}
          {loading && (
            <div className="message assistant">
              <p>Chargement...</p>
            </div>
          )}
        </div>
        <div className="input-container">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Posez votre question sur la cuisine..."
          />
          <button onClick={sendMessage}>Envoyer</button>
        </div>
      </div>
    </div>
  );
};

export default App;