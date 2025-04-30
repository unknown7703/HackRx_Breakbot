import React, { useState, useEffect, useRef } from 'react';
import Chat from './Chat';

const ChatBotWindow = () => {
  const [chatHistory, setChatHistory] = useState([]);
  const [userInput, setUserInput] = useState('');
  const chatRef = useRef(null);

  // Add message to chat history
  const addMessageToChatHistory = (sender, message) => {
    setChatHistory((prev) => [...prev, { sender, message }]);
  };

  // Send message handler
  const handleSendMessage = async () => {
    if (userInput.trim() === '') return;
    addMessageToChatHistory('user', userInput);
    setUserInput('');
    try {
      const response = await fetch('http://localhost:8080/chat/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query: userInput }),
      });
      const data = await response.json();
      addMessageToChatHistory('bot', data.bot_message);
    } catch (error) {
      addMessageToChatHistory('bot', 'Sorry, something went wrong.');
    }
  };

  // Auto-scroll
  useEffect(() => {
    if (chatRef.current) {
      chatRef.current.scrollTop = chatRef.current.scrollHeight;
    }
  }, [chatHistory]);

  // Input handlers
  const handleInputChange = (e) => setUserInput(e.target.value);
  const handleKeyPress = (e) => {
    if (e.key === 'Enter') handleSendMessage();
  };

  return (
    <div className="w-full h-full rounded-2xl flex flex-col justify-between p-4 bg-black shadow-2xl border border-[#232323]">
      <div
        ref={chatRef}
        className="flex-grow overflow-y-auto mb-4 space-y-4 scrollbar-thin scrollbar-thumb-[#232323] scrollbar-track-black"
      >
        {chatHistory.map((chat, idx) => (
          <Chat key={idx} sender={chat.sender} message={chat.message} />
        ))}
      </div>
      <div className="flex bg-[#18191a] rounded-xl shadow-inner border border-[#232323]">
        <input
          type="text"
          value={userInput}
          onChange={handleInputChange}
          onKeyDown={handleKeyPress}
          placeholder="Type your message..."
          className="flex-grow px-4 py-3 bg-transparent text-white placeholder-gray-500 focus:outline-none rounded-l-xl"
        />
        <button
          onClick={handleSendMessage}
          className="bg-cyan-500 hover:bg-cyan-400 transition-colors px-6 py-3 rounded-r-xl font-semibold text-black"
        >
          Send
        </button>
      </div>
    </div>
  );
};

export default ChatBotWindow;
