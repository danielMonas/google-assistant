""" UI for the entire project, using Kivy """

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
import kivy
kivy.require('1.10.1')


class ConfigList(BoxLayout):
    """ Configurations main screen """
    def __init__(self, **kwargs):
        super(ConfigList, self).__init__(**kwargs)
        self.add_widget(Label(text='Tag As: [Tag0]'))
        self.add_widget(TextInput(text='queries'))
        self.add_widget(TextInput(text='untag queries')) #TODO - add option in future version.

class Buttons(BoxLayout):
    """ Main buttons """
    def __init__(self, **kwargs):
        super(Buttons, self).__init__(**kwargs)
        self.add_widget(Button(text='Run', size_hint=(0.3, 0.3)))
        self.add_widget(Button(text='Next Setting', size_hint=(0.4, 0.3)))

class MainLayout(BoxLayout):
    """ Main layout wrapper """
    def __init__(self, **kwargs):
        super(MainLayout, self).__init__(**kwargs)
        self.add_widget(ConfigList())
        self.add_widget(Buttons())

class Interface(App):
    """ Main GUI class """
    def build(self):
        """ Building the GUI """
        return MainLayout(spacing=10, orientation='vertical')

def main():
    """ Main function. """
    Interface().run()
if __name__ == '__main__':
    main()
