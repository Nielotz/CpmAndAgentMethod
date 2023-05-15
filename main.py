from kivy.app import App
from kivy.core.window import Window

from gui.screen_manager import *
from gui.agent_out import TestAgentWidget

class CPMapp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.result_networks: [Network, ] = None

    @staticmethod
    def load_data_from_user(path: str) -> {Hashable, Node}:
        """ Load data from user.

        @return: dict{Node.id_, Node} - dict of nodes with nodes' id as a key
        """
        nodes: {Hashable, Node} = dict()
        read_data = data_input.load_data_from_file(path=path)
        for id_, prev_ids, duration in read_data[tuple(read_data.keys())[0]]:
            nodes[id_] = Node(id_, prev_ids.split(",") if prev_ids else [], float(duration))
        return nodes

    def build(self):
        Window.clearcolor = (218 / 255, 222 / 255, 206 / 255, 1.0)
        return TestAgentWidget()
        # return MyScreenManager()


CPMapp().run()
