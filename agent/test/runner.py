import pytest

from agent.data_loader import load_data_from_json_file

from agent.agent import AgentData, Agent
from agent.supply_chain import SupplyChainData, Trader, Route

def runner(path: str):
    supply_chain_data: SupplyChainData
    test_ad: AgentData
    supply_chain_data, test_ad = load_data_from_json_file(path=path)
    results_ad: [AgentData] = Agent.solve(supply_chain_data=supply_chain_data)
    result_ad = results_ad[0]

    assert result_ad.total_transport_cost == test_ad.total_transport_cost
    assert result_ad.total_products_cost == test_ad.total_products_cost
    assert result_ad.total_income == test_ad.total_income
    assert result_ad.total_cost == test_ad.total_cost
    assert result_ad.total_profit == test_ad.total_profit
    assert result_ad.unit_profit_table == test_ad.unit_profit_table
    assert result_ad.optimal_transport_table == test_ad.optimal_transport_table