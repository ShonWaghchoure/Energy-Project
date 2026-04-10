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
        
        if (_isBuy) {
            buyOrders.push(newOrder);
        } else {
            sellOrders.push(newOrder);
        }
    }

    function matchOrders() external {
        // 1. Sort Buyers by Reputation (Highest First) - Selection Sort
        for (uint i = 0; i < buyOrders.length; i++) {
            for (uint j = i + 1; j < buyOrders.length; j++) {
                if (registry.getReputation(buyOrders[j].trader) > registry.getReputation(buyOrders[i].trader)) {
                    Order memory temp = buyOrders[i];
                    buyOrders[i] = buyOrders[j];
                    buyOrders[j] = temp;
                }
            }
        }

        // 2. Sort Sellers by Reputation (Highest First)
        for (uint i = 0; i < sellOrders.length; i++) {
            for (uint j = i + 1; j < sellOrders.length; j++) {
                if (registry.getReputation(sellOrders[j].trader) > registry.getReputation(sellOrders[i].trader)) {
                    Order memory temp = sellOrders[i];
                    sellOrders[i] = sellOrders[j];
                    sellOrders[j] = temp;
                }
            }
        }

        // 3. Perform the matching
        uint256 minLen = buyOrders.length < sellOrders.length ? buyOrders.length : sellOrders.length;
        for (uint256 i = 0; i < minLen; i++) {
            Order storage buy = buyOrders[i];
            Order storage sell = sellOrders[i];

            // Only match if Buyer is willing to pay at least the Seller's price
            if (buy.price >= sell.price) {
                uint256 matchedAmount = buy.amount < sell.amount ? buy.amount : sell.amount;

                emit TradeExecuted(buy.trader, sell.trader, matchedAmount, sell.price);

                // Update Reputation: +2 points for successful trade
                registry.updateReputation(buy.trader, 2);
                registry.updateReputation(sell.trader, 2);
            }
        }

        // Clear the order book for the next round
        delete buyOrders;
        delete sellOrders;
    }

    function getOrdersCount() external view returns (uint256 buys, uint256 sells) {
        return (buyOrders.length, sellOrders.length);
    }
}