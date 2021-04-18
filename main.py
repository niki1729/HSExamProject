from random import randint, random

from kivy.core.text import Label
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty, StringProperty
from kivy.core.window import Window

from labels import *
from utilities.calculator_eval import Eval

Window.size = (600, 700)


# For PopupWindow, probably wil be used several times
class P(FloatLayout):
    pass


class HomeScreen(Screen):
    def change_color(self):
        self.ids.welcome_label.color=randint(0,100)/100, randint(0,100)/100, randint(0,100)/100, 1


class CalculatorScreen(Screen):
    history_text = StringProperty()
    last_result = ""
    last_calc = ""
    new_calc = True
    char_processed = False

    def __init__(self, **kwargs):
        super(CalculatorScreen, self).__init__(**kwargs)
        Window.bind(on_key_down=self._on_keyboard_down)

    def print_button_text(self, char):
        self.char_processed = False

        if self.new_calc:
            state = char == "+" or char == "*" or char == "/"  # char == "-" or
            if not self.char_processed and state:
                if self.last_result != "" and self.ids.calc_inp.text == "":
                    self.ids.calc_inp.text = self.last_result + str(char)
                elif self.ids.calc_inp.text == "":
                    self.ids.calc_inp.text = "0" + self.ids.calc_inp.text + str(char)

            elif not self.char_processed and char == "." and self.ids.calc_inp.text == "":
                try:
                    int(self.last_result)
                    self.ids.calc_inp.text = self.last_result + str(char)
                except:
                    self.ids.calc_inp.text = self.last_result

            elif not self.char_processed and self.ids.calc_inp.text == "":
                self.ids.calc_inp.text = self.ids.calc_inp.text + str(char)

            self.char_processed = True

        elif not self.char_processed:
            self.ids.calc_inp.text = self.ids.calc_inp.text + str(char)
        self.new_calc = False

    def eval_function(self):
        if self.ids.calc_inp.text != "":

            try:
                eval = Eval()
                self.last_result = str(self.if_int(round(eval.evaluate(self.ids.calc_inp.text), 6)))
                self.last_calc = self.ids.calc_inp.text
                self.history_text = str(self.ids.calc_inp.text) + "=" + self.last_result
                self.ids.calc_inp.text = ""
                self.new_calc = True
            except:
                # self.last_result = self.ids.calc_inp.text
                # self.ids.calc_inp.text = "Python syntax error!"
                self.show_popup()

    def last_result_print(self):
        self.ids.calc_inp.text = self.last_calc
        self.new_calc = False

    def clear_text_input(self):
        self.ids.calc_inp.text = ""
        self.new_calc = True

    def delete_last_char(self):
        self.ids.calc_inp.text = self.ids.calc_inp.text[:-1]
        if self.ids.calc_inp.text == "":
            self.new_calc = True

    def _on_keyboard_down(self, instance, keyboard, keycode, text, modifiers):

        print(text)
        if keycode == 40:  # 40 - Enter key pressed#
            print("test")
            self.eval_function()
        return True

    def show_popup(self):
        show = P()
        popup_window = Popup(title="Python syntax error!", content=show, size_hint=(0.5, 0.3), size=(400, 100))
        # show.ids.popuplabel.text = "Python syntax error!"
        popup_window.open()

    def if_int(self, result):
        if int(result) == result:
            return int(result)
        else:
            return result


list_images = ["resources/niki.jpg", "resources/roseschloss2.jpg", "resources/tunnel.jpg"]


class DemoScreen(Screen):
    def change_image(self):
        self.ids.demo_image.source = list_images[randint(0, len(list_images) - 1)]
        self.ids.button_change_image.color=randint(0,100)/100, randint(0,100)/100, randint(0,100)/100, 1


class ContentNavigationDrawer(BoxLayout):
    screen_manager = ObjectProperty()
    nav_drawer = ObjectProperty()
    # https://kivymd.readthedocs.io/en/latest/components/navigation-drawer/
    pass


class MainApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Gray"
        self.theme_cls.primary_hue = "A700"
        self.theme_cls.theme_style = "Dark"

        self.title = TITLE
        GUI = Builder.load_file("main.kv")
        return GUI


MainApp().run()
