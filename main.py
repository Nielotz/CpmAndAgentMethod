from kivy.app import App
from kivy.core.window import Window


from gui.screen_manager import MyScreenManager


class CpmAndAgentMethodSimulator (App):
    def build(self):
        Window.clearcolor = (218 / 255, 222 / 255, 206 / 255, 1.0)
        return MyScreenManager()


CpmAndAgentMethodSimulator().run()
