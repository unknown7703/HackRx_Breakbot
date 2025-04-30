import React from 'react';

const FinBotDescription = () => (
  <section className="w-full max-w-xl mx-auto mt-8 mb-6 bg-[#18191a] border border-[#232323] rounded-2xl shadow-lg p-8 flex flex-col items-center text-center">
    <div className="flex items-center mb-4">
      <div className="bg-black border-2 border-cyan-500 rounded-full w-14 h-14 flex items-center justify-center shadow-md mr-3">
        <span className="text-cyan-400 font-bold text-2xl">F</span>
      </div>
      <h1 className="text-3xl font-extrabold tracking-tight text-cyan-400">FinBot</h1>
    </div>
    <p className="text-gray-300 text-lg mb-3">
      <span className="font-semibold text-cyan-400">FinBot</span> is your intelligent insurance assistant agent.
    </p>
    <p className="text-gray-400 mb-2">
      Effortlessly query your insurance documents with state-of-the-art <span className="text-cyan-400 font-semibold">Retrieval-Augmented Generation (RAG)</span> for reliable, context-aware answers.
    </p>
    <p className="text-gray-400 mb-4">
      Need to take action? FinBot features <span className="text-cyan-400 font-semibold">agentic tools</span> to help you <span className="font-semibold">book appointments</span> with insurance experts-directly from your chat.
    </p>
    <div className="flex flex-row gap-3 mt-2">
      <span className="bg-cyan-900/30 text-cyan-300 px-3 py-1 rounded-full text-xs font-medium">Insurance</span>
      <span className="bg-cyan-900/30 text-cyan-300 px-3 py-1 rounded-full text-xs font-medium">Document Q&A</span>
      <span className="bg-cyan-900/30 text-cyan-300 px-3 py-1 rounded-full text-xs font-medium">Appointment Booking</span>
    </div>
  </section>
);

export default FinBotDescription;
