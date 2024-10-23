// src/App.jsx

import React from 'react';
import Chatbot from './components/ChatBot';  // Import ChatBot component

function App() {
  return (
    <div className="App">
      <h1>Welcome to the ChatBot App</h1>
      <Chatbot />  {/* Render the ChatBot */}
    </div>
  );
}

export default App;

