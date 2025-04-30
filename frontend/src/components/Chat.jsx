import React from 'react';

const Chat = ({ sender, message }) => {
  const isUser = sender === 'user';
  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'}`}>
      <div
        className={`max-w-lg px-5 py-3 rounded-2xl shadow
          ${isUser
            ? 'bg-cyan-500 text-black rounded-br-none'
            : 'bg-[#18191a] text-gray-200 rounded-bl-none border border-[#232323]'}
          `}
      >
        <span className="block text-xs font-semibold mb-1 opacity-60">
          {isUser ? 'You' : 'FinBot'}
        </span>
        <span className="text-base break-words">{message}</span>
      </div>
    </div>
  );
};

export default Chat;
