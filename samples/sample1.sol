pragma solidity ^0.8.0;

contract VulnerableBank {

    mapping(address => uint) public balances;

    // Deposit ETH into the contract
    function deposit() public payable {
        balances[msg.sender] += msg.value;
    }

    // Withdraw ETH (VULNERABLE FUNCTION)
    function withdraw(uint _amount) public {
        require(balances[msg.sender] >= _amount, "Insufficient balance");

        // ❌ Vulnerability: Sending ETH before updating balance
        (bool success, ) = msg.sender.call{value: _amount}("");
        require(success, "Transfer failed");

        // State update happens AFTER external call
        balances[msg.sender] -= _amount;
    }

    // Check contract balance
    function getBalance() public view returns (uint) {
        return address(this).balance;
    }
}