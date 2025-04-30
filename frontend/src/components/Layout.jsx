import React from 'react';
import Navbar from './Navbar';
import Uploader from './Uploader';
import ChatBotWindow from './ChatWindow';
import FinBotDescription from './FinBotDescription';

const Layout = () => {
  return (
    <div className="flex flex-col w-screen h-screen bg-black text-white">
      <Navbar />
      <div className="flex flex-row w-full h-[90%] px-2 pb-2 gap-2">
        <div className="hidden md:flex w-1/3 h-full justify-center items-center bg-[#18191a] border border-cyan-800 rounded-2xl shadow-lg">
          <FinBotDescription />
        </div>
        <div className="flex flex-1 h-full justify-center items-center bg-[#18191a] border border-cyan-800 rounded-2xl shadow-lg">
          <ChatBotWindow />
        </div>
      </div>
    </div>
  );
};

export default Layout;
