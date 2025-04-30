import React, { useEffect, useState } from 'react';

const Navbar = () => {
  const [isDarkMode, setIsDarkMode] = useState(true); // Default to dark mode for this theme

  // Toggle dark mode and update localStorage
  const toggleDarkMode = () => {
    setIsDarkMode(!isDarkMode);
    if (!isDarkMode) {
      document.documentElement.classList.add('dark');
      localStorage.setItem('theme', 'dark');
    } else {
      document.documentElement.classList.remove('dark');
      localStorage.setItem('theme', 'light');
    }
  };

  // Load dark mode preference from localStorage on initial load
  useEffect(() => {
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'dark' || savedTheme === null) { // Default to dark for this theme
      setIsDarkMode(true);
      document.documentElement.classList.add('dark');
    }
  }, []);

  return (
    <nav className="bg-black border-b border-[#232323] shadow-md">
      <div className="max-w-screen-xl flex flex-wrap items-center justify-between mx-auto p-3">
        <div className="flex items-center">
          <span className="text-cyan-500 text-xl font-bold tracking-tight">BreakBot</span>
        </div>
        
        <div className="flex md:order-2 space-x-4 items-center">
          <p className="text-gray-300 font-semibold hidden sm:block">HackrX - BreakBot</p>
          
          <button
            type="button"
            className="text-black bg-cyan-500 hover:bg-cyan-400 transition-colors focus:ring-2 focus:ring-cyan-600 font-medium rounded-lg text-sm px-4 py-2"
          >
            Github
          </button>
          
          <button
            type="button"
            className="text-black bg-cyan-500 hover:bg-cyan-400 transition-colors focus:ring-2 focus:ring-cyan-600 font-medium rounded-lg text-sm px-4 py-2 md:hidden"
          >
            Upload
          </button>

          
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
