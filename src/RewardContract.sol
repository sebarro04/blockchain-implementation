// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "./YourToken.sol"; // Importa el contrato del token ERC20

contract TaskRewardContract {
    address public owner;
    YourToken public token; // Token ERC20 que recompensará a los usuarios
    mapping(address => uint256) public userTaskCounts;

    uint256 public tasksRequiredForReward = 10; //Cantidadde tareas requeridas para la recompensa
    uint256 public rewardAmount = 1;            // Cantidad de tokens a recompensar

    event TaskCompleted(address indexed user, uint256 taskCount);

    constructor(address _tokenAddress) {
        owner = msg.sender;
        token = YourToken(_tokenAddress);
    }

    // Función para que los usuarios completen tareas
    function completeTask() external {
        require(msg.sender != address(0), "Invalid sender address");
        userTaskCounts[msg.sender]++;
        emit TaskCompleted(msg.sender, userTaskCounts[msg.sender]);

        if (userTaskCounts[msg.sender] >= tasksRequiredForReward) {
            rewardUser();
        }
    }

    // Función para recompensar a los usuarios
    function rewardUser() internal {
        require(userTaskCounts[msg.sender] >= tasksRequiredForReward, "Not enough tasks completed");
        require(token.balanceOf(address(this)) >= rewardAmount, "Insufficient contract balance");

        // Transfiere tokens al usuario
        require(token.transfer(msg.sender, rewardAmount), "Token transfer failed");

        // Restablece el recuento de tareas del usuario
        userTaskCounts[msg.sender] -= tasksRequiredForReward;
    }
}