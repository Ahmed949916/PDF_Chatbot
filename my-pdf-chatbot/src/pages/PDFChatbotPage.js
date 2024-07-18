import React ,{useState} from 'react';
import './PDFChatbotPage.css';
const PDFChatbotPage = () => {
    const [inputText,setInputText]=useState('');
    const[outputtext,setOutputText]=useState('');
    const [pdf,setpdf]=useState(null);

    const handlePdfUpload=(event)=>{
        setInputText(event.target.files[0]);
    };
    const handleInputChange=(event)=>{
        setInputText(event.target.value);
    };
    const handleSubmit=()=>{
        setOutputText(`You entered: ${inputText}`);
    };

  return (
    <div  class="pdf-chatbot-container">
      <h1>PDF Chatbot</h1>
      <div class="output-window"> 

        
        <p >{outputtext}</p>
      </div>
      <label htmlFor="pdf-upload" className="custom-file-upload">
          Upload PDF
        </label>
        <input
          type="file"
          id="pdf-upload"
          accept="application/pdf"
          onChange={handlePdfUpload}
        />
      
        <label htmlFor='user-input'>Enter Text</label>
        <input type="text" id='user-input' value={inputText} onChange={handleInputChange}/>
      
      <button onClick={handleSubmit} className='submitbutton'></button>
      <div>
        <label htmlFor='pdf-upload'></label>
        <input type="file" id="pdf-upload" accept="appliacation/pdf" onChange={handlePdfUpload}/>
      </div>
      
     
    </div>
  );


};

export default PDFChatbotPage;
