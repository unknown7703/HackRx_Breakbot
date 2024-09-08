import React from 'react';

// Chat component to display individual chat messages
const Chat = ({ sender, message }) => {
  const isUser = sender === 'user';
  const chatContainerClass = isUser ? 'justify-end' : 'justify-start';
  const chatBubbleClass = isUser ? 'bg-green-200 text-right' : 'bg-gray-200 text-left';

  return (
    <div className={`flex ${chatContainerClass}`}>
      <div className={`max-w-xs p-2 rounded ${chatBubbleClass}`}>
        {message}
      </div>
    </div>
  );
};

export default Chat;