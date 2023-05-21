from agent.agent import Agent
from agent.data_loader import load_data_from_json_file, load_data_from_gui
from agent.supply_chain import SupplyChainData

# supply_chain_data, _ = load_data_from_json_file(path="agent/test_data/simple_test_2x2.json")
# supply_chain_data: SupplyChainData

supply: [] = [1,   1]
demand: [] = [10, 10]
sell_price: [] = [1,   1]
buy_price: [] = [1,   1]
transport_table: [[]] = [[1, 2], [3, 4]]
force_fictional: bool = False

supply_chain_data = load_data_from_gui(supply=supply,
                       demand=demand,
                       sell_price=sell_price,
                       buy_price=buy_price,
                       transport_table=transport_table,
                       force_fictional=force_fictional)
result = Agent.solve(supply_chain_data=supply_chain_data)
