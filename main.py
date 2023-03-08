import cpm.cpm as cpm
from kivy.app import App
import gui.graph as graph

class CPMapp(App):
    def build(self):
        return graph.GraphWidget()

CPMapp().run()

""" Create CPM sth. """
brrr_system = cpm.CPM()

""" Load data from user (to load data from file, see cpm/test/data_loader.py). """
# Input
brrr_system.load_data_from_user()

""" Solve network. """
# Brrrrr
brrr_system.solve()

# Output
brrr_system.print_result_network()
# brrr_system.show_result_network()
