import Navbar from "./Navbar";
import Uploader from "./Uploader";
import ChatBotWindow from "./ChatWindow";
const Layout =()=>{
    return(
        <div className="flex flex-col w-screen h-screen">
            <div>
                <Navbar/>
            </div>
            <div className="flex flex-row w-[100%] h-[90%]">
                <div className="hidden md:flex flex-row w-[20%] m-1 justify-center items-center border-solid border-2 border-sky-500 rounded-md"><Uploader/></div>
                <div className="flex flex-row w-[100%] m-1 justify-center items-center border-solid border-2 border-sky-500 rounded-md md:w-[80%]"><ChatBotWindow/></div>
            </div>
        </div>
    );
};

export default Layout