import React from 'react';
import { BrowserRouter, Routes, Route, Link, useLocation } from 'react-router-dom';
import { ShieldAlert, BookOpen, Layers } from 'lucide-react';

import Landing from './pages/Landing';
import Scanner from './pages/Scanner';
import Education from './pages/Education';

function Navigation() {
  const location = useLocation();
  const isActive = (path) => location.pathname === path;

  return (
    <nav className="fixed top-0 left-0 right-0 z-50 glass border-b border-t-0 border-l-0 border-r-0 border-white/10 px-6 py-4 flex justify-between items-center shadow-lg">
      <Link to="/" className="flex items-center space-x-3 hover:opacity-80 transition-opacity">
        <ShieldAlert className="w-8 h-8 text-teal-400" />
        <span className="text-2xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-teal-400 to-blue-500">BlockGuard XAI</span>
      </Link>
      <div className="flex space-x-6 items-center">
        <Link 
          to="/education" 
          className={`flex items-center space-x-2 text-sm font-medium transition-colors ${isActive('/education') ? 'text-teal-400' : 'text-gray-400 hover:text-gray-200'}`}
        >
          <BookOpen className="w-4 h-4" />
          <span>Vulnerability Hub</span>
        </Link>
        <Link 
          to="/scanner" 
          className={`flex items-center space-x-2 px-4 py-2 rounded-xl transition-all ${isActive('/scanner') ? 'bg-teal-500/20 text-teal-400 border border-teal-500/30' : 'bg-white/5 text-white hover:bg-white/10'}`}
        >
          <Layers className="w-4 h-4" />
          <span>Launch Scanner</span>
        </Link>
      </div>
    </nav>
  );
}

export default function App() {
  return (
    <BrowserRouter>
      <Navigation />
      <div className="pt-24">
        <Routes>
          <Route path="/" element={<Landing />} />
          <Route path="/scanner" element={<Scanner />} />
          <Route path="/education" element={<Education />} />
        </Routes>
      </div>
    </BrowserRouter>
  );
}
