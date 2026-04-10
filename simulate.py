import json
import os
from web3 import Web3

# --- CONFIGURATION ---
# Change this to "surplus.json", "malicious.json", or "high_demand.json"
SCENARIO_FILE = "high_demand.json" 
# ---------------------

# 1. Connect to local Hardhat node
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))

import os

def load_contracts():
    # Use absolute paths to avoid any directory confusion
    base_path = os.path.dirname(os.path.abspath(__file__))
    
    addr_path = os.path.join(base_path, "ignition", "deployments", "chain-31337", "deployed_addresses.json")
    with open(addr_path, "r") as f:
        addresses = json.load(f)
        reg_addr = addresses["EnergyMarketModule#UserRegistry"]
        mkt_addr = addresses["EnergyMarketModule#EnergyMarket"]

    def get_abi(name):
        abi_path = os.path.join(base_path, "artifacts", "contracts", f"{name}.sol", f"{name}.json")
        with open(abi_path, "r") as f:
            return json.load(f)["abi"]

    registry = w3.eth.contract(address=reg_addr, abi=get_abi("UserRegistry"))
    market = w3.eth.contract(address=mkt_addr, abi=get_abi("EnergyMarket"))
    
    return registry, market

def run_scenario():
    if not w3.is_connected():
        print("❌ Error: Not connected to Hardhat node.")
        return

    registry, market = load_contracts()
    accounts = w3.eth.accounts
    
    # Load Scenario Data
    file_path = os.path.join("scenarios", SCENARIO_FILE)
    if not os.path.exists(file_path):
        print(f"❌ Error: {file_path} not found. Create a 'scenarios' folder first.")
        return

    with open(file_path, "r") as f:
        data = json.load(f)

    print(f"\n🚀 STARTING SCENARIO: {SCENARIO_FILE.upper()}")
    print("-" * 50)

    # Phase 1: Registration & Submission
    for entry in data:
        uid = entry["id"]
        amount = entry["amount"]
        price_eth = entry["price"]
        is_buy = entry["is_buy"]
        user_wallet = accounts[uid]

        # Ensure user is registered
        if not registry.functions.isUserRegistered(user_wallet).call():
            role = 2 if is_buy else 1
            registry.functions.registerUser(role).transact({'from': user_wallet})
        
        # Submit Order
        price_wei = w3.to_wei(price_eth, 'ether')
        market.functions.submitOrder(amount, price_wei, is_buy).transact({'from': user_wallet})
        
        type_str = "BUY" if is_buy else "SELL"
        print(f"✅ User {uid} submitted {type_str}: {amount}kWh @ {price_eth} ETH")

    # Phase 2: Matching
    print("\n--- Triggering Matching Engine ---")
    tx_hash = market.functions.matchOrders().transact({'from': accounts[0]})
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    print(f"Market cleared. Gas Used: {receipt.gasUsed}")

    # Phase 3: Display Trade Results (Events)
    print("\n--- Trade Results (On-Chain Events) ---")
    
    # Check if the event exists in the ABI we just loaded
    market_events = [e['name'] for e in market.abi if e['type'] == 'event']
    if "TradeExecuted" not in market_events:
        print("⚠️ Warning: 'TradeExecuted' not in ABI. Run 'npx hardhat clean && npx hardhat compile'.")
    else:
        try:
            event_logs = market.events.TradeExecuted().get_logs(
                from_block=receipt.blockNumber, 
                to_block=receipt.blockNumber
            )
            if not event_logs:
                print("No matches found in this round.")
            for log in event_logs:
                args = log['args']
                print(f"🤝 MATCH: Buyer {args['buyer'][:6]} bought {args['amount']}kWh from Seller {args['seller'][:6]} @ {w3.from_wei(args['price'], 'ether')} ETH")
        except Exception as e:
            print(f"Could not fetch events: {e}")

    # Phase 4: Reputation Check
    print("\n--- Current Reputation Scores ---")
    unique_users = set([entry["id"] for entry in data])
    for uid in unique_users:
        rep = registry.functions.getReputation(accounts[uid]).call()
        print(f"User {uid} Reputation: {rep}")

if __name__ == "__main__":
    run_scenario()