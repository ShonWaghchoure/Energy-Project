// SPDX-License-Identifier: MIT
pragma solidity ^0.8.28;

import "./UserRegistry.sol";

contract EnergyMarket {
    UserRegistry public registry;
    
    struct Order {
        address trader;
        uint256 amount; 
        uint256 price;  
        bool isBuyOrder;
    }

    event TradeExecuted(address indexed buyer, address indexed seller, uint256 amount, uint256 price);

    Order[] public buyOrders;
    Order[] public sellOrders;

    constructor(address _registryAddr) {
        registry = UserRegistry(_registryAddr);
    }

    function submitOrder(uint256 _amount, uint256 _price, bool _isBuy) external {
        require(registry.isUserRegistered(msg.sender), "Register first");
        Order memory newOrder = Order(msg.sender, _amount, _price, _isBuy);
        if (_isBuy) buyOrders.push(newOrder);
        else sellOrders.push(newOrder);
    }

    function matchOrders() external {
        // 1. Sort Buyers by Reputation (Descending)
        for (uint i = 0; i < buyOrders.length; i++) {
            for (uint j = i + 1; j < buyOrders.length; j++) {
                if (registry.getReputation(buyOrders[j].trader) > registry.getReputation(buyOrders[i].trader)) {
                    Order memory temp = buyOrders[i];
                    buyOrders[i] = buyOrders[j];
                    buyOrders[j] = temp;
                }
            }
        }

        // 2. Sort Sellers by Reputation (Descending)
        for (uint i = 0; i < sellOrders.length; i++) {
            for (uint j = i + 1; j < sellOrders.length; j++) {
                if (registry.getReputation(sellOrders[j].trader) > registry.getReputation(sellOrders[i].trader)) {
                    Order memory temp = sellOrders[i];
                    sellOrders[i] = sellOrders[j];
                    sellOrders[j] = temp;
                }
            }
        }

        // 3. Pairwise matching (Top-to-Top)
        uint256 iterations = buyOrders.length < sellOrders.length ? buyOrders.length : sellOrders.length;
        
        for (uint256 i = 0; i < iterations; i++) {
            Order storage buy = buyOrders[i];
            Order storage sell = sellOrders[i];

            // Match only if price overlap exists
            if (buy.price >= sell.price) {
                uint256 matchedAmount = buy.amount < sell.amount ? buy.amount : sell.amount;
                
                emit TradeExecuted(buy.trader, sell.trader, matchedAmount, sell.price);

                registry.updateReputation(buy.trader, 2);
                registry.updateReputation(sell.trader, 2);
            }
        }

        delete buyOrders;
        delete sellOrders;
    }
}