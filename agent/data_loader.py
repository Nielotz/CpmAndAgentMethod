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

    force_fictional: bool = supply_chain["force fictional"]

    result: AgentData = None
    if "output" in supply_chain_data:
        output = supply_chain_data["output"]
        result = AgentData(total_products_cost=output["total products cost"],
                           total_transport_cost=output["total transport cost"],
                           total_cost=output["total cost"],
                           total_income=output["total income"],
                           total_profit=output["total profit"],
                           buyers=buyers,
                           sellers=sellers,
                           unit_profit_table=output["unit profit table"],
                           optimal_transport_table=output["optimal transport table"])


    return SupplyChainData(sellers=sellers, buyers=buyers, routes=routes, force_fictional=force_fictional), result


def load_data_from_gui(supply: [], demand: [], sell_price: [], buy_price: [], transport_table: [[]],
                       force_fictional: bool) -> SupplyChainData:

    sellers: [Trader, ] = [Trader(capacity=supply_, price=buy_price_) for supply_, buy_price_ in zip(supply, buy_price)]
    buyers: [Trader, ] = [Trader(capacity=supply_, price=buy_price_) for supply_, buy_price_ in zip(demand, sell_price)]

    routes: [Route, ] = []
    sellers_iter = iter(sellers)
    buyers_iter = iter(buyers)
    for row in transport_table:
        routes.append([Route(seller=next(sellers_iter), buyer=next(buyers_iter), transport_cost=cost) for cost in row])

    return SupplyChainData(sellers=sellers, buyers=buyers, routes=routes, force_fictional=force_fictional)