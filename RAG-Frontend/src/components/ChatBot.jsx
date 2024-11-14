import { useState } from 'react';
import axios from 'axios';
import '../assets/ChatBot.css';

const ChatBot = () => {
  const [query, setQuery] = useState('');
  const [messages, setMessages] = useState([]);
  const [sessionId, setSessionId] = useState(null);  // Store session ID

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (query.trim() === '') return;

    // Add user's message to the chat history
    setMessages((prev) => [...prev, { text: query, isUser: true }]);
    setQuery('');  // Clear the input field

    try {
      // Send request to the backend with session ID
      const result = await axios.post('http://localhost:8000/api/rag-query/', {
        question: query,
        session_id: sessionId  // Include session_id if available
      });

      console.log("Backend response:", result.data);  // Log the response
      const responseText = result.data.answer.trim();
      
      // Update session ID if not already set
      if (!sessionId) setSessionId(result.data.session_id);

      // Display bot response with typewriter effect
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
      newMessages[newMessages.length - 1] = { text: '', isUser: false };
      return newMessages;
    });

    const interval = setInterval(() => {
      setMessages((prev) => {
        const newMessages = [...prev];
        const lastMessage = newMessages[newMessages.length - 1];
        lastMessage.text = text.slice(0, index + 1);
        return newMessages;
      });

      index++;

      if (index >= text.length) {
        clearInterval(interval);
      }
    }, 50);
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

