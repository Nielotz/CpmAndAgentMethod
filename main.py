import cpm.cpm as cpm
from kivy.app import App
import gui.graph as graph
import cpm.network as network
import cpm.test.data_loader as dl
from kivy.core.window import Window

class CPMapp(App):
    def build(self):
        net: tuple[network.Network, network.Network] = dl.load_data_from_file(path="cpm\\test_data\\test_two_critical_paths_that_ends_with_orphans.txt")
        nn = net[0].solve()

        gra = graph.GraphWidget()
        # gra.set_network(net[0])
        gra.draw_graph(nn[0])
        return gra

Window.clearcolor = (218/255, 222/255, 206/255, 1.0)
CPMapp().run()

# """ Create CPM sth. """
# brrr_system = cpm.CPM()

# """ Load data from user (to load data from file, see cpm/test/data_loader.py). """
# # Input
# brrr_system.load_data_from_user ()

# """ Solve network. """
# # Brrrrr
# brrr_system.solve()

# # Output
# brrr_system.print_result_network()
# # brrr_system.show_result_network()
