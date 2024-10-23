import { useState } from 'react';
import axios from 'axios';

const Chatbot = () => {
  const [query, setQuery] = useState('');
  const [response, setResponse] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      // Adjust this URL based on your backend's address (localhost or deployed)
      const result = await axios.post('http://localhost:8000/api/rag-query/', { query });
      setResponse(result.data.result);
    } catch (error) {
      setResponse('An error occurred. Please try again.');
    }
  };

  return (
    <div>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Ask me anything..."
        />
        <button type="submit">Send</button>
      </form>
      <div>{response}</div>
    </div>
  );
};

export default Chatbot;
