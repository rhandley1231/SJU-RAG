import React from 'react';
import ChatBot from './components/ChatBot';
import './assets/ChatBot.css';

function App() {
  return (
    <>
      <div className="header">Welcome to the Johnny Bot</div>
      <div className="main-content">
        <ChatBot />
      </div>
    </>
  );
}

export default App;

