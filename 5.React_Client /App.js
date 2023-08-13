import React, { useState } from 'react';
import axios from 'axios';
import './App.css';
import { Buffer } from 'buffer';

function App() {
  const [inputImage, setInputImage] = useState(null);
  const [outputImage, setOutputImage] = useState(null);
  const [fileInputKey, setFileInputKey] = useState(Date.now());
  const [server, setServer] = useState("http://api-serv.ru:8001"); // new state for selected server

  const servers = [
    "http://158.160.69.94:8001",
    "http://api-serv.ru:8001",
    "http://158.160.69.94:8000",
    // Add more server URLs as needed
  ]; // list of servers


  const loadImage = (e) => {
    const file = e.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = (e) => setInputImage(e.target.result);
      reader.readAsDataURL(file);
    }
  };


  async function processImage() {
    if (!inputImage) return;
    const url = `${server}/process_image`; // use the selected server
    const formData = new FormData();
    formData.append('image', dataURLtoFile(inputImage, 'input.png'));
    try {
      const response = await axios.post(url, formData, {
        responseType: 'blob',
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      const outputImageUrl = URL.createObjectURL(response.data);
      setOutputImage(outputImageUrl);
    } catch (error) {
      console.error(error);
    }
  }

  function dataURLtoFile(dataurl, filename) {
    let arr = dataurl.split(','),
      mime = arr[0].match(/:(.*?);/)[1],
      bstr = Buffer.from(arr[1], 'base64'),
      n = bstr.length,
      u8arr = new Uint8Array(n);

    for (let i = 0; i < n; i++) {
      u8arr[i] = bstr[i];
    }
    return new File([u8arr], filename, { type: mime });
  }


  const clearImages = () => {
    setInputImage(null);
    setOutputImage(null);
    setFileInputKey(Date.now());
  };


  return (
    <div className="App">
      <b>Choose Server:</b>
      {servers.map((srv, idx) => (
        <div key={idx}>
          <input
            type="radio"
            id={`server${idx}`}
            checked={server === srv}
            onChange={() => setServer(srv)}
          />
          <label htmlFor={`server${idx}`}><font size="1">{srv}</font></label>
        </div>
      ))}

      <h2>Input Image</h2>
      {inputImage ? (
        <img src={inputImage} alt="Input" style={{ maxWidth: '100%', maxHeight: '200px' }} />
      ) : null}
      <h2>Output Image</h2>
      {outputImage ? (
        <img src={outputImage} alt="Output" style={{ maxWidth: '100%', maxHeight: '200px' }} />
      ) : null}
      <div style={{ display: 'flex', justifyContent: 'space-between', width: 'fit-content', margin: 'auto' }}>
        <div>
          <input
            type="file"
            accept="image/*"
            onChange={loadImage}
            key={fileInputKey}
            className="hidden-input"
            id="file-input"
          />
          <label htmlFor="file-input" className="custom-file-button">
            Choose File
          </label>
        </div>
        <div>
          <button className="custom-button" onClick={processImage}>
            Process Image
          </button>
        </div>
        <div>
          <button className="custom-button" onClick={clearImages}>
            Clear Images
          </button>
        </div>
      </div>
    </div>
  );

}

export default App;
