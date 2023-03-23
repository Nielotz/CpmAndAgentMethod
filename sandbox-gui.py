from kivy.app import App
from kivy.graphics import Color, Rectangle
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.layout import Layout
from kivy.uix.button import Button

import cpm.cpm as cpm
from gui.table import OutputTable


class CPSapp(App):
    def build(self):
        import cpm.test.data_loader
        from cpm.network import Network
        result_network: Network
        test_network: Network
        test_network, result_network = cpm.test.data_loader.load_data_from_file("cpm/test_data/simple_test.txt")
        # test_network, result_network = cpm.test.data_loader.load_data_from_file("cpm/test_data/test_mid_orphan.txt")
        # test_network, result_network = cpm.test.data_loader.load_data_from_file("cpm/test_data/test_two_critical_paths_that_ends_with_orphans.txt")


        result_networks: [Network, ] = test_network.solve()
        result_network = result_networks[0]

        # output_table = OutputTable(headers=("ID", "Poprzednik", "Czas trwania", "ES", "EF", "LS", "LF", "Opóżnienie"))
        output_table = OutputTable(headers=tuple(result_network.nodes_by_id.values())[0].asdict().keys())
        for id_, node in result_network.nodes_by_id.items():
            values = node.asdict().values()
            values = tuple(map(lambda val: ", ".join(val) if isinstance(val, (list, tuple)) else str(val), values))
            output_table.add_values(values)

        return output_table


CPSapp().run()

# """ Create CPM sth. """
# brrr_system = cpm.CPM()
#
# """ Load data from user (to load data from file, see cpm/test/data_loader.py). """
# # Input
# brrr_system.load_data_from_user()
#
# """ Solve network. """
# # Brrrrr
# brrr_system.solve()
#
# # Output
# brrr_system.print_result_network()
# # brrr_system.show_result_network()
