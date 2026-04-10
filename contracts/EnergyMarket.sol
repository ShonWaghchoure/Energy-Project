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

    // --- ADD THIS LINE: Define the event ---
    event TradeExecuted(address indexed buyer, address indexed seller, uint256 amount, uint256 price);

    Order[] public buyOrders;
    Order[] public sellOrders;

    constructor(address _registryAddr) {
        registry = UserRegistry(_registryAddr);
    }

    function submitOrder(uint256 _amount, uint256 _price, bool _isBuy) external {
        require(registry.isUserRegistered(msg.sender), "Register first");
        Order memory newOrder = Order(msg.sender, _amount, _price, _isBuy);
        
        if (_isBuy) {
            buyOrders.push(newOrder);
        } else {
            sellOrders.push(newOrder);
        }
    }

    function getOrdersCount() external view returns (uint256 buys, uint256 sells) {
        return (buyOrders.length, sellOrders.length);
    }

    function matchOrders() external {
        // Simple matching logic for MVP
        uint256 minLen = buyOrders.length < sellOrders.length ? buyOrders.length : sellOrders.length;

        for (uint256 i = 0; i < minLen; i++) {
            Order storage buy = buyOrders[i];
            Order storage sell = sellOrders[i];

            if (buy.price >= sell.price) {
                uint256 matchedAmount = buy.amount < sell.amount ? buy.amount : sell.amount;

                // --- ADD THIS LINE: Trigger the event ---
                emit TradeExecuted(buy.trader, sell.trader, matchedAmount, sell.price);

                // Update Reputation
                registry.updateReputation(buy.trader, 2);
                registry.updateReputation(sell.trader, 2);
            }
        }

        delete buyOrders;
        delete sellOrders;
    }
}