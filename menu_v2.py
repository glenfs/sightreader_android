
from kivy.app import App
from kivy.core.audio import SoundLoader
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView

from kivymd.uix.segmentedcontrol import MDSegmentedControl, MDSegmentedControlItem

from keyboard import KeyBoardLayoutMenu


class SightReaderMenu(ScrollView):

    def on_difficulty_press(self, instance_segcontrol, instance_segment):
        selected_value = instance_segment.text
        # print(selected_value)
        App.get_running_app().update_difficulty(selected_value)
        self.interface_click.play()

        if selected_value == 'Beginner':
            if App.get_running_app().get_clef() == 'Bass':
                self.keyboard.toggle_state_down([[10, 17]])
            elif App.get_running_app().get_clef() == 'treble':
                self.keyboard.toggle_state_down([[12, 19]])
            else:
                self.keyboard.toggle_state_down([[10, 19]])
        elif selected_value == 'Intermediate':
            if App.get_running_app().get_clef() == 'Bass':
                self.keyboard.toggle_state_down([[5, 12]])
            elif App.get_running_app().get_clef() == 'Treble':
                self.keyboard.toggle_state_down([[15, 24]])
            else:
                self.keyboard.toggle_state_down([[5, 12],[15,24]])
        else:
            if App.get_running_app().get_clef() == 'Bass':
                self.keyboard.toggle_state_down([[0, 8]])
            elif App.get_running_app().get_clef() == 'Treble':
                self.keyboard.toggle_state_down([[21, 29]])
            else:
                self.keyboard.toggle_state_down([[0, 8],[21, 29]])

    def on_clef_press(self, instance_segcontrol, instance_segment):
        selected_value = instance_segment.text
        # print(f"Selected Value: {selected_value}")
        App.get_running_app().update_clef(selected_value)
        self.interface_click.play()

        if selected_value == 'Bass':
            if App.get_running_app().get_difficulty() == 'Beginner':
                self.keyboard.toggle_state_down([[10, 17]])
            elif App.get_running_app().get_difficulty() == 'Intermediate':
                self.keyboard.toggle_state_down([[5, 12]])
            else:
                self.keyboard.toggle_state_down([[0, 8]])
        elif selected_value == 'Treble':
            if App.get_running_app().get_difficulty() == 'Beginner':
                self.keyboard.toggle_state_down([[12, 19]])
            elif App.get_running_app().get_difficulty() == 'Intermediate':
                self.keyboard.toggle_state_down([[15, 24]])
            else:
                self.keyboard.toggle_state_down([[21, 29]])
        else:
            if App.get_running_app().get_difficulty() == 'Beginner':
                self.keyboard.toggle_state_down([[10, 19]])
            elif App.get_running_app().get_difficulty() == 'Intermediate':
                self.keyboard.toggle_state_down([[5, 12],[15,24]])
            else:
                self.keyboard.toggle_state_down([[0, 8],[21, 29]])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = GridLayout(cols=1, spacing=dp(50), size_hint_y=None)
        # Make sure the height is such that there is something to scroll.
        layout.bind(minimum_height=layout.setter('height'))

        # Create the top app bar
        #top_app_bar = MDTopAppBar(title="[font=fonts/Roboto-Thin.ttf][size=32]Sight Reader Expert", size_hint_y=None, height=dp(35))
        top_app_bar = Label(text='Sight Reader Expert',  font_name="littledays", font_size='36sp', bold=True, color='66ffff',size_hint_y=None, height=dp(25))
        layout.add_widget(top_app_bar)
        #l = Label(text='', font_size='24sp', bold=True, color=(1, 0, 0, 1), size_hint_y=None,
              #height=dp(35))
        #layout.add_widget(l)
        layout_segments = GridLayout(rows=2, cols=1, padding=dp(25), spacing=dp(25), size_hint_y=None, height=dp(50),
                                     )
        # Create and add the second segmented control for Beginner, Intermediate, Advanced
        difficulty_segment = MDSegmentedControl(
            MDSegmentedControlItem(text="Beginner", font_name="littledays"),
            MDSegmentedControlItem(text="Intermediate", font_name="littledays"),
            MDSegmentedControlItem(text="Advanced", font_name="littledays"),
            size_hint_y=None,
            height = dp(25)
        )
        layout_segments.add_widget(difficulty_segment)
        # Bind the on_press event to the callback function
        difficulty_segment.bind(on_active=self.on_difficulty_press)

        # Create and add the first segmented control for Treble, Bass, Both
        clef_segment = MDSegmentedControl(
            MDSegmentedControlItem(text="Treble", font_name="littledays"),
            MDSegmentedControlItem(text="Bass", font_name="littledays"),
            MDSegmentedControlItem(text="Both", font_name="littledays"),
            size_hint_y=None,
            height=dp(25)
        )
        layout_segments.add_widget(clef_segment)
        layout_segments.height = dp(50)
        layout.add_widget(layout_segments)
        # Bind the on_press event to the callback function
        clef_segment.bind(on_active=self.on_clef_press)

        # Create a RelativeLayout for buttons
        # layout_buttons = RelativeLayout(size_hint_y=None)

        # Create Advanced options button

        layout_buttons = GridLayout(rows=1, cols=1, padding=dp(25), spacing=dp(25), size_hint_y=None, height=dp(40))

        # layout_opt_buttons.add_widget(options_button)
        # layout_buttons.add_widget(options_button)

        l = Label(text="")
        layout_buttons.add_widget(l)
        layout.add_widget(layout_buttons)

        self.keyboard = KeyBoardLayoutMenu()

        self.keyboard.size_hint_y = None  # 40% height
        self.keyboard.height = 250
        self.keyboard.size_hint_x = 1
        layout.add_widget(self.keyboard)

        company_label = Label(text="\u00a9 Adagio Labs India, 2024",   font_size='12sp', bold=False, color='white',size_hint_y=None, height=dp(15))
        layout.add_widget(company_label)
        # for i in range(100):
        # btn = Button(text=str(i), size_hint_y=None, height=dp(40))
        # layout.add_widget(btn)

        # Create the main screen and add the layout to it
        # screen = MDScreen()
        # screen.add_widget(layout)
        # screen.add_widget(layout_buttons)
        # screen.add_widget(layout_opt_buttons)
        # screen.add_widget(keyboard)

        self.size_hint = (1, None)
        print("Window.width="+str(Window.width))
        self.size = (Window.width, Window.height)
        self.add_widget(layout)
        # root = ScrollView(size_hint=(1, None), size=(Window.width, Window.height))
        # root.add_widget(layout)

        # #print(root.children[0])
        # #print(root.children[0].children[0])
        # #print(root.children[0].children[0].children[-1].children[14])
        # target_button = root.children[0].children[0].children[-1].children[-1]
        # Scroll to the target button
        # root.scroll_to(target_button, padding=10, animate=True)

        # return root

        # Load Sounds
        self.interface_click = SoundLoader.load('sounds/interface_click.wav')


