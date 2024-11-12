import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import '../assets/ChatBoxStyle.css';
import logo from './st-johns-logo.png';

const ChatBot = () => {
    const [query, setQuery] = useState('');
    const [messages, setMessages] = useState([]);
    const [isLoading, setIsLoading] = useState(false);
    const [isTyping, setIsTyping] = useState(false);
    const endOfMessagesRef = useRef(null);

    // Scroll to the bottom when messages change
    useEffect(() => {
        endOfMessagesRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, [messages]);

    // Show typing indicator after a delay when loading
    useEffect(() => {
        if (isLoading) {
            const timer = setTimeout(() => setIsTyping(true), 500);
            return () => clearTimeout(timer);
        } else {
            setIsTyping(false);
        }
    }, [isLoading]);

    // Typewriter effect for displaying text letter by letter
    const typewriterEffect = (text, callback) => {
        let index = 0;
        const interval = setInterval(() => {
            if (index < text.length) {
                callback(text.slice(0, index + 1));
                index++;
            } else {
                clearInterval(interval);
            }
        }, 50); // Adjust typing speed as needed
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (query.trim() === '' || isLoading) return;

        setIsLoading(true);
        const formattedDate = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
        
        // Add user's message to chat history
        const userMessage = { sender: "User", text: query, timestamp: formattedDate };
        setMessages((prevMessages) => [...prevMessages, userMessage]);
        setQuery('');

        // Show "Thinking..." indicator
        const thinkingMessage = { sender: "Chatbot", text: "...", timestamp: formattedDate };
        setMessages((prevMessages) => [...prevMessages, thinkingMessage]);

        try {
            const response = await axios.post('http://localhost:8000/api/rag-query/', { question: query });
            const responseText = response.data.answer.trim();

            // Remove thinking indicator
            setMessages((prevMessages) => prevMessages.slice(0, -1));

            // Add an empty bot message for typewriter effect
            const botMessage = { sender: "Chatbot", text: '', timestamp: formattedDate };
            setMessages((prevMessages) => [...prevMessages, botMessage]);

            // Convert URLs into clickable links
            const formattedText = responseText.replace(
                /(https?:\/\/\S+)/g,
                '<a href="$1" target="_blank" rel="noopener noreferrer">$1</a>'
            );

            // Apply typewriter effect
            typewriterEffect(formattedText, (text) => {
                setMessages((prevMessages) => {
                    const newMessages = [...prevMessages];
                    newMessages[newMessages.length - 1].text = text;
                    return newMessages;
                });
            });

        } catch (error) {
            const errorMessage = { sender: "System", text: "Error: Unable to reach the server", timestamp: formattedDate };
            setMessages((prevMessages) => [...prevMessages, errorMessage]);
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="chatbox-container">
            <div className="chatbox-header">
                <img src={logo} alt="St. John's University Logo" />
            </div>
            <div className="chatbox-messages">
                {messages.map((msg, index) => (
                    <div key={index} className={`message ${msg.sender.toLowerCase()}`}>
                        <span dangerouslySetInnerHTML={{ __html: `<strong>${msg.sender}:</strong> ${msg.text}` }} />
                        <span className="timestamp">{msg.timestamp}</span>
                    </div>
                ))}
                {isTyping && (
                    <div className="typing-indicator">
                        <span></span><span></span><span></span>
                    </div>
                )}
                <div ref={endOfMessagesRef}></div>
            </div>
            <form onSubmit={handleSubmit} className="chatbox-input">
                <input
                    type="text"
                    placeholder="Type your message..."
                    aria-label="Type your message"
                    value={query}
                    onChange={(e) => setQuery(e.target.value)}
                    disabled={isLoading}
                />
                <button type="submit" disabled={isLoading} aria-label="Send message">Send</button>
            </form>
        </div>
    );
};

export default ChatBot;