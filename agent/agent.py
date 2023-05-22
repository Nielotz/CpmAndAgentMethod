from dataclasses import dataclass

from agent.supply_chain import SupplyChainData, RoutesTable, TransportTable, Table, Route, Trader, FictionalTrader, \
    FictionalRoute


@dataclass
class AgentData:
    total_products_cost: int
    total_transport_cost: int
    total_cost: int
    total_income: int
    total_profit: int
    buyers: [Trader]  # Headers in tables.
    sellers: [Trader]  # Headers in tables.
    unit_profit_table: [[int, ]]
    optimal_transport_table: [[int, ]]


class Agent:
    """
`       BUYERS
    S [      ]
    E [      ]
    L [      ]
    L [      ]
    E [      ]
    R [      ]
    S [      ]`"""

    @staticmethod
    def convert_to_agent_data(transport_table: TransportTable,
                              buyers: [Trader],
                              sellers: [Trader],
                              routes_table: RoutesTable) -> AgentData:
        total_products_cost = 0
        total_transport_cost = 0
        total_income = 0
        for row_idx, (transport_table_row, routes_table_row) in enumerate(zip(transport_table, routes_table)):
            for col_idx, (transported_amount, route) in enumerate(zip(transport_table_row, routes_table_row)):
                transported_amount: int

                if isinstance(route, FictionalRoute):
                    products_cost = 0
                    transport_cost = 0
                    income = 0
                else:
                    route: Route
                    products_cost = route.seller.price * transported_amount
                    transport_cost = route.transport_cost * transported_amount
                    income = route.buyer.price * transported_amount

                total_products_cost += products_cost
                total_transport_cost += transport_cost
                total_income += income

        return AgentData(
            total_products_cost=total_products_cost,
            total_transport_cost=total_transport_cost,
            total_cost=total_products_cost + total_transport_cost,
            total_income=total_income,
            total_profit=total_income - (total_products_cost + total_transport_cost),
            buyers=buyers,
            sellers=sellers,
            unit_profit_table=routes_table.unit_profit_table,
            optimal_transport_table=transport_table.table
        )

    @classmethod
    def solve(cls, supply_chain_data: SupplyChainData) -> [AgentData, ]:
        buyers: [Trader, ] = supply_chain_data.buyers
        sellers: [Trader, ] = supply_chain_data.sellers
        routes: [Route] = supply_chain_data.routes

        routes_table: RoutesTable = RoutesTable.from_flat(elements=routes, dimensions=(len(sellers), len(buyers)))

        buyers_capacity = sum([cap.capacity for cap in buyers])
        sellers_capacity = sum([cap.capacity for cap in sellers])

        if supply_chain_data.force_fictional or buyers_capacity != sellers_capacity:
            fictional_seller: FictionalTrader = FictionalTrader(capacity=buyers_capacity)
            sellers.append(fictional_seller)
            routes_table.add_row(
                [FictionalRoute(seller=fictional_seller, buyer=buyer, transport_cost=0) for buyer in buyers])

            fictional_buyer: FictionalTrader = FictionalTrader(capacity=sellers_capacity)
            buyers.append(fictional_buyer)
            routes_table.add_column(
                [FictionalRoute(seller=seller, buyer=fictional_buyer, transport_cost=0) for seller in sellers])

        transport_table: TransportTable = TransportTable.create_using_north_west_method(buyers=buyers, sellers=sellers)

        transport_table.print(header="Transport table:")

        transport_table.init_equations(routes_table=routes_table)
        transport_table.optimality_indicators_equations.print(header="Equations")

        transport_tables: [TransportTable] = []

        for loops_left in range(30, 0, -1):  # Infinite loop guard.
            optimality_indicators: [int] = transport_table.get_optimality_indicators()
            Table(table=[optimality_indicators]).print(header="Optimality indicators")

            if min(optimality_indicators) < 0:
                transport_table.shuffle_products(optimality_indicators=optimality_indicators)
                transport_table.print(header="Transport table")

                if transport_table in transport_tables:
                    transport_tables = transport_tables[transport_tables.index(transport_table):]
                    break
                else:
                    transport_tables.append(TransportTable(table=transport_table.table))
            else:
                transport_tables = [transport_table]
                break
        else:
            raise RecursionError()

        return [Agent.convert_to_agent_data(transport_table=transport_table,
                                            buyers=buyers,
                                            sellers=sellers,
                                            routes_table=routes_table) for transport_table in transport_tables]
