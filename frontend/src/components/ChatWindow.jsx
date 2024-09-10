import React, { useState,useEffect,useRef } from 'react';
import Chat from './Chat';

const ChatBotWindow = () => {
  const [chatHistory, setChatHistory] = useState([]);
  const [userInput, setUserInput] = useState(''); 
  const chatRef = useRef(null);

  //user message to chat history
  const addMessageToChatHistory = (sender, message) => {
    setChatHistory((prevChatHistory) => [
      ...prevChatHistory,
      { sender, message }
    ]);
  };

  // call chat api
  const handleSendMessage = async () => {
    setUserInput('');
    if (userInput.trim() === '') return; 
    addMessageToChatHistory('user', userInput);

    try {
      const response = await fetch('http://127.0.0.1:8000/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ text: userInput })
      });

      const data = await response.json();
      const botMessage = data.message.message;

      renderBotMessage(botMessage);

    } catch (error) {
      console.error('Error sending message:', error);
    }

  };

    //add response from api to char render list
  const renderBotMessage = (message) => {
    addMessageToChatHistory('bot', message);
  };

  //auto scroll to bottom in chat window
  useEffect(() => {
    if (chatRef.current) {
      chatRef.current.scrollTop = chatRef.current.scrollHeight;
    }
  }, [chatHistory]);
  

  //event changes
  const handleInputChange = (e) => {
    setUserInput(e.target.value);
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      handleSendMessage();
    }
  };

  return (
    <div className="w-[100%] mx-auto h-[100%] rounded-lg flex flex-col justify-between p-4 bg-white shadow-lg dark:bg-[#212121]">
      <div ref={chatRef}  className="flex-grow overflow-y-auto mb-4 space-y-2">
        {chatHistory.map((chat, index) => (
          <Chat key={index} sender={chat.sender} message={chat.message} />
        ))}
      </div >
      <div className="flex dark:bg-[#2F2F2F]">
        <input
          type="text"
          value={userInput}
          onChange={handleInputChange}
          onKeyPress={handleKeyPress}
          placeholder="Type your message..."
          className="flex-grow p-2 border border-gray-300 rounded-l focus:outline-none dark:bg-[#2F2F2F] text-white"
        />
        <button
          onClick={handleSendMessage}
          className="bg-blue-500 text-white p-2 rounded-r hover:bg-blue-600 transition-colors"
        >
          Send
        </button>
      </div>
    </div>
  );
};

export default ChatBotWindow;
