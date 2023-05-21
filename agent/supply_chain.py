import copy
from dataclasses import dataclass
from typing import Self, Callable, Iterable

import sympy


@dataclass
class Trader:
    capacity: int
    price: int


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


class Table:
    table: [[]]

    def print(self, header: str = "", indent: int=0, next_indent: int=4):
        print(self.repr(header=header, indent=indent, next_indent=next_indent))

    def repr(self, header: str = "", indent: int=0, next_indent: int=4) -> str:
        if not self.table:
            return "[]"

        columns_length = [max([len(str(self.table[row_idx][col_idx])) for row_idx in range(len(self.table))])
                          for col_idx in range(len(self.table[0]))]

        next_indent_ = " " * next_indent
        return f"{' ' * indent}{header}" \
               f"\n{next_indent_}[ " \
            + f"\n{next_indent_}[ ".join([
                " | ".join([str(val).rjust(col_len) for (val, col_len) in zip(row, columns_length)])
                + " ]" for row in self.table
            ] )


    def __init__(self, table: [[]] = None):
        self.table = copy.deepcopy(table) or [[]]

    @classmethod
    def from_flat(cls, elements: (), dimensions: (int, int)) -> Self:
        rows, cols = dimensions

        table: [[]] = [list()] * rows
        for row_id in range(rows):
            table[row_id] = [elements[row_id * cols + x] for x in range(cols)]

        return cls(table=table)

    def __iter__(self):
        yield from self.table

    def __getitem__(self, item):
        return self.table[item]

    def __len__(self):
        return len(self.table)

class RoutesTable(Table):
    table: [[Route, ]]


class TransportTable(Table):
    optimality_indicators_equations: Table

    def init_equations(self, routes_table: RoutesTable):
        rows: int = len(routes_table.table)
        cols: int = len(routes_table.table[0])

        alfa = sympy.symbols(", ".join([f"a_{i}" for i in range(rows)]))
        beta = sympy.symbols(", ".join([f"b_{i}" for i in range(cols)]))

        equations = [[None] * cols for _ in range(rows)]
        for i in range(rows):
            for j in range(cols):
                route_ij: Route = routes_table.table[i][j]
                c: int = route_ij.transport_cost + route_ij.seller.price - route_ij.buyer.price
                equations[i][j] = (lambda i=i, j=j, c=c: alfa[i] + beta[j] + c)()

        self.optimality_indicators_equations = Table(table=equations)

    @classmethod
    def create_using_north_west_method(cls, supply_chain_data: SupplyChainData) -> Self:
        buyers_len = len(supply_chain_data.buyers)
        sellers_len = len(supply_chain_data.sellers)

        transport_table: [[]] = [[0] * buyers_len for _ in range(sellers_len)]
        buyers_caps = [buyer.capacity for buyer in supply_chain_data.buyers]
        for seller_idx, seller in enumerate(supply_chain_data.sellers):
            seller: Trader
            seller_cap: int = seller.capacity
            for buyer_cap_idx, buyer_cap in enumerate(buyers_caps):
                if buyer_cap == 0:
                    continue

                if buyer_cap < seller_cap:
                    seller_cap -= buyer_cap
                    transport_table[seller_idx][buyer_cap_idx] += buyer_cap
                    buyers_caps[buyer_cap_idx] = 0
                else:
                    buyer_cap -= seller_cap  # Sell all.
                    buyers_caps[buyer_cap_idx] = buyer_cap
                    transport_table[seller_idx][buyer_cap_idx] += seller_cap
                    break

        return cls(table=transport_table)

    def get_optimality_indicators(self) -> []:
        # Calculate coefficients α and β.
        base_equations: [] = []
        non_base_equations: [] = []

        for row_idx, row in enumerate(self.table):
            for col_idx, route_elem in enumerate(row):
                eq = self.optimality_indicators_equations[row_idx][col_idx]

                if route_elem != 0:
                    base_equations.append(eq)
                else:
                    non_base_equations.append(eq)

        unique_vars_in_base_equations: set[sympy.Symbol] = set(var for eq in base_equations for var in eq.free_symbols)
        unique_vars_in_base_equations: list[sympy.Symbol] = list(unique_vars_in_base_equations)

        # Make equations soluble.
        over_amounted_vars = len(unique_vars_in_base_equations) - len(base_equations)
        for _ in range(over_amounted_vars):
            var_to_subs = unique_vars_in_base_equations.pop()
            for eq_idx, eq in enumerate(base_equations):
                base_equations[eq_idx] = eq.subs(var_to_subs, 0)

            for eq_idx, eq in enumerate(non_base_equations):
                non_base_equations[eq_idx] = eq.subs(var_to_subs, 0)

        coefficients: dict[sympy.core.symbol.Symbol: sympy.core.numbers.Integer] = sympy.solve(base_equations)

        # Calculate non-base equations
        for var, value in coefficients.items():
            for eq_idx, eq in enumerate(non_base_equations):
                non_base_equations[eq_idx] = eq.subs(var, value)

        return non_base_equations

    def shuffle_products(self, optimality_indicators: Iterable[int, ]):
        """Shuffle products based on optimality indicators.

            Select smallest value in optimality_indicators and shuffle transport table using it.
        """
        # Get from where to start - idx of min optimality_indicators.
        start_row_idx: int = 0
        start_col_idx: int = 0
        min_oi_val: int = min(optimality_indicators)
        optimality_indicators_iter = iter(optimality_indicators)
        for row_idx, row in enumerate(self.table):
            for col_idx, elem in enumerate(row):
                if elem == 0:
                    if next(optimality_indicators_iter) == min_oi_val:
                        start_row_idx = row_idx
                        start_col_idx = col_idx

        # Find matching route points for field with minimal indicator.
        end_row_idx: int = 0
        end_col_idx: int = 0
        for row_idx, row in enumerate(self.table):
            if row_idx != start_row_idx:  # Searching square-like path.
                for col_idx, elem in enumerate(row):
                    if col_idx != start_col_idx:  # Searching square-like path.
                        route_point1_amount = self.table[start_row_idx][col_idx]
                        route_point2_amount = self.table[row_idx][start_col_idx]
                        # route_point3_amount = self.table[row_idx][col_idx]
                        if 0 not in [route_point1_amount, route_point2_amount]:
                            end_row_idx = row_idx
                            end_col_idx = col_idx
                            break

        # Transfer products.
        transferable_amount = min(self.table[start_row_idx][end_col_idx],
                                  self.table[end_row_idx][start_col_idx])

        self.table[start_row_idx][start_col_idx] += transferable_amount  # route point: 0
        self.table[start_row_idx][end_col_idx] -= transferable_amount  # route point: 1
        self.table[end_row_idx][start_col_idx] -= transferable_amount  # route point: 2
        self.table[end_row_idx][end_col_idx] += transferable_amount  # route point: 3









