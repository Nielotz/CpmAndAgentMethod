from dataclasses import dataclass


@dataclass
class Trader:
    id_: str
    capacity: int
    price: float

@dataclass
class Route:
    seller: Trader
    buyers: Trader
    transport_cost: int

@dataclass
class SupplyChainData:
    sellers: [Trader, ]
    buyers: [Trader, ]
    routes: [Route, ]
