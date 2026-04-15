# P2P Energy Trading System with Reputation-Priority Matching (RWDA-Inspired)

---

## 🧠 Abstract

This project presents a decentralized Peer-to-Peer (P2P) energy trading system built using blockchain technology. The system introduces a **Reputation-Priority Matching Algorithm inspired by the Reputation Weighted Decision Algorithm (RWDA)**. 

Unlike traditional markets that prioritize price alone, this system prioritizes **trust (reputation)** while using price as a feasibility constraint.

---

## ⚙️ System Components

### 1. User Registry (Smart Contract)
- Registers users as:
  - Prosumer (Seller)
  - Consumer (Buyer)
- Assigns initial reputation = 50
- Maintains reputation in range [0, 100]

---

### 2. Energy Market (Smart Contract)
- Stores:
  - Buy Orders
  - Sell Orders
- Executes matching logic

---

### 3. Python Simulation (Web3.py + Hardhat)
- Runs 10 scenarios
- Uses ~20 simulated peers (Hardhat accounts)
- Logs trades and reputation changes

---

## 🧠 Matching Logic Overview

### Steps:
1. Users register
2. Users submit buy/sell orders
3. Orders are sorted based on reputation
4. Matching is done pairwise
5. Trades execute if price condition satisfied
6. Reputation updated

---

## ⚠️ RWDA Clarification (IMPORTANT)

### What RWDA Ideally Is:

RWDA Score = α × Reputation + β × Price + γ × Time

---

### What This Project Implements:

RWDA (Simplified) = Reputation Only

Score(trader) = Reputation(trader)

---

### Interpretation:

- Reputation → determines priority
- Price → acts as constraint (buy.price ≥ sell.price)
- Time → not considered

---

### Research Statement (Use This)

> This system implements a **Reputation-Priority Matching Algorithm inspired by RWDA**, where reputation is the dominant factor influencing trade execution priority, while price is used as a feasibility constraint.

---

## 🧾 Pseudocode

---

### Register User

```
FUNCTION registerUser(role):
    IF role == None:
        ERROR

    IF user already registered:
        ERROR

    CREATE user:
        reputation = 50
        role = input
```

---

### Submit Order

```
FUNCTION submitOrder(amount, price, isBuy):
    IF user not registered:
        ERROR

    CREATE order

    IF isBuy:
        ADD to buyOrders
    ELSE:
        ADD to sellOrders
```

---

### Sort by Reputation (Core Logic)

```
FUNCTION sortByReputation(orderList):

    FOR i FROM 0 TO n:
        FOR j FROM i+1 TO n:

            IF reputation(j) > reputation(i):
                SWAP(order[i], order[j])
```

---

### Match Orders

```
FUNCTION matchOrders():

    sortByReputation(buyOrders)
    sortByReputation(sellOrders)

    iterations = MIN(len(buyOrders), len(sellOrders))

    FOR i FROM 0 TO iterations:

        buy = buyOrders[i]
        sell = sellOrders[i]

        IF buy.price >= sell.price:

            matchedAmount = MIN(buy.amount, sell.amount)

            EXECUTE trade

            UPDATE reputation(buy, +2)
            UPDATE reputation(sell, +2)

    CLEAR all orders
```

---

### Python Simulation Logic

```
FOR each scenario:

    FOR each user entry:
        register if not exists
        submit order

    CALL matchOrders()

    FETCH events

    PRINT trade results
    PRINT reputation snapshot
```

---

## 🧪 Experimental Setup

### Hardware
- Device: MacBook Pro
- Processor: Intel Core i9
- RAM: 16 GB
- OS: macOS

---

### Software Stack
- Hardhat Local Blockchain
- Solidity (Smart Contracts)
- Python (Web3.py)

---

## 🔁 Simulation Details

- Total Scenarios: 10
- Peers: ~20 (Hardhat accounts)
- Each scenario includes:
  - Buyers and Sellers
  - Different price/amount combinations
  - Dynamic registration

---

## 📊 Observations

- High-reputation users are matched first
- System promotes trust-based trading
- Price ensures feasibility but not priority
- Deterministic outputs across simulations

---

## 🚀 Future Work

- Implement full RWDA (weighted scoring)
- Add time priority (FIFO)
- Optimize sorting to O(n log n)
- Introduce penalties for dishonest behavior

---

## 📌 Conclusion

This project demonstrates a decentralized energy trading system where **trust (reputation)** is prioritized over pure pricing mechanisms. The RWDA-inspired approach improves fairness and reliability in peer-to-peer markets.

---

## 🧾 One-Line Summary

A blockchain-based P2P energy trading system using a **reputation-priority matching algorithm inspired by RWDA**, evaluated through multi-scenario simulations on a Hardhat local network.
