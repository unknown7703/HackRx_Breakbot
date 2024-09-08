import React, {useRef} from 'react'
const Uploader =()=>{
    const fileInputRef = useRef();
  
  const handleChange = (event) =>{
    // do something with event data

  }
  
  return(
    <div className='flex flex-col'>
      <button type="button" className="p-3 bg-blue-700 rounded-lg text-white border-gray-200"onClick={()=>fileInputRef.current.click()}>
        Upload Your File
      </button>
      <input onChange={handleChange} multiple={false} ref={fileInputRef} type='file'hidden/>
      <p className='text-grey-100 dark:text-white'>file types - pdf,ppt,docx</p>
    </div>
  )
}
export default Uploader