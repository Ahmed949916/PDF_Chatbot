import React from 'react';
import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';
import PDFChatbotPage from './pages/PDFChatbotPage.js';
import AboutPage from './pages/AboutPage.js';
import Navbar from './pages/Navbar.js';
import './App.css'
function App() {
  return (
    <Router>
    <div >
      <Navbar />
      <div className="content">
        <Routes>
          <Route path="/" element={<PDFChatbotPage />} />
          <Route path="/about" element={<AboutPage />} />
        </Routes>
      </div>
    </div>
  </Router>
  );
}

export default App;
