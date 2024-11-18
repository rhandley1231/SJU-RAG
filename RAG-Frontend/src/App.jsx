import React from 'react';
import ChatBot from './components/ChatBot';
//import './assets/ChatBot.css';
import './App.css'

const App = () => {
  return (
    <div id="root">
      <header className="header">
        <h1>Welcome to Johnny Bot</h1>
      </header>
      <main className="main-content">
        <ChatBot />
      </main>
    </div>
  );
};

export default App;

