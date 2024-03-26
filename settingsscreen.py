from kivy.app import App
from kivy.metrics import dp
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.checkbox import CheckBox
from kivy.uix.label import Label
from kivymd.app import MDApp
from kivymd.uix.button import MDExtendedFabButtonIcon
from kivymd.uix.textfield import MDTextField
import json

class SettingsScreen(Screen):
    def __init__(self, **kwargs):
        super(SettingsScreen, self).__init__(**kwargs)
        app = MDApp.get_running_app()

        # Load value from settings.json file
        self.num_sets = 5
        self.timer_secs = 10

        try:
            with open("settings.json", "r") as f:
                data = json.load(f)
                self.num_sets = data.get("numOfSets", 5)
                self.timer_secs = data.get("timerSecs", 5)
        except FileNotFoundError:
            pass

        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        # Create a BoxLayout for the widgets
        box_layout = GridLayout(rows=5, cols=2, spacing=10, padding=10,size_hint_y=0.5)

        # Title Label
        label_title = Label(
            text="Advanced Settings",
            size_hint_y=None,
            height=50,
            font_size='20sp',
            bold=True,
            font_name="littledays",
            color=(1,1,1,0.4)  # Adjust the color as needed
        )
        label_num_sets = Label(text="Repetition Sets", size_hint_y=None, height=40, font_name="littledays")
        num_sets_field = MDTextField(
            hint_text="Set how many rounds of notes for a session",
            text=str(self.num_sets),
            #line_color_normal= app.theme_cls.accent_color,
            line_color_normal="#FAA0A0",
            font_name="littledays"
        )

        # Bind text change event to update JSON
        num_sets_field.bind(text=self.on_text_change_repitittion_sets)

        label_timer_secs = Label(text="Sight Reader Timer seconds", size_hint_y=None, height=40, font_name="littledays")
        label_timer_secs_field = MDTextField(
            hint_text="Enter the seconds for Sight reader timer mode. ",
            text=str(self.timer_secs),
            #line_color_normal= app.theme_cls.accent_color,
            line_color_normal="#FAA0A0",
            font_name="littledays"
        )

        # Bind text change event to update JSON
        label_timer_secs_field.bind(text=self.on_text_change_timer)


        label_show_ledger_lines = Label(text="Show Ledger Lines", size_hint_y=None, height=40, font_name="littledays")
        # Checkbox for Show Ledger Lines
        show_ledger_lines_checkbox = CheckBox(
            active=True,  # Default to checked
            size_hint_y=None,
            height=dp(40),
            disabled=True,
        )

        label_chord_mode = Label(text="Chord Mode", size_hint_y=None, height=40, font_name="littledays")
        # Checkbox for Chord Mode
        chord_mode_checkbox = CheckBox(
            active=False,  # Default to not checked
            size_hint_y=None,
            height=dp(40),
            disabled=True
        )

        # Label for Pro Version
        label_pro_version = Label(
            text="(Pro version) Add more Students",
            size_hint_y=None,
            height=dp(40),
            color=(1, 0, 0, 1),  # Bright color, you can adjust the values (R, G, B, A)
            font_name="littledays"
        )

        # Button for adding more students (initially disabled)
        button_add_students = Button(
            text="Add more Students",
            size_hint_y=None,
            height=dp(40),
            width=dp(20),
            disabled=True,
            font_name="littledays"
        )

        # Add widgets to BoxLayout
        box_layout.add_widget(label_num_sets)
        box_layout.add_widget(num_sets_field)
        box_layout.add_widget(label_timer_secs)
        box_layout.add_widget(label_timer_secs_field)
        box_layout.add_widget(label_show_ledger_lines)
        box_layout.add_widget(show_ledger_lines_checkbox)
        box_layout.add_widget(label_chord_mode)
        box_layout.add_widget(chord_mode_checkbox)
        box_layout.add_widget(label_pro_version)
        box_layout.add_widget(button_add_students)

        float_layout = FloatLayout()
        float_layout.pos_hint = {"center_x": 0.5, "center_y": 0.5}
        # Create Home button
        home_button = MDExtendedFabButtonIcon(
            icon="home",
            text='Home', halign="center",
            font_name="littledays"
        )

        home_button.pos_hint = {"x": 0.45, "y": 0.5}
        home_button.bind(on_release=self.go_to_menu)

        float_layout.add_widget(home_button)

        layout.add_widget(label_title)
        layout.add_widget(box_layout)
        layout.add_widget(float_layout)

        self.add_widget(layout)

    def on_text_change_repitittion_sets(self, instance, value):

        # Load existing JSON data from the file
        try:
            with open("settings.json", "r") as f:
                data = json.load(f)
        except FileNotFoundError:
            data = {}  # Create an empty dictionary if the file doesn't exist

        # Update the specific value
        try:
            # Update num_sets and save to settings.json
            self.num_sets = int(value)
            app = MDApp.get_running_app()
            app.g_number_of_slide = self.num_sets
            data["numOfSets"] = self.num_sets
            #print("app.g_number_of_slide" + str(app.g_number_of_slide))
            with open("settings.json", "w") as f:
                json.dump(data, f)
        except ValueError:
            pass

    def on_text_change_timer(self, instance, value):

        # Load existing JSON data from the file
        try:
            with open("settings.json", "r") as f:
                data = json.load(f)
        except FileNotFoundError:
            data = {}  # Create an empty dictionary if the file doesn't exist

        # Update the specific value
        try:
            # Update num_sets and save to settings.json
            self.timer_secs = int(value)
            app = MDApp.get_running_app()
            app.g_timer_secs = self.timer_secs
            data["timerSecs"] = self.timer_secs
            #print("app.g_number_of_slide" + str(app.g_number_of_slide))
            with open("settings.json", "w") as f:
                json.dump(data, f)
        except ValueError:
            pass


    def go_to_menu(self, instance):
        app = MDApp.get_running_app()
        self.manager.current = 'menu'
        app.change_palette(theme='Dark', prim_palette='Cyan')
