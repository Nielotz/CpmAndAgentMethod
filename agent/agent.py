from dataclasses import dataclass

from agent.supply_chain import SupplyChainData


@dataclass
class AgentData:
    total_cost: float
    total_income: float
    total_profit: float
    buyers: [str]  # Headers in tables.
    sellers: [str]  # Headers in tables.
    profit_table: [[float, ]]
    optimal_transport_table: [[float, ]]


class Agent:
    @classmethod
    def solve(cls, supply_chain_data: SupplyChainData) -> [AgentData, ]:
        pass
