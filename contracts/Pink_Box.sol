// we are going to import the 2 contracts here https://github.com/OpenZeppelin/openzeppelin-contracts/tree/master/contracts/proxy/transparent
// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

contract Pink_Box {
    uint256 private num;

    event NumChanged(uint256 newNum);

    function store(uint256 newNum) public {
        num = newNum;
        emit NumChanged(newNum);
    }

    function retrieve() public view returns (uint256) {
        return num;
    }
}
