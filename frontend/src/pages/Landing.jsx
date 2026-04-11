import React from 'react';
import { Link } from 'react-router-dom';
import { ArrowRight, Search, Shield, Zap, Database } from 'lucide-react';

export default function Landing() {
  return (
    <div className="min-h-[calc(100vh-80px)] flex flex-col justify-center items-center text-center px-4">
      {/* HERO SECTION */}
      <div className="max-w-5xl mx-auto space-y-8 mt-12 mb-24 relative">
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-96 h-96 bg-teal-500/20 blur-[120px] rounded-full pointer-events-none" />
        <h1 className="text-6xl md:text-8xl font-black tracking-tighter text-white relative z-10">
          Decentralized <br /> <span className="bg-clip-text text-transparent bg-gradient-to-r from-teal-400 to-blue-600">Smart Scanner.</span>
        </h1>
        <p className="text-xl md:text-2xl text-gray-400 max-w-3xl mx-auto font-light">
          BlockGuard utilizes sequence Deep Learning and predictive Machine Learning 
          Heuristics to reverse-engineer Bytecode and spot severe vulnerabilities in milliseconds.
        </p>
        
        <div className="flex flex-col sm:flex-row justify-center items-center space-y-4 sm:space-y-0 sm:space-x-6 pt-8">
          <Link 
            to="/scanner"
            className="flex items-center space-x-2 px-8 py-4 bg-teal-500 hover:bg-teal-400 text-gray-900 font-bold rounded-xl transition-all shadow-[0_0_40px_rgba(45,212,191,0.4)]"
          >
            <Search className="w-5 h-5" />
            <span>Scan Contract</span>
          </Link>
          <Link 
            to="/education"
            className="flex items-center space-x-2 px-8 py-4 bg-white/5 border border-white/10 hover:bg-white/10 text-white font-medium rounded-xl transition-all"
          >
            <span>Learn More</span>
            <ArrowRight className="w-5 h-5" />
          </Link>
        </div>
      </div>

      {/* FEATURES ROW */}
      <div className="w-full max-w-6xl grid grid-cols-1 md:grid-cols-3 gap-8 pb-32">
        <div className="glass p-8 rounded-3xl border border-gray-800 text-left hover:border-teal-500/30 transition-all">
          <Shield className="w-10 h-10 text-teal-400 mb-6" />
          <h3 className="text-2xl font-bold mb-3">Threat Detection</h3>
          <p className="text-gray-400">Zero-shot identification of Reentrancy, Overflow, Block Timestamp logic, and Ether Locking routines.</p>
        </div>
        <div className="glass p-8 rounded-3xl border border-gray-800 text-left hover:border-blue-500/30 transition-all">
          <Zap className="w-10 h-10 text-blue-400 mb-6" />
          <h3 className="text-2xl font-bold mb-3">Sub-second Speed</h3>
          <p className="text-gray-400">Pure programmatic opcode extraction paired directly with high-efficiency Flask ML tensors.</p>
        </div>
        <div className="glass p-8 rounded-3xl border border-gray-800 text-left hover:border-purple-500/30 transition-all">
          <Database className="w-10 h-10 text-purple-400 mb-6" />
          <h3 className="text-2xl font-bold mb-3">Active Learning</h3>
          <p className="text-gray-400">Your payloads generate constant synthetic arrays to iteratively buffer future LSTM retraining phases.</p>
        </div>
      </div>
    </div>
  );
}
