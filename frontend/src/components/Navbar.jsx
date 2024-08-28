const Navbar =()=>{
    return(
        <nav className="bg-white border-gray-200 dark:bg-gray-900">
            <div className="max-w-screen-xl flex flex-wrap items-center justify-between mx-auto p-4">
                
                <div className="flex md:order-2 space-x-3 md:space-x-3 rtl:space-x-reverse">
                    <button type="button" className="text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm px-4 py-2 
                    text-center dark:bg-blue-600">Github</button>
                    <button type="button" className="inline text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm px-4 py-2 
                    text-center dark:bg-blue-600 md:hidden">Upload</button>
                </div>
            
            </div>
        </nav>
    );
};
export default Navbar