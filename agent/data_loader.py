import json
from typing import Optional

from agent.agent import AgentData
from agent.supply_chain import SupplyChainData, Trader, Route


def load_data_from_json_file(path: str = "") -> (SupplyChainData, Optional[AgentData]):
    with open(path) as file:
        supply_chain_data: {} = json.load(file)
    supply_chain = supply_chain_data["input"]

    def extract_traders(data: dict):
        return [Trader(capacity=capacity, price=price) for (capacity, price) in zip(data["capacities"], data["prices"])]

    sellers: [Trader, ] = extract_traders(supply_chain["sellers"])
    buyers: [Trader, ] = extract_traders(supply_chain["buyers"])

    routes: [Route, ] = []
    for seller, road in zip(sellers, supply_chain["routes costs"]):
        for buyer, route_cost in zip(buyers, road):
            routes.append(Route(seller=seller, buyer=buyer, transport_cost=route_cost))

    result: AgentData = None
    if "output" in supply_chain_data:
        output = supply_chain_data["output"]
        result = AgentData(total_cost=output["total cost"],
                           total_income=output["total income"],
                           total_profit=output["total profit"],
                           buyers=buyers,
                           sellers=sellers,
                           profit_table=output["profit table"],
                           optimal_transport_table=output["optimal transport table"])

    return SupplyChainData(sellers=sellers, buyers=buyers, routes=routes), result
