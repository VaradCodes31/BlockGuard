// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract LockedEther {

    address public owner;

    constructor() {
        owner = msg.sender;
    }

    // Accept ETH deposits
    function deposit() public payable {}

    // ❌ Problematic withdraw function
    function withdraw() public {
        require(msg.sender == owner, "Not owner");

        // Trying to send ETH using transfer (limited gas)
        payable(owner).transfer(address(this).balance);
    }
}