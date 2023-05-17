from dataclasses import dataclass


@dataclass
class Trader:
    capacity: int
    price: float

@dataclass
class Route:
    seller: Trader
    buyer: Trader
    transport_cost: int

@dataclass
class SupplyChainData:
    sellers: [Trader, ]
    buyers: [Trader, ]
    routes: [Route, ]
