import json
import os
from web3 import Web3

# --- CONFIGURATION ---
SCENARIO_FILE = "high_demand.json" 
NODE_URL = "http://127.0.0.1:8545"
# ---------------------

w3 = Web3(Web3.HTTPProvider(NODE_URL))

def load_contracts():
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
    
    base_path = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_path, "scenarios", SCENARIO_FILE)
    with open(file_path, "r") as f:
        data = json.load(f)

    print(f"\n🚀 RUNNING REPUTATION-WEIGHTED SCENARIO: {SCENARIO_FILE.upper()}")
    print("-" * 60)

    # Phase 1: Registration & Submission
    for entry in data:
        uid = entry["id"]
        amount = entry["amount"]
        price_eth = entry["price"]
        is_buy = entry["is_buy"]
        user_wallet = accounts[uid]

        if not registry.functions.isUserRegistered(user_wallet).call():
            role = 2 if is_buy else 1
            registry.functions.registerUser(role).transact({'from': user_wallet})
        
        price_wei = w3.to_wei(price_eth, 'ether')
        market.functions.submitOrder(amount, price_wei, is_buy).transact({'from': user_wallet})
        
        type_str = "BUY" if is_buy else "SELL"
        print(f"✅ User {uid} submitted {type_str}: {amount}kWh @ {price_eth} ETH")

    # Phase 2: Matching
    print("\n--- Triggering Reputation-Weighted Matching ---")
    tx_hash = market.functions.matchOrders().transact({'from': accounts[0]})
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

    # Phase 3: Trade Results
    print("\n--- Trade Results ---")
    try:
        event_logs = market.events.TradeExecuted().get_logs(from_block=receipt.blockNumber)
        if not event_logs:
            print("No matches found (Prices did not overlap or order book empty).")
        for log in event_logs:
            args = log['args']
            print(f"🤝 MATCH: Buyer {args['buyer'][:6]} bought from Seller {args['seller'][:6]} @ {w3.from_wei(args['price'], 'ether')} ETH")
    except Exception as e:
        print(f"Event Error: {e}")

    # Phase 4: Final Reputations
    print("\n--- Final Reputation Scores ---")
    unique_users = set([entry["id"] for entry in data])
    for uid in unique_users:
        rep = registry.functions.getReputation(accounts[uid]).call()
        print(f"User {uid} Reputation: {rep}")

if __name__ == "__main__":
    run_scenario()