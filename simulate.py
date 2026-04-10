import json
import os
from web3 import Web3

# --- CONFIGURATION ---
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

def run_scenario(scenario_name):
    if not w3.is_connected():
        print("❌ Error: Not connected to Hardhat node.")
        return

    registry, market = load_contracts()
    accounts = w3.eth.accounts
    
    base_path = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_path, "scenarios", scenario_name)
    
    if not os.path.exists(file_path):
        print(f"⚠️ Skipping: {scenario_name} not found in /scenarios")
        return

    with open(file_path, "r") as f:
        data = json.load(f)

    print(f"\n▶️ RUNNING: {scenario_name.upper()}")
    print("=" * 60)

    # Phase 1: Registration & Submission
    for entry in data:
        uid = entry["id"]
        amount = entry["amount"]
        price_eth = entry["price"]
        is_buy = entry["is_buy"]
        user_wallet = accounts[uid]

        # Register if needed
        if not registry.functions.isUserRegistered(user_wallet).call():
            role = 2 if is_buy else 1
            registry.functions.registerUser(role).transact({'from': user_wallet})
        
        # Submit Order
        price_wei = w3.to_wei(price_eth, 'ether')
        market.functions.submitOrder(amount, price_wei, is_buy).transact({'from': user_wallet})
        
        type_str = "BUY" if is_buy else "SELL"
        print(f"   [Order] User {uid} -> {type_str}: {amount}kWh @ {price_eth} ETH")

    # Phase 2: Matching
    print("\n--- Matching & Reputation Sorting ---")
    tx_hash = market.functions.matchOrders().transact({'from': accounts[0]})
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    print(f"Done. Gas Used: {receipt.gasUsed}")

    # Phase 3: Trade Results
    try:
        event_logs = market.events.TradeExecuted().get_logs(
            from_block=receipt.blockNumber, 
            to_block=receipt.blockNumber
        )
        if not event_logs:
            print("   Match Result: No matches (Price gap or empty book)")
        for log in event_logs:
            args = log['args']
            print(f"   🤝 MATCH: Buyer {args['buyer'][:6]} bought from Seller {args['seller'][:6]} @ {w3.from_wei(args['price'], 'ether')} ETH")
    except Exception as e:
        print(f"Event Error: {e}")

    # Phase 4: Snapshot of current reputations
    print("\n--- Current Reputations ---")
    # Dynamically check only the accounts available in Hardhat (usually 20)
    for uid in range(len(accounts)):
        user_wallet = accounts[uid]
        # Only call getReputation if the user is actually registered
        if registry.functions.isUserRegistered(user_wallet).call():
            rep = registry.functions.getReputation(user_wallet).call()
            print(f"   User {uid}: {rep}")
    print("-" * 60)

if __name__ == "__main__":
    # Loop through all 10 scenarios
    for i in range(1, 11):
        target_file = f"scen_{i}.json"
        run_scenario(target_file)