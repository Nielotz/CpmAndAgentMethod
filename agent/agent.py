from dataclasses import dataclass

from agent.supply_chain import SupplyChainData, RoutesTable, TransportTable, Table


@dataclass
class AgentData:
    # total_products_cost: int
    # total_transport_cost: int
    total_cost: int
    total_income: int
    total_profit: int
    buyers: [str]  # Headers in tables.
    sellers: [str]  # Headers in tables.
    profit_table: [[int, ]]
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

    @classmethod
    def solve(cls, supply_chain_data: SupplyChainData) -> [AgentData, ]:
        routes_table: RoutesTable = RoutesTable.from_flat(
            elements=supply_chain_data.routes,
            dimensions=(len(supply_chain_data.buyers),
                        len(supply_chain_data.sellers))
        )

        transport_table: TransportTable = TransportTable.create_using_north_west_method(
            supply_chain_data=supply_chain_data)

        transport_table.print(header="Transport table:")

        transport_table.init_equations(routes_table=routes_table)
        transport_table.optimality_indicators_equations.print(header="Equations")

        for loops_left in range(20, 0, -1):  # Infinite loop guard.
            optimality_indicators: [int] = transport_table.get_optimality_indicators()
            Table(table=[optimality_indicators]).print(header="Optimality indicators")

            if min(optimality_indicators) < 0:
                transport_table.shuffle_products(optimality_indicators=optimality_indicators)
                transport_table.print(header="Transport table")
            else:
                break
        else:
            raise RecursionError()
