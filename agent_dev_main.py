from agent.agent import Agent
from agent.data_loader import load_data_from_json_file
from agent.supply_chain import SupplyChainData

supply_chain_data, _ = load_data_from_json_file(path="agent/test_data/test_upel_2x3.json")
supply_chain_data: SupplyChainData

result = Agent.solve(supply_chain_data=supply_chain_data)
