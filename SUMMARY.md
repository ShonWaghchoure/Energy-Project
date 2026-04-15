# P2P Energy Trading System with Reputation-Based Matching

## 🧠 Overview

This project implements a decentralized Peer-to-Peer (P2P) energy trading system using blockchain technology. It introduces a reputation-aware matching algorithm to prioritize trustworthy participants in the energy market.

---

## ⚙️ System Components

### 1. User Registry
- Manages user registration
- Assigns roles: Prosumer (seller) or Consumer (buyer)
- Maintains reputation (0–100, initial = 50)

### 2. Energy Market
- Accepts buy/sell orders
- Stores orders in order books
- Executes matching using reputation and price logic

### 3. Python Simulation
- Runs multiple scenarios
- Interacts with contracts using Web3.py
- Logs trades and reputation changes

---

## 🔁 Core Algorithm

### Matching Logic
1. Sort buyers by reputation (descending)
2. Sort sellers by reputation (descending)
3. Match top buyer with top seller
4. Execute trade if buy.price >= sell.price
5. Update reputation
6. Clear order books

---

## 🧾 Pseudocode

### Register User
```
FUNCTION registerUser(role):
    IF role == None:
        ERROR
    IF already registered:
        ERROR
    CREATE user with reputation = 50
```

### Submit Order
```
FUNCTION submitOrder(amount, price, isBuy):
    IF not registered:
        ERROR
    ADD order to respective list
```

### Sort Orders
```
FUNCTION sortByReputation(list):
    FOR i:
        FOR j:
            IF rep[j] > rep[i]:
                SWAP
```

### Match Orders
```
FUNCTION matchOrders():
    sort buyers
    sort sellers
    FOR each pair:
        IF price match:
            EXECUTE trade
            UPDATE reputation
    CLEAR books
```

---

## 🧪 Experimental Setup

### Hardware
- Device: MacBook Pro
- Processor: Intel Core i9
- RAM: 16 GB
- OS: macOS

### Software
- Hardhat (local blockchain)
- Solidity
- Python (Web3.py)

---

## 🔁 Simulation Details

- 10 scenarios executed
- ~20 simulated peers (Hardhat accounts)
- Each scenario includes:
  - User registration
  - Order submission
  - Matching execution
  - Event logging
  - Reputation tracking

---

## 📊 Observations

- High reputation users are prioritized
- Encourages fair and honest participation
- Deterministic behavior across runs
- Gas usage recorded per transaction

---

## 📌 Conclusion

A decentralized energy trading system that integrates trust (reputation) into market matching, improving fairness and reliability over traditional price-only systems.
