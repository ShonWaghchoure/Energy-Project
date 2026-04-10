# P2P Energy Trading System with Dynamic Reputation Logic

A decentralized Peer-to-Peer (P2P) energy trading market prototype built on the Ethereum blockchain. This project implements a **Reputation-Weighted** framework to ensure trust and reliability in local microgrid energy exchanges.

## 📖 Research Context

In traditional P2P markets, matching is often performed solely based on price. This system introduces a **Reputation Score** (Initial: 50) for each participant. Successful trades increment the reputation, while malicious behavior or delivery failures result in penalties, ensuring that trustworthy prosumers are prioritized in the market.

## 🛠 Tech Stack

- **Blockchain:** Solidity `^0.8.28`
- **Development Suite:** Hardhat 3.0
- **Deployment:** Hardhat Ignition
- **Simulation Engine:** Python 3 (Web3.py)
- **Data Architecture:** JSON-based Market Scenarios

## 📂 Project Structure

- `contracts/`: Solidity smart contracts (`UserRegistry.sol`, `EnergyMarket.sol`).
- `scenarios/`: JSON files defining market conditions (Supply, Demand, Prices).
- `simulate.py`: The Python execution engine that connects the scenarios to the blockchain.
- `ignition/`: Deployment modules and on-chain addresses.

## ⚙️ Setup Instructions

### 1. Installation

Clone the repository and install the NPM dependencies:

```bash
npm install
```

### 2. Python Environment

Create a virtual environment and install the required libraries to run the simulation:

```bash
python3 -m venv venv
source venv/bin/activate
pip install web3
```

## 🚀 Running the Simulation

Follow these steps in order to ensure the blockchain state and Python script are in sync:

### Step 1: Start the Local Node

In your first terminal:

```bash
npx hardhat node
```

### Step 2: Deploy Contracts

In a second terminal, deploy the contracts using Ignition. The `--reset` flag is used to ensure a clean state:

```bash
npx hardhat ignition deploy ./ignition/modules/EnergyMarket.ts --network localhost --reset
```

### Step 3: Execute Scenarios

Open `simulate.py` and set the `SCENARIO_FILE` variable (e.g., "high_demand.json").

Run the simulation:

```bash
python3 simulate.py
```

## 🧪 Included Scenarios

- `high_demand.json`: Simulates a scarcity environment where multiple buyers compete for limited supply.
- `surplus.json`: Simulates a high-generation environment (e.g., peak solar hours) with excess supply.
- `malicious.json`: Used to test the impact of reputation penalties on market participants.

## 📊 Expected Output

Upon running `simulate.py`, the console will display:

- Successful user registrations.
- Order submissions with ETH prices.
- Trade Results: Matches found via overlapping price discovery.
- Reputation Updates: Proof of reputation scores increasing (e.g., 50 -> 52) after successful trades.

## 👨‍💻 Author

**Shon Waghchoure**  
Indian Institute of Information Technology (IIIT) Allahabad
