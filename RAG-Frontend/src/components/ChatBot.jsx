import { useState, useEffect, useRef } from "react";
import axios from "axios";
import "../assets/ChatBot.css";

const ChatBot = () => {
  const [query, setQuery] = useState("");
  const [messages, setMessages] = useState([]);
  const [sessionId, setSessionId] = useState(null); // Store session ID
  const [isTyping, setIsTyping] = useState(false); // Track typing status

  const messagesEndRef = useRef(null); // Ref to track the last message

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (query.trim() === "") return;

    // Add user's message to the chat history
    setMessages((prev) => [...prev, { text: query, isUser: true }]);
    setQuery(""); // Clear the input field

    // Display typing indicator
    setIsTyping(true);

    try {
      // Send request to the backend with session ID
      const result = await axios.post("http://localhost:8000/api/rag-query/", {
        question: query,
        session_id: sessionId, // Include session_id if available
      });

      console.log("Backend response:", result.data); // Log the response
      const responseText = result.data.answer.trim();

      // Update session ID if not already set
      if (!sessionId) setSessionId(result.data.session_id);

      // Remove typing indicator and add the bot's response
      setIsTyping(false);
      setMessages((prev) => [
        ...prev,
        { text: responseText, isUser: false },
      ]);
    } catch (error) {
      // Remove typing indicator and show an error message
      setIsTyping(false);
      setMessages((prev) => [
        ...prev,
        { text: "An error occurred. Please try again.", isUser: false },
      ]);
    }
  };

  useEffect(() => {
    // Scroll to the bottom whenever messages update
    if (messagesEndRef.current) {
      messagesEndRef.current.scrollIntoView({ behavior: "smooth" });
    }
  }, [messages, isTyping]);

  return (
    <div className="chatbot-container">
      <div className="messages-container">
        {messages.map((msg, idx) => (
          <div
            key={idx}
            className={
              msg.isUser ? "message user-message" : "message bot-message"
            }
          >
            {msg.isUser ? (
              msg.text
            ) : (
              <div
                className="bot-response"
                dangerouslySetInnerHTML={{ __html: msg.text }}
              />
            )}
          </div>
        ))}
        {/* Typing indicator */}
        {isTyping && (
          <div className="message bot-message typing-indicator">
            <span className="dot"></span>
            <span className="dot"></span>
            <span className="dot"></span>
          </div>
        )}
        <div ref={messagesEndRef} /> {/* Reference to the end of messages */}
      </div>
      <form onSubmit={handleSubmit} className="input-container">
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="How can Johnny Bot assist you today?"
        />
        <button type="submit" aria-label="Send">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
            <path
              d="M12 2L12 22M12 2L6 8M12 2L18 8"
              stroke="currentColor"
              stroke-width="3"
              stroke-linecap="round"
              stroke-linejoin="round"
              fill="none"
            />
          </svg>
        </button>
      </form>
    </div>
  );
};

export default ChatBot;