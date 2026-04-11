import React, { useState, useCallback } from 'react';
import axios from 'axios';
import { UploadCloud, ShieldAlert, Cpu, CheckCircle, AlertTriangle, FileCode } from 'lucide-react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell, CartesianGrid } from 'recharts';

const VULN_DETAILS = {
  "Reentrancy": {
     description: "This vulnerability occurs when your code makes an external call to an untrusted contract before it resolves its own state (e.g., deducting balances). The malicious contract can recursively loop back into your function, draining your vault.",
     remediation: "Implement the Checks-Effects-Interactions pattern. Ensure all internal state changes (like balances[msg.sender] -= amount) occur BEFORE the external `.call` is executed, or use OpenZeppelin's `nonReentrant` mutex modifier."
  },
  "Ether Lock": {
     description: "This contract intakes Ethereum, but the withdrawal logic is either missing entirely, subject to fatal gas limitations (like the deprecated `.transfer()` limit), or blocked by faulty permission logic. Funds run the risk of permanent freezing.",
     remediation: "Ensure explicit withdrawal functions exist for stuck assets. Furthermore, instead of using `.transfer(...)` which is capped at 2300 gas and reverts on proxy wallets, use modern execution paths: `(bool success, ) = payable(recipient).call{value: amount}(\"\"); require(success);`"
  },
  "Integer": {
     description: "A mathematical breakdown where variables rapidly increase or decrease past their 256-bit memory capability, causing the numbers to loop completely backwards to 0 and destroying the balance tracking mechanisms.",
     remediation: "If compiling in Solidity versions below 0.8.0, wrap all mathematical addition and subtraction with the `SafeMath` library. In versions 0.8.0 and above, this is mostly mitigated globally by native compiler halts."
  },
  "Block Dependency": {
     description: "The logic evaluates outcomes based on blockchain environment artifacts like `block.timestamp` or `blockhash`. Fraudulent miners can locally adjust time nodes down to the exact second needed to exploit specific deterministic conditional checks.",
     remediation: "Never use block parameters as a source of entropy. Offload verifiable random numbers to decentralized Oracle networks such as Chainlink VRF (Verifiable Random Function)."
  }
};

export default function Scanner() {
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

             {/* PROBABILITY DISTRIBUTION (NEW) */}
             {result.all_probabilities && result.all_probabilities.length > 0 && (
                 <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mt-6">
                     {result.all_probabilities.sort((a,b) => b.probability - a.probability).map((prob, idx) => (
                         <div key={idx} className="glass p-4 rounded-xl border border-gray-800 text-center relative overflow-hidden">
                             <div 
                                className="absolute bottom-0 left-0 right-0 bg-teal-500/20" 
                                style={{ height: `${prob.probability * 100}%`, transition: 'height 1s ease-out' }} 
                             />
                             <p className="text-xs text-gray-400 mb-1 relative z-10">{prob.class_name}</p>
                             <p className="text-lg font-bold text-white relative z-10">{(prob.probability * 100).toFixed(1)}%</p>
                         </div>
                     ))}
                 </div>
             )}

             {/* REMEDIATION ADVISORY (NEW) */}
             {VULN_DETAILS[result.prediction.vulnerability] && (
               <div className="mt-6 flex flex-col md:flex-row gap-4 text-left">
                 <div className="flex-1 bg-red-500/10 border border-red-500/20 p-6 rounded-xl relative overflow-hidden">
                   <div className="flex items-center space-x-2 text-red-500 mb-2 font-bold"><AlertTriangle className="w-5 h-5"/> <span>Why this happens</span></div>
                   <p className="text-gray-300 text-sm leading-relaxed">{VULN_DETAILS[result.prediction.vulnerability].description}</p>
                 </div>
                 <div className="flex-1 bg-green-500/10 border border-green-500/20 p-6 rounded-xl relative overflow-hidden">
                   <div className="flex items-center space-x-2 text-green-500 mb-2 font-bold"><ShieldAlert className="w-5 h-5"/> <span>Recommended Fix</span></div>
                   <p className="text-gray-300 text-sm leading-relaxed">{VULN_DETAILS[result.prediction.vulnerability].remediation}</p>
                 </div>
               </div>
             )}

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
                                <Tooltip cursor={{fill: '#ffffff0a'}} contentStyle={{ backgroundColor: '#0f172a', border: '1px solid #1e293b', borderRadius: '8px' }} itemStyle={{ color: '#ffffff' }} />
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
                                <Tooltip cursor={{fill: '#ffffff0a'}} contentStyle={{ backgroundColor: '#0f172a', border: '1px solid #1e293b', borderRadius: '8px' }} itemStyle={{ color: '#ffffff' }} />
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
