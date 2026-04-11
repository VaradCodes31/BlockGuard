import React from 'react';
import { Terminal, Lock, AlertTriangle, Clock } from 'lucide-react';

export default function Education() {
  const vulnerabilities = [
    {
      title: "Reentrancy",
      icon: <Terminal className="w-8 h-8 text-red-500" />,
      color: "border-red-500/30",
      description: "A catastrophic vector where a malicious contract repeatedly calls back into a vulnerable vault before the vault updates its internal balance, allowing infinite withdrawals.",
      code: `// VULNERABLE CODE
function withdraw(uint _amount) public {
    require(balances[msg.sender] >= _amount);
    
    // External call made BEFORE state update
    (bool success, ) = msg.sender.call{value: _amount}("");
    
    balances[msg.sender] -= _amount;
}`,
      fix: `// SECURE CODE (Checks-Effects-Interactions)
function withdraw(uint _amount) public {
    require(balances[msg.sender] >= _amount);
    
    // State update BEFORE external call
    balances[msg.sender] -= _amount;
    
    (bool success, ) = msg.sender.call{value: _amount}("");
}`
    },
    {
      title: "Integer Overflow",
      icon: <AlertTriangle className="w-8 h-8 text-purple-500" />,
      color: "border-purple-500/30",
      description: "Occurs when arithmetic equations exceed the massive numeric limits of the Ethereum Virtual Machine (EVM), violently rolling back to absolute zero and destroying accounting logic.",
      code: `// VULNERABLE CODE (Solidity < 0.8.0)
function transfer(address _to, uint256 _value) public {
    require(balanceOf[msg.sender] >= _value);
    // If balanceOf[_to] + _value > 2^256-1, it rolls over to 0!
    balanceOf[_to] += _value;
    balanceOf[msg.sender] -= _value;
}`,
      fix: `// SECURE CODE
// Use SafeMath library or Solidity >= 0.8.0 
// which automatically reverts on overflow
function transfer(address _to, uint256 _value) public {
    require(balanceOf[msg.sender] >= _value);
    balanceOf[_to] += _value;
    balanceOf[msg.sender] -= _value;
}`
    },
    {
      title: "Ether Lock",
      icon: <Lock className="w-8 h-8 text-orange-500" />,
      color: "border-orange-500/30",
      description: "A permanent freezing of assets. Occurs when a contract contains a payable deposit logic but developers fail to expose any successful withdrawal functions, causing all accumulated coins to become trapped in the blockchain forever.",
      code: `// VULNERABLE CODE
contract Vault {
    mapping(address => uint) public balances;
    
    // Users can deposit
    function deposit() public payable {
        balances[msg.sender] += msg.value;
    }
    
    // NO WITHDRAW FUNCTION EXISTS!
}`,
      fix: `// SECURE CODE
contract Vault {
    mapping(address => uint) public balances;
    
    function deposit() public payable { balances[msg.sender] += msg.value; }
    
    // Withdrawal route explicitly defined
    function withdraw(uint _amount) public {
        require(balances[msg.sender] >= _amount);
        balances[msg.sender] -= _amount;
        payable(msg.sender).transfer(_amount);
    }
}`
    },
    {
      title: "Block Dependency",
      icon: <Clock className="w-8 h-8 text-blue-500" />,
      color: "border-blue-500/30",
      description: "When developers use environmental block variables (like block.timestamp) as a source of randomness. Malicious miners can slightly alter these variables to force a win in gambling contracts.",
      code: `// VULNERABLE CODE
function playLottery() public payable {
    require(msg.value == 1 ether);
    // Miners can manipulate block.timestamp!
    if (block.timestamp % 2 == 0) {
        payable(msg.sender).transfer(2 ether);
    }
}`,
      fix: `// SECURE CODE
// use Chainlink VRF (Verifiable Random Function)
function playLottery() public payable {
    require(msg.value == 1 ether);
    // requestRandomness(keyHash, fee);
    // DO NOT rely on block.timestamp
}`
    }
  ];

  return (
    <div className="max-w-6xl mx-auto px-6 py-12 text-white">
      <div className="text-center mb-16 max-w-3xl mx-auto">
        <h1 className="text-5xl font-extrabold tracking-tight mb-6">Threat Intelligence Hub</h1>
        <p className="text-lg text-gray-400">
          Understand the precise source code vulnerabilities that BlockGuard's intelligence network detects.
        </p>
      </div>

      <div className="space-y-12">
        {vulnerabilities.map((vuln, idx) => (
          <div key={idx} className={`glass rounded-3xl border ${vuln.color} p-8 flex flex-col lg:flex-row gap-8 relative overflow-hidden group`}>
            {/* Background Animation Glow */}
            <div className="absolute top-0 right-0 w-64 h-64 bg-white/5 blur-[80px] rounded-full group-hover:bg-white/10 transition-colors duration-700" />
            
            <div className="lg:w-1/3 space-y-4 relative z-10">
              <div className="flex items-center space-x-3 mb-4">
                <div className="p-3 bg-white/5 rounded-xl border border-white/10 shadow-lg">
                  {vuln.icon}
                </div>
                <h2 className="text-3xl font-bold">{vuln.title}</h2>
              </div>
              <p className="text-gray-300 leading-relaxed">
                {vuln.description}
              </p>
            </div>

            <div className="lg:w-2/3 flex flex-col md:flex-row gap-4 relative z-10 w-full">
               <div className="flex-1 bg-[#090b10] border border-red-500/20 rounded-xl p-4 overflow-x-auto shadow-inner">
                 <div className="text-xs text-red-400/70 font-mono mb-2 uppercase tracking-widest border-b border-red-500/20 pb-2">Exploit Pattern</div>
                 <pre className="text-sm font-mono text-red-300/90 whitespace-pre-wrap">
                   {vuln.code}
                 </pre>
               </div>
               <div className="flex-1 bg-[#090b10] border border-green-500/20 rounded-xl p-4 overflow-x-auto shadow-inner">
                 <div className="text-xs text-green-400/70 font-mono mb-2 uppercase tracking-widest border-b border-green-500/20 pb-2">Secure Resolution</div>
                 <pre className="text-sm font-mono text-green-300/90 whitespace-pre-wrap">
                   {vuln.fix}
                 </pre>
               </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
