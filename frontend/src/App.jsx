import React, { useState, useCallback } from 'react';
import axios from 'axios';
import { UploadCloud, ShieldAlert, Cpu, CheckCircle, AlertTriangle, FileCode } from 'lucide-react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell, CartesianGrid } from 'recharts';

export default function App() {
  const [file, setFile] = useState(null);
  const [isHovering, setIsHovering] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [result, setResult] = useState(null);

  const handleDragOver = (e) => {
    e.preventDefault();
    setIsHovering(true);
  };

  const handleDragLeave = () => {
    setIsHovering(false);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setIsHovering(false);
    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      processFile(e.dataTransfer.files[0]);
    }
  };

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files.length > 0) {
      processFile(e.target.files[0]);
    }
  };

  const processFile = async (droppedFile) => {
    setFile(droppedFile);
    setError('');
    setResult(null);
    setLoading(true);

    const formData = new FormData();
    formData.append('file', droppedFile);

    try {
      const res = await axios.post('/api/analyze', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      setResult(res.data.data);
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to process the contract.');
    } finally {
      setLoading(false);
    }
  };

  const ResultCard = ({ title, value, color }) => (
    <div className={`p-6 rounded-2xl glass border ${color} bg-opacity-10 text-center`}>
      <p className="text-gray-400 text-sm font-medium tracking-wide uppercase mb-1">{title}</p>
      <h3 className="text-3xl font-bold text-white">{value}</h3>
    </div>
  );

  return (
    <div className="min-h-screen p-8 text-gray-100 flex flex-col items-center">
      <header className="mb-12 text-center w-full max-w-4xl mx-auto mt-8">
         <div className="inline-flex items-center justify-center p-4 bg-teal-500/10 rounded-full mb-6 relative">
            <div className="absolute inset-0 bg-teal-500/20 blur-xl rounded-full" />
            <ShieldAlert className="w-12 h-12 text-teal-400 relative z-10" />
         </div>
         <h1 className="text-5xl font-extrabold tracking-tight mb-4 bg-clip-text text-transparent bg-gradient-to-r from-teal-400 to-blue-500">
           BlockGuard XAI
         </h1>
         <p className="text-xl text-gray-400 max-w-2xl mx-auto font-light leading-relaxed">
           Drag & Drop your compiled smart contract to scan for severe vulnerabilities utilizing Deep Sequence Learning.
         </p>
      </header>

      {/* UPLOADER */}
      <div 
        className={`w-full max-w-4xl p-12 transition-all duration-300 rounded-3xl border-2 border-dashed glass flex flex-col items-center justify-center cursor-pointer relative overflow-hidden group
          ${isHovering ? 'border-teal-400 bg-teal-500/5 shadow-[0_0_50px_rgba(45,212,191,0.1)]' : 'border-gray-700 hover:border-gray-500'}
          ${loading ? 'opacity-50 pointer-events-none' : ''}`}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
      >
         <input 
            type="file" 
            className="absolute inset-0 w-full h-full opacity-0 cursor-pointer" 
            onChange={handleFileChange}
            disabled={loading}
            accept=".sol,.bin,.hex,.txt"
         />
         {!loading ? (
             <>
                 <div className={`p-6 rounded-full transition-colors duration-300 mb-6 ${isHovering ? 'bg-teal-500/20 text-teal-400' : 'bg-gray-800 text-gray-400 group-hover:text-gray-300'}`}>
                    <UploadCloud className="w-10 h-10" />
                 </div>
                 <h3 className="text-2xl font-semibold mb-2">Drop Contract File Here</h3>
                 <p className="text-gray-500">Supports .bin, .hex, or .txt bytecode exports</p>
             </>
         ) : (
             <div className="flex flex-col items-center">
                 <div className="w-12 h-12 border-4 border-teal-500 border-t-transparent rounded-full animate-spin mb-6" />
                 <h3 className="text-2xl font-semibold animate-pulse text-teal-400">Analyzing Topologies...</h3>
             </div>
         )}
      </div>

      {/* ERROR */}
      {error && (
         <div className="mt-8 p-4 glass border-red-500/30 bg-red-500/10 text-red-200 rounded-xl max-w-4xl w-full flex items-center space-x-3">
             <AlertTriangle className="w-6 h-6 text-red-500" />
             <p>{error}</p>
         </div>
      )}

      {/* RESULTS DASHBOARD */}
      {result && (
         <div className="w-full max-w-6xl mt-16 space-y-8 animate-in fade-in slide-in-from-bottom-8 duration-700 fill-mode-both">
             
             {/* HEADER METRICS */}
             <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                 <ResultCard 
                    title="Vulnerability Class" 
                    value={result.prediction.vulnerability} 
                    color="border-blue-500/30" 
                 />
                 <ResultCard 
                    title="Confidence" 
                    value={`${(result.prediction.confidence * 100).toFixed(2)}%`} 
                    color="border-purple-500/30" 
                 />
                 <ResultCard 
                    title="Risk Severity" 
                    value={result.prediction.risk} 
                    color={
                        result.prediction.risk === 'HIGH' ? 'border-red-500/50 bg-red-500/10 text-red-400' : 
                        result.prediction.risk === 'MEDIUM' ? 'border-orange-500/50 bg-orange-500/10 text-orange-400' : 
                        'border-green-500/50 bg-green-500/10 text-green-400'
                    } 
                 />
             </div>

             {/* DATA VISUALIZATIONS */}
             <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                 
                 {/* SHAP CHART */}
                 <div className="glass p-8 rounded-3xl border-gray-800">
                    <div className="flex items-center space-x-3 mb-6">
                        <Cpu className="w-6 h-6 text-blue-400" />
                        <h3 className="text-xl font-bold">AI Feature Importance (SHAP)</h3>
                    </div>
                    <div className="h-72 w-full">
                        <ResponsiveContainer width="100%" height="100%">
                            <BarChart data={result.shap_data} layout="vertical" margin={{ left: 20, right: 20, top: 0, bottom: 0 }}>
                                <CartesianGrid strokeDasharray="3 3" stroke="#ffffff15" horizontal={false} />
                                <XAxis type="number" stroke="#888" tick={{fill: '#888'}} />
                                <YAxis dataKey="feature" type="category" stroke="#888" tick={{fill: '#ccc'}} width={100} />
                                <Tooltip cursor={{fill: '#ffffff0a'}} contentStyle={{ backgroundColor: '#0f172a', border: '1px solid #1e293b', borderRadius: '8px' }} />
                                <Bar dataKey="impact" radius={[0, 4, 4, 0]}>
                                    {result.shap_data.map((entry, index) => (
                                        <Cell key={`cell-${index}`} fill={entry.impact > 0 ? '#ef4444' : '#3b82f6'} />
                                    ))}
                                </Bar>
                            </BarChart>
                        </ResponsiveContainer>
                    </div>
                    <p className="text-sm text-gray-500 mt-4 text-center">Blue = Lowers likelihood | Red = Increases likelihood of prediction</p>
                 </div>

                 {/* FREQUENCY CHART */}
                 <div className="glass p-8 rounded-3xl border-gray-800">
                    <div className="flex items-center space-x-3 mb-6">
                        <FileCode className="w-6 h-6 text-purple-400" />
                        <h3 className="text-xl font-bold">Opcode Distribution</h3>
                    </div>
                    <div className="h-72 w-full mt-8">
                        <ResponsiveContainer width="100%" height="100%">
                            <BarChart data={result.opcode_distribution} margin={{ left: 0, right: 0, top: 0, bottom: 20 }}>
                                <CartesianGrid strokeDasharray="3 3" stroke="#ffffff15" vertical={false} />
                                <XAxis dataKey="opcode" stroke="#888" tick={{fill: '#888'}} angle={-45} textAnchor="end" height={60} />
                                <YAxis stroke="#888" tick={{fill: '#888'}} />
                                <Tooltip cursor={{fill: '#ffffff0a'}} contentStyle={{ backgroundColor: '#0f172a', border: '1px solid #1e293b', borderRadius: '8px' }} />
                                <Bar dataKey="count" fill="#8b5cf6" radius={[4, 4, 0, 0]} />
                            </BarChart>
                        </ResponsiveContainer>
                    </div>
                 </div>

             </div>

             {/* INSIGHTS */}
             <div className="glass p-8 rounded-3xl border-gray-800 mt-8 mb-24">
                 <h3 className="text-xl font-bold mb-6">Semantic Diagnostics</h3>
                 <div className="space-y-4">
                     {result.insights.map((insight, idx) => (
                         <div key={idx} className={`p-5 rounded-2xl border flex items-start space-x-4
                             ${insight.type === 'risk' ? 'bg-red-500/10 border-red-500/20' : 
                               insight.type === 'warning' ? 'bg-orange-500/10 border-orange-500/20' : 
                               'bg-blue-500/10 border-blue-500/20'}
                         `}>
                             <div className="mt-0.5">
                                 {insight.type === 'risk' && <ShieldAlert className="w-5 h-5 text-red-500" />}
                                 {insight.type === 'warning' && <AlertTriangle className="w-5 h-5 text-orange-500" />}
                                 {insight.type === 'info' && <CheckCircle className="w-5 h-5 text-blue-500" />}
                             </div>
                             <p className={`${
                                 insight.type === 'risk' ? 'text-red-200' : 
                                 insight.type === 'warning' ? 'text-orange-200' : 
                                 'text-blue-200'
                             }`}>{insight.msg}</p>
                         </div>
                     ))}
                     {result.insights.length === 0 && (
                         <div className="p-5 rounded-2xl bg-green-500/10 border border-green-500/20 flex items-center space-x-4 text-green-200">
                             <CheckCircle className="w-5 h-5 text-green-500" />
                             <p>No immediate structural macro-risks parsed from heuristic signatures.</p>
                         </div>
                     )}
                 </div>
             </div>

         </div>
      )}
    </div>
  );
}
