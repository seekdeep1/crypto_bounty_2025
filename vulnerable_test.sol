// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract VulnerableTest {
    mapping(address => uint) public balances;
    
    function deposit() public payable {
        balances[msg.sender] += msg.value;
    }
    
    // VULNERABLE: Classic reentrancy
    function withdraw() public {
        uint amount = balances[msg.sender];
        (bool success, ) = msg.sender.call{value: amount}("");
        require(success);
        balances[msg.sender] = 0; // State update after external call
    }
    
    // VULNERABLE: Access control issue
    function adminWithdraw() public {
        // Missing onlyOwner modifier
        payable(msg.sender).transfer(address(this).balance);
    }
}
