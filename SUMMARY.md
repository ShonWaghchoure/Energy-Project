# P2P Energy Trading System Documentation

## 1. Problem Statement

Traditional centralized energy systems lack transparency, flexibility,
and incentives for prosumers. This project proposes a decentralized
Peer-to-Peer (P2P) energy trading system using blockchain technology,
enhanced with a reputation-based matching mechanism to improve trust,
efficiency, and fairness among participants.

------------------------------------------------------------------------

## 2. System Specifications & Simulation Environment

    Component            Specification
    -------------------- ---------------------------------------------
    Machine              MacBook Pro (16-inch, 2019)
    Processor            2.6 GHz Intel Core i9 (9th Gen, 8-Core)
    Memory               16 GB 2667 MHz DDR4
    Storage              1 TB PCIe-based SSD
    Blockchain Node      Hardhat Network (EVM-compatible local node)
    Node Configuration   20 Pre-funded Accounts (Peers)
    Environment          Python 3.x with Web3.py & Solidity 0.8.28

------------------------------------------------------------------------

## 3. Mathematical Formulas

### A. Reputation Dynamics

R\_{t+1} = min(100, max(0, R_t + Δρ))

Where: - R_t: Current reputation score\
- Δρ: Reputation change (+2 per successful trade)

------------------------------------------------------------------------

### B. Order Matching Condition

P_buy ≥ P_sell

Transaction price = P_sell\
Buyer surplus = P_buy - P_sell

------------------------------------------------------------------------

## 4. Algorithmic Pseudocode

### Algorithm 1: Reputation-Based Sorting

    FOR i = 0 TO length(O) - 1:
        FOR j = i + 1 TO length(O) - 1:
            Rep_i = getReputation(O[i].trader)
            Rep_j = getReputation(O[j].trader)

            IF Rep_j > Rep_i:
                SWAP(O[i], O[j])

------------------------------------------------------------------------

### Algorithm 2: P2P Matching Engine

    limit = MIN(buyOrders.length, sellOrders.length)

    FOR i FROM 0 TO limit - 1:
        BUYER = buyOrders[i]
        SELLER = sellOrders[i]

        IF BUYER.price >= SELLER.price:
            matchedVolume = MIN(BUYER.amount, SELLER.amount)

            EMIT TradeExecuted

            updateReputation(BUYER, +2)
            updateReputation(SELLER, +2)

    CLEAR order books

------------------------------------------------------------------------

## 5. System Architecture Overview

The system consists of the following components: - Users (Buyers and
Sellers) - Smart Contracts (UserRegistry.sol and EnergyMarket.sol) -
Hardhat Local Blockchain Node - Web3.py interaction layer

------------------------------------------------------------------------

## 6. Smart Contract Design

### UserRegistry.sol

-   Handles user registration
-   Maintains reputation scores
-   Functions:
    -   registerUser()
    -   updateReputation()

### EnergyMarket.sol

-   Handles order submission
-   Executes matching logic
-   Emits trade events

------------------------------------------------------------------------

## 7. Data Structures

    struct Order {
        address trader;
        uint price;
        uint amount;
    }

-   buyOrders\[\]: Array storing buyer orders
-   sellOrders\[\]: Array storing seller orders

------------------------------------------------------------------------

## 8. System Logic Flow

1.  Peer Discovery: 20 accounts initialized
2.  Identity Management: registerUser(), initial R = 50
3.  Order Submission: Buy/Sell orders submitted
4.  Matching Epoch:
    -   matchOrders() triggered
    -   Orders sorted by reputation
5.  Execution:
    -   Pairwise matching
6.  Settlement:
    -   Successful trades → +2 reputation

------------------------------------------------------------------------

## 9. Assumptions

-   Fixed reputation increment of +2 per successful trade
-   No malicious behavior handling implemented
-   Matching is index-based after sorting
-   Orders are cleared after each epoch

------------------------------------------------------------------------

## 10. Limitations

-   Bubble Sort has O(n²) complexity
-   Gas cost constraints in EVM
-   No penalty mechanism for failed trades
-   No dynamic pricing mechanism

------------------------------------------------------------------------

## 11. Results / Observations

-   System successfully executes trades between peers
-   Reputation increases over time for active participants
-   Matching efficiency is high for small datasets (≤20 users)

------------------------------------------------------------------------

## 12. Performance Analysis

-   Hardware is sufficient (i9, 16GB RAM)
-   Primary bottleneck: EVM Gas Limit
-   Not scalable for large peer networks without optimization

------------------------------------------------------------------------

## 13. Conclusion

This system demonstrates a decentralized P2P energy trading mechanism
with a reputation-based matching algorithm. It improves trust and
prioritizes reliable participants, making it a strong foundation for
future scalable blockchain-based energy markets.

------------------------------------------------------------------------



**By: Shon Waghchoure**
