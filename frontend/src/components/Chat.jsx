import React, { useState, useEffect, useRef } from 'react';

const Chat = ({ sender, message }) => {
  const isUser = sender === 'user';
  const chatContainerClass = isUser ? 'justify-end' : 'justify-start';
  const chatBubbleClass = isUser ? 'bg-green-200 text-right' : 'bg-gray-200 text-left';

  const [typedText, setTypedText] = useState('');
  const indexRef = useRef(0);

  useEffect(() => {
    if (message) {
      if (!isUser) {
        // Reset state and ref when message changes
       //setTypedText('');
        indexRef.current = 0;
        
        const type = () => {
          console.log(indexRef.current,":",typedText);
          if (indexRef.current < message.length) {
            setTypedText(prevTypedText => prevTypedText + message.charAt(indexRef.current));
            indexRef.current += 1;
            setTimeout(type, 50); // Adjust typing speed as needed
          }
        };

        type();
      } else {
        // Directly display the message for user
        setTypedText(message);
      }
    }
  }, [message, isUser]);

  return (
    <div className={`flex ${chatContainerClass}`}>
      <div className={`max-w-xs p-2 rounded ${chatBubbleClass} font-mono`}>
        {typedText}
        
      </div>
    </div>
  );
};

export default Chat;
