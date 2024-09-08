import React, { useEffect, useState } from 'react';

const Navbar = () => {
    const [isDarkMode, setIsDarkMode] = useState(false);

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
      if (savedTheme === 'dark') {
        setIsDarkMode(true);
        document.documentElement.classList.add('dark');
      }
    }, []);
  
    return (
      <nav className="bg-white border-gray-200 dark:bg-gray-900">
        <div className="max-w-screen-xl flex flex-wrap items-center justify-between mx-auto p-4">
          <div className="flex md:order-2 space-x-3 md:space-x-3 rtl:space-x-reverse">
            <button
              type="button"
              className="text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm px-4 py-2 text-center dark:bg-blue-600"
            >
              Github
            </button>
            <button
              type="button"
              className="inline text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm px-4 py-2 text-center dark:bg-blue-600 md:hidden"
            >
              Upload
            </button>
            <p className="text-black dark:text-white">HackrX - BreakBot</p>
  
            <button
                onClick={toggleDarkMode}
                className="text-sm bg-blue-500 text-white dark:bg-gray-700 p-2 rounded"
                >
                {isDarkMode ? 'Light Mode' : 'Dark Mode'}
            </button>
          </div>
        </div>
      </nav>
    );
  };
  
  export default Navbar;
  