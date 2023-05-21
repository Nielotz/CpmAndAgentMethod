import pytest

from agent.data_loader import load_data_from_json_file

from agent.agent import AgentData, Agent
from agent.supply_chain import SupplyChainData, Trader, Route

def runner(path: str):
    supply_chain_data: SupplyChainData
    test_ad: AgentData
    supply_chain_data, test_ad = load_data_from_json_file(path=path)

    result_ad: AgentData = Agent.solve(supply_chain_data=supply_chain_data)

    assert test_ad.total_cost == result_ad.total_cost
    assert test_ad.total_income == result_ad.total_income
    assert test_ad.total_profit == result_ad.total_profit

    for t, r in zip(test_ad.profit_table, result_ad.profit_table):
        assert t == pytest.approx(r)

    for t, r in zip(test_ad.optimal_transport_table, result_ad.optimal_transport_table):
        assert t == pytest.approx(r)