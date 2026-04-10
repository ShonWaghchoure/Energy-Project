import { buildModule } from "@nomicfoundation/hardhat-ignition/modules";

const EnergyMarketModule = buildModule("EnergyMarketModule", (m) => {
  // 1. Deploy the UserRegistry first
  const registry = m.contract("UserRegistry");

  // 2. Deploy EnergyMarket and pass the registry's address to the constructor
  const market = m.contract("EnergyMarket", [registry]);

  return { registry, market };
});

export default EnergyMarketModule;