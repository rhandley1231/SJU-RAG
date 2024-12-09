import React, {useEffect} from 'react';
import ChatBot from './components/ChatBot';
//import './assets/ChatBot.css';
import './App.css'
import Crest from './assets/Crest.png';

const App = () => {
  useEffect(() => {
    document.title = "Johnny Bot";
    const link = document.querySelector("link[rel*='icon']") || document.createElement('link');
    link.type = 'image/png';
    link.rel = 'icon';
    link.href = Crest; // Use the imported logo
    document.getElementsByTagName('head')[0].appendChild(link);
  }, []);
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

