from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.togglebutton import ToggleButton
from kivymd.app import MDApp


class KeyBoardLayoutMenu(ScrollView):
    keys_selected_treble = {}

    def toggle_state_down(self, range_list):
        app = MDApp.get_running_app()

        for i, toggle_button in enumerate(self.toggle_buttons):
            toggle_button.state = 'normal'
            app.notes_selection_menu[i] = False

            # Set toggle buttons in specified ranges to 'down' state
            for range_item in range_list:
                print("range_item="+str(range_item))
                start_index, end_index = range_item
                for i in range(start_index, end_index):
                    self.toggle_buttons[i].state = 'down'
                    app.notes_selection_menu[i] = True


    def update_state(self, j):
        #print("Called update state")
        #print("J=" + str(j))
        # Iterate through toggle buttons and update their state
        app = MDApp.get_running_app()

        for i, toggle_button in enumerate(self.toggle_buttons):
            toggle_button.state = 'down' if i <= j else 'normal'
            app.notes_selection_menu[i] = toggle_button.state == 'down'


    def on_toggle_button_click(self, instance, idx):
        #print("ToggleButton Clicked")
        app = MDApp.get_running_app()
        app.notes_selection_menu[idx] = instance.state == 'down'
        #print(app.notes_selection_menu)

        # self.state_list[idx] = instance.state == 'down'  # Update the state_list

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = MDApp.get_running_app()
        # Create a list to store toggle buttons

        window_width = Window.width

        window_height = Window.height
        # calculate keys width-- 75 below is the key width which you can tweak.
        white_key_width_800x600 = 50
        white_key_width = (
                                  window_width * white_key_width_800x600) / 800  # because for 800 with the right width was 100, so we calculate for others.
        current_pos_increse_val = (window_width * 2) / 800

        # Calculate the total height needed for the layout
        total_width = 0
        for i in range(0, 29):
            btn = Button(text=str(i), size_hint_x=None)
            total_width += white_key_width + current_pos_increse_val  # 10 is the spacing

        # Create a widget to hold the buttons
        button_holder = RelativeLayout(size_hint_x=None, width=total_width)

        # Position the buttons in the button_holder RelativeLayout
        current_width = 0
        pos_increment_steps = .9  # Earlier value was .12 when there were only 8 white keys.

        self.toggle_buttons = []
        self.size_hint_x = None

        notes_list = ['C', 'D', 'E', 'F', 'G', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'A', 'B', 'C', 'D', 'E',
                      'F', 'G', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'A', 'B', 'C']
        current_width = 0

        # White Keys
        for i in range(0, 29):
            btn = ToggleButton(size_hint_x=None,
                               background_normal='images/white_key_2.png', group=i, state='normal')
            btn.width = white_key_width
            btn.pos = (current_width, 50)
            btn.size_hint_y = 1
            # #print(btn.pos)

            if i == 14:
                btn.text = "C4"
                btn.background_normal = ''
                btn.background_color = (0.77, 0.87, 0.87, 1)

            btn.bind(on_release=lambda instance, idx=i: self.on_toggle_button_click(instance, idx))
            btn.val = [notes_list[i]]
            btn.id = i


            if i > 13 and i < 19:  # as initial state beginer and both.
                btn.state = 'down'

            self.toggle_buttons.append(btn)
            button_holder.add_widget(btn)
            current_width += btn.width + current_pos_increse_val  # 10 is the spacing

        # black_notes_list = ['C#|Db', 'D#|Eb', '', 'F#|Gb', 'G#|Ab', 'A#|Bb', '', '', 'C#|Db', 'D#|Eb', '', 'F#|Gb',
        #                     'G#|Ab', 'A#|Bb', '', '', 'C#|Db', 'D#|Eb', '']
        # first_black_key_pos = .045  # Earlier value was .07 when there were only 8 white keys.
        # black_val_size_hint_x = .045  # Earlier value was .07 when there were only 8 white keys.
        # black_val_size_hint_y = .6

        black_notes_list = ['F#|Gb', 'G#|Ab', 'A#|Bb', '', '', 'C#|Db', 'D#|Eb', '', 'F#|Gb', 'G#|Ab', 'A#|Bb', '', '',
                            'C#|Db', 'D#|Eb', '']
        first_black_key_pos = .055  # Earlier value was .07 when there were only 8 white keys.
        black_val_size_hint_x = .055  # Earlier value was .07 when there were only 8 white keys.
        black_val_size_hint_y = .6
        two_black = True
        skip_a_note = False
        black_notes_count = 0

        black_notes_list = ['F#|Gb', 'G#|Ab', 'A#|Bb', '', '', 'C#|Db', 'D#|Eb', '', 'F#|Gb', 'G#|Ab', 'A#|Bb', '', '',
                            'C#|Db', 'D#|Eb', '']
        first_black_key_pos = (window_width * 35) / 800
        black_val_size_hint_y = 0.45
        black_key_width = white_key_width * 0.70
        for i in range(0, 29):
            if not skip_a_note:
                key_pos = first_black_key_pos + (i * (
                        white_key_width + current_pos_increse_val))  # current_pos_increse_val we are adding this when creating the white keys so adding its value here too.
                #print("key_pos=" + str(key_pos))
                if two_black:
                    black_notes_count = black_notes_count + 1
                    btn = Button(size_hint_x=None,
                                 background_normal='images/black-key.jpg')

                    # btn.pos = (current_width + (current_width * 0.25), 50)
                    btn.pos_hint = {"top": 1}
                    btn.x = key_pos
                    btn.size_hint_y = black_val_size_hint_y
                    # btn.size_hint_x = black_val_size_hint_x
                    btn.width = black_key_width
                    #print("Black Button width =" + str(btn.width))
                    button_holder.add_widget(btn)
                    # current_width += btn.width + current_pos_increse_val  # 10 is the spacing
                    if black_notes_count >= 2:
                        two_black = False
                        skip_a_note = True
                        black_notes_count = 0
                else:
                    black_notes_count = black_notes_count + 1
                    btn = Button(size_hint_x=None,
                                 background_normal='images/black-key.jpg')
                    # btn.width = black_key_width
                    # btn.pos = (current_width + (current_width * 0.25), 50)
                    btn.pos_hint = {"top": 1}
                    btn.x = key_pos
                    btn.size_hint_y = black_val_size_hint_y
                    # btn.size_hint_x = black_val_size_hint_x
                    btn.width = black_key_width
                    button_holder.add_widget(btn)
                    # current_width += btn.width + 2  # 10 is the spacing
                    if black_notes_count >= 3:
                        two_black = True
                        skip_a_note = True
                        black_notes_count = 0
            else:
                skip_a_note = False

        # Create a ScrollView and add the button_holder to it
        self.size_hint = (None, 0.5)
        self.size = (Window.width, Window.height)
        self.add_widget(button_holder)
        self.scroll_x = 0.5
