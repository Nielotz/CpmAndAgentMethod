from agent.test.runner import runner

def test_2x2():
    runner("agent/test_data/simple_test_2x2.json")

def test_3x3():
    runner("agent/test_data/simple_test_3x3.json")

def test_upel_2x3():
    runner("agent/test_data/test_upel_2x3.json")

def test_upel_zad0_2x2():
    runner("agent/test_data/test_upel_zad0_2x2.json")