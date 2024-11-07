import { useState } from 'react';
import axios from 'axios';
import '../assets/ChatBot.css';

const ChatBot = () => {
  const [query, setQuery] = useState('');
  const [displayedText, setDisplayedText] = useState('');
  const [messages, setMessages] = useState([]); // Array to store chat history

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (query.trim() === '') return;
  
    // Add user's message to the chat history
    setMessages((prev) => [...prev, { text: query, isUser: true }]);
    setQuery(''); // Clear the input field
  
    try {
      // Send request to the backend
      const result = await axios.post('http://localhost:8000/api/rag-query/', { question: query });
      console.log("Backend response:", result.data); // Log the entire response object
      const responseText = result.data.answer.trim(); // Trim any potential leading/trailing whitespace
  
      // Start with an empty bot message for the typewriter effect
      setMessages((prev) => [...prev, { text: '', isUser: false }]);
      typewriterEffect(responseText);
    } catch (error) {
      setMessages((prev) => [...prev, { text: 'An error occurred. Please try again.', isUser: false }]);
    }
  };
   

  const typewriterEffect = (text) => {
    let index = 0;
  
    setMessages((prev) => {
      const newMessages = [...prev];
      newMessages[newMessages.length - 1] = { text: '', isUser: false }; // Initialize with empty text
      return newMessages;
    });
  
    const interval = setInterval(() => {
      setMessages((prev) => {
        const newMessages = [...prev];
        const lastMessage = newMessages[newMessages.length - 1];
  
        // Append the current character to the last message's text
        lastMessage.text = text.slice(0, index + 1); // Ensure we're slicing from the start
  
        return newMessages;
      });
  
      index++;
  
      if (index >= text.length) {
        clearInterval(interval);
      }
    }, 50); // Adjust typing speed
  };
  
  
  return (
    <div className="chatbot-container">
      <div className="messages-container">
        {messages.map((msg, idx) => (
          <div key={idx} className={msg.isUser ? 'message user-message' : 'message bot-message'}>
            {msg.text}
          </div>
        ))}
      </div>
      <form onSubmit={handleSubmit} className="input-container">
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Ask me anything..."
        />
        <button type="submit">Send</button>
      </form>
    </div>
  );
};

export default ChatBot;
