import { useState } from "react";
import axios from "axios";
import "../assets/ChatBot.css";

const ChatBot = () => {
  const [query, setQuery] = useState("");
  const [messages, setMessages] = useState([]);
  const [sessionId, setSessionId] = useState(null); // Store session ID

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (query.trim() === "") return;

    // Add user's message to the chat history
    setMessages((prev) => [...prev, { text: query, isUser: true }]);
    setQuery(""); // Clear the input field

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

      // Display bot response with typewriter effect
      setMessages((prev) => [
        ...prev,
        { text: "", isUser: false, isTyping: true },
      ]);
      typewriterEffect(responseText);
    } catch (error) {
      setMessages((prev) => [
        ...prev,
        { text: "An error occurred. Please try again.", isUser: false },
      ]);
    }
  };

  const typewriterEffect = (text) => {
    let index = 0;

    setMessages((prev) => {
      const newMessages = [...prev];
      newMessages[newMessages.length - 1] = {
        text: "",
        isUser: false,
        isTyping: true,
      };
      return newMessages;
    });

    const interval = setInterval(() => {
      setMessages((prev) => {
        const newMessages = [...prev];
        const lastMessage = newMessages[newMessages.length - 1];

        // Render partial HTML during typewriting
        lastMessage.text = text.slice(0, index + 1);
        lastMessage.isTyping = true;
        return newMessages;
      });

      index++;

      if (index >= text.length) {
        setMessages((prev) => {
          const newMessages = [...prev];
          const lastMessage = newMessages[newMessages.length - 1];
          lastMessage.isTyping = false; // Stop typing animation
          return newMessages;
        });
        clearInterval(interval);
      }
    }, 50);
  };

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
              <div dangerouslySetInnerHTML={{ __html: msg.text }} />
            )}
          </div>
        ))}
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
