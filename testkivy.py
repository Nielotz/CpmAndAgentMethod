from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button

class PongGame(Widget):
    pass


class PongApp(App):
    def build(self):
        parent = Widget()
        self.pong = PongGame()
        testBtn = Button(text='Test')
        testBtn.bind(on_relase)
        parent.add_widget(self.pong)
        parent.add_widget(testBtn)
        return parent

 
PongApp().run()