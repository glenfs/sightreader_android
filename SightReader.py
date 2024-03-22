import random

from kivy.app import App
from kivy.core.image import Image as CoreImage
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from kivy.graphics import Rectangle, Line, Color

from kivy.properties import DictProperty, NumericProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.widget import Widget
from kivymd.app import MDApp
from kivymd.uix.behaviors import MagicBehavior
from kivymd.uix.button import MDFillRoundFlatButton

from SightReaderQuizSet import SightReaderQuizSet
from animations.Button_animation import AnimationHelper
from note import Note
from kivymd.uix.snackbar import Snackbar


class Keyboard(BoxLayout):
    NUM_OF_WHITE_KEYS = 15

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # self.size_hint_max = (None, 300)
        self.line = None
        self.size_hint_min = (None, 200)
        # self.create_button()  # call the new method to add a button

    def on_size(self, *args):
        self.line = None
        # self.canvas.before.add(Color(0.6, 0, 0, 1))
        # self.line = self.canvas.before.add(Line(width=2, points=[self.x+13, self.top-18, self.right-42, self.top-18]))


class MusicStaff(Widget):
    difficulty = None
    clef = None
    NUMBER_OF_SETS = 2  # this value is set in the main program. Initialized here in the constructor. 2 is default value.
    NUMBER_OF_NOTES = 3

    wrong_answer_in_set = 0

    pos_hint = DictProperty({'x': 0, 'y': 0})
    start_x = NumericProperty(0)
    start_y = NumericProperty(0)
    length_staff = NumericProperty(0)
    line_1 = None
    line_2 = None
    line_3 = None
    line_4 = None
    line_5 = None
    note_size_x = NumericProperty(0)
    note_size_y = NumericProperty(0)
    note_size = None
    note_1 = None
    treble_clef_sign = None
    note_value = None
    x_start = NumericProperty(0)
    x_end = NumericProperty(0)

    y_F4 = NumericProperty(0)
    y_D4 = NumericProperty(0)
    y_E4 = NumericProperty(0)  # Give E4 note.
    y_G4 = NumericProperty(0)  # Give G4 note.
    y_A5 = NumericProperty(0)
    y_B5 = NumericProperty(0)
    y_C5 = NumericProperty(0)
    y_D5 = NumericProperty(0)
    y_E5 = NumericProperty(0)
    y_F5 = NumericProperty(0)
    y_G5 = NumericProperty(0)
    y_C4 = NumericProperty(0)
    y_B4 = NumericProperty(0)
    y_A4 = NumericProperty(0)
    y_G3 = NumericProperty(0)
    y_F3 = NumericProperty(0)
    y_A6 = NumericProperty(0)
    y_B6 = NumericProperty(0)
    y_C6 = NumericProperty(0)
    y_D6 = NumericProperty(0)
    y_E6 = NumericProperty(0)

    notes_selection_menu_Treble = []
    number_of_notes = 0
    number_of_sets_completed = 0
    correct_answer_in_set = 0

    notes = []
    current_note_index = NumericProperty(0)
    distance_between_lines = 0
    # notes_dict = {0: 'F', 1: 'A', 2: 'C', 3: 'E', 4: 'G', 5: 'D', 6: 'E', 7: 'G', 8: 'B', 9: 'D', 10: 'F', 11: 'C4',
    # 12: 'B', 13: 'A', 14: 'G', 15: 'F', 16: 'A', 17: 'B', 18: 'C', 19: 'D', 20: 'E'}
    notes_dict = {0: 'C2', 1: 'D2', 2: 'E2', 3: 'F2', 4: 'G2', 5: 'A3', 6: 'B3', 7: 'C3', 8: 'D3', 9: 'E3', 10: 'F3',
                  11: 'G3',
                  12: 'A4', 13: 'B4', 14: 'C4', 15: 'D4', 16: 'E4', 17: 'F4', 18: 'G4', 19: 'A5', 20: 'B5', 21: 'C5',
                  22: 'D5',
                  23: 'E5', 24: 'F5', 25: 'G5', 26: 'A6', 27: 'B6', 28: 'C6'}
    notes_mapping_to_dict = {}
    staff_notes_mapper = {'F4': 0, 'A5': 1, 'C5': 2, 'E5': 3, 'G5': 4, 'D4': 5, 'E4': 6, 'G4': 7, 'B5': 8, 'D5': 9,
                          'F5': 10, 'C4': 11, 'B4': 12, 'A4': 13, 'G3': 14, 'F3': 15, 'A6': 16,
                          'B6': 17, 'C6': 18, 'D6': 19, 'E6': 20}

    notes_index = []
    notes_attempted = {}
    quiz_set = None
    reset_staff_event = None

    def __init__(self, **kwargs):
        super(MusicStaff, self).__init__(**kwargs)
        # #print("On size  W:" + str(self.width) + " H:" + str(self.height))
        # Set the widget's position using pos_hint
        # #print(self.pos)
        # #print(self.size)
        app = MDApp.get_running_app()
        self.NUMBER_OF_SETS = app.g_number_of_slide
        #print("app.g_number_of_slide-Sight Reader" + str(self.NUMBER_OF_SETS))
        self.speech_play = 0
        self.notes_selection_menu = None
        self.notes_selection_menu_treble = None
        self.attempted_answer = 0
        self.correct_answer = 0

        self.label_1 = None
        self.note_1_pos_x = NumericProperty(0)
        self.note_1_rect = None
        self.notes = [None] * self.NUMBER_OF_NOTES

        self.current_note_index = 0
        self.create_staff_lines()

        self.difficulty = App.get_running_app().difficulty_selected
        self.clef = App.get_running_app().clef_selected
        # #print("app.notes_selection_menu_Treble=====")
        # #print(app.notes_selection_menu_Treble)
        self.notes_attempted = {}

        self.correct_answer_sound_1 = SoundLoader.load('sounds/correct_1.mp3')
        self.correct_answer_sound_1.volume = 0.15
        self.correct_answer_sound_2 = SoundLoader.load('sounds/correct_2.mp3')
        self.correct_answer_sound_2.volume = 0.15

        self.wrong_answer_sound = SoundLoader.load('sounds/error.mp3')
        self.wrong_answer_sound.volume = 0.15
        self.next_set_notes_sound = SoundLoader.load('sounds/next_set.mp3')
        self.next_set_notes_sound.volume = 0.15

        # self.correct_1 = SoundLoader.load('sounds/Excellent.mp3')
        # self.correct_1.volume = 0.2
        # self.correct_2 = SoundLoader.load('sounds/Impressive.mp3')
        # self.correct_2.volume = 0.2
        # self.correct_3 = SoundLoader.load('sounds/Fantastic.mp3')
        # self.correct_3.volume = 0.2
        # self.correct_4 = SoundLoader.load('sounds/Incredible.mp3')
        # self.correct_4.volume = 0.2
        # self.correct_5 = SoundLoader.load('sounds/Awesome.mp3')
        # self.correct_5.volume = 0.2
        # self.correct_6 = SoundLoader.load('sounds/Bravo.mp3')
        # self.correct_6.volume = 0.2
        # self.wrong_1 = SoundLoader.load('sounds/Nice_try.mp3')
        # self.wrong_1.volume = 0.2
        # self.wrong_2 = SoundLoader.load('sounds/Not_RightAns.mp3')
        # self.wrong_2.volume = 0.2
        # self.wrong_3 = SoundLoader.load('sounds/oops_not_right_2.mp3')
        # self.wrong_3.volume = 0.2
        # self.wrong_4 = SoundLoader.load('sounds/No_worries.mp3')
        # self.wrong_4.volume = 0.2
        # self.wrong_5 = SoundLoader.load('sounds/Little_more_practice.mp3')
        # self.wrong_5.volume = 0.2
        # self.wrong_6 = SoundLoader.load('sounds/Keep_trying.mp3')
        # self.wrong_6.volume = 0.2

        self.number_of_sets_completed = 0
        self.b_end_game = False
        self.quiz_sets = []  # Creating a list of SightReaderQuizSet instances.Used in the end game screen to show the questions and response asked in the session.
        self.reset_staff_event = None
        self.snackbar = None
        self.correct_note_tex = CoreImage('images/green_tex.png')
        self.wrong_note_tex = CoreImage('images/red_tex.png')

    def cancel_reset_staff_event(self):
        if self.reset_staff_event is not None:
            Clock.unschedule(self.reset_staff_event)

    def reset_staff(self):
        self.attempted_answer = 0
        self.correct_answer = 0
        self.label_1 = None
        self.note_1_pos_x = NumericProperty(0)
        self.note_1_rect = None
        self.notes = [None] * self.NUMBER_OF_NOTES
        self.current_note_index = 0
        self.create_staff_lines()
        self.quiz_set = SightReaderQuizSet()

    def update_rect(self, *args):
        # Update the position and size of the rectangle
        # #print(self.pos)
        # #print(self.size)
        self.rect.pos = self.pos
        self.rect.size = self.size

    def on_parent(self, widget, parent):
        pass
        #print("On parent size  W:" + str(self.width) + " H:" + str(self.height))

    def on_size(self, *args):
        # #print("On on_size size  W:" + str(self.width) + " H:" + str(self.height))
        # placing the logic here as we need to set the notes selected once after the selection is made, so cannot do in __init method.
        self.notes_selection_for_sight_reader()
        self.init_constant_values()
        self.update_staff_lines()

    def notes_selection_for_sight_reader(self):
        number_of_notes = 0
        app = App.get_running_app()
        self.notes_selection_menu_treble = app.notes_selection_menu_Treble
        self.notes_selection_menu = app.notes_selection_menu
        #print("app.notes_selection_menu=" + str(app.notes_selection_menu))
        true_count = self.notes_selection_menu.count(True)
        self.notes_index = [None] * true_count

        for index, item in enumerate(self.notes_selection_menu):
            if item:  # if True
                self.notes_index[number_of_notes] = index
                self.notes_mapping_to_dict[index] = self.notes_dict[index]
                number_of_notes = number_of_notes + 1

        #print(self.notes_mapping_to_dict)
            #print("number_of_notes=" + str(number_of_notes))

    def create_staff_lines(self):
        line_width = 1.0
        stem_line_width = 1.2

        with self.canvas:
            Color(0, 0, 0, 0.6)  # Black color
            self.line_1 = Line(points=[0, 100, 2, 100], width=line_width)
            self.line_2 = Line(points=[0, 100, 2, 100], width=line_width)
            self.line_3 = Line(points=[0, 100, 2, 100], width=line_width)
            self.line_4 = Line(points=[0, 100, 2, 100], width=line_width)
            self.line_5 = Line(points=[0, 100, 2, 100], width=line_width)
            self.treble_clef_sign = Rectangle(source='', pos=(self.start_x - 50, self.start_y - 20), size=(106, 106))

            self.note_size = (0, 0)

            # self.note_1 = Note(pos=(0, 0), size=self.note_size)
            Color(1, 1, 1, 1)  # Set color to white for texture
            for i in range(self.NUMBER_OF_NOTES):
                # Color(0.8, 0.6, 0,0.8)  # Set color to red
                self.notes[i] = Note(pos=(0, 0), size=self.note_size)

    def init_constant_values(self):
        self.pos = [self.pos[0], self.parent.size[1] / 2]
        # #print("pos=" + str(self.pos[0]) + " " + str(self.pos[1]))
        w = self.width
        # 87.5 was calculated by trial and error by having a screen width of 800 and 700 being the max width appeared almost right.  800-100 = 700, so percentage to minus is 87.5%
        max_width_staff_lines = ((w * 80) / 100)
        min_width_staff_lines = ((w * 42) / 100)

        # #print("min_width_staff_lines--" + str(min_width_staff_lines))
        # #print("max_width_staff_lines--" + str(max_width_staff_lines))
        w = max_width_staff_lines if w >= max_width_staff_lines else min_width_staff_lines if w <= min_width_staff_lines else w
        # self.x_end = int(w * .7)
        # self.x_end = int(w * .85)
        self.x_end = int(w * 1.1)
        # self.x_start = int(w * .25)
        # self.x_start = int(w * .4)
        self.x_start = int(w * .1)  # making the staff start from the x most cooardinates

        h = self.height
        max_height_staff_lines = ((h * 72.5) / 100)
        min_height_staff_lines = ((h * 49.16) / 100)
        h = max_height_staff_lines if h >= max_height_staff_lines else min_height_staff_lines if h <= min_height_staff_lines else h
        center_y = int(h * .5)
        # #print("center_y=" + str(center_y))
        # self.distance_between_lines = int(h * 0.07)
        # self.distance_between_lines = int(h * 0.1)
        self.distance_between_lines = int(h * 0.12)
        # #print("update center_y=" + str(center_y))
        # y1 = dp(self.pos[1]) + dp(75)

        # .4 is 40 % , putting the first line 40% from the bottom canvas. if we put first line exactly at 50% or half
        # of box height the staff looks positioned not centered.

        self.y_F4 = self.pos[1] + self.pos[1] * .4
        self.y_D4 = self.y_F4 - self.distance_between_lines  # Gives D4 note.
        self.y_E4 = self.y_D4 + (self.distance_between_lines / 2)  # Give E4 note.
        self.y_G4 = self.y_F4 + (self.distance_between_lines / 2)  # Give E4 note.
        self.y_A5 = self.y_F4 + self.distance_between_lines
        self.y_B5 = self.y_A5 + (self.distance_between_lines / 2)  # Give B5 note.
        self.y_C5 = self.y_A5 + self.distance_between_lines
        self.y_D5 = self.y_C5 + (self.distance_between_lines / 2)  # Give B5 note.
        self.y_E5 = self.y_C5 + self.distance_between_lines
        self.y_F5 = self.y_E5 + (self.distance_between_lines / 2)  # Give B5 note.
        self.y_G5 = self.y_E5 + self.distance_between_lines
        self.y_C4 = self.y_D4 - (self.distance_between_lines / 2)
        self.y_B4 = self.y_D4 - self.distance_between_lines
        self.y_A4 = self.y_B4 - (self.distance_between_lines / 2)

        self.y_G3 = self.y_B4 - self.distance_between_lines
        self.y_F3 = self.y_G3 - (self.distance_between_lines / 2)
        self.y_A6 = self.y_G5 + (self.distance_between_lines / 2)
        self.y_B6 = self.y_G5 + self.distance_between_lines
        self.y_C6 = self.y_B6 + (self.distance_between_lines / 2)
        self.y_D6 = self.y_B6 + self.distance_between_lines
        self.y_E6 = self.y_D6 + (self.distance_between_lines / 2)

        #print("self.x_start=" + str(self.x_start))
        #print("self.y_F4=" + str(self.y_F4))
        #print("self.x_end=" + str(self.x_end))
        #print("width=" + str(self.width))

        self.line_1.points = [self.x_start, self.y_F4, self.x_end, self.y_F4]
        self.line_2.points = [self.x_start, self.y_A5, self.x_end, self.y_A5]
        self.line_3.points = [self.x_start, self.y_C5, self.x_end, self.y_C5]
        self.line_4.points = [self.x_start, self.y_E5, self.x_end, self.y_E5]
        self.line_5.points = [self.x_start, self.y_G5, self.x_end, self.y_G5]

        # self.note_size = (w * .045, h * .07) # original values
        # self.note_size = (w * .065, h * .09)
        self.note_size = (w * .085, h * .13)

    def update_staff_lines(self):

        if not self.b_end_game:
            self.attempted_answer = 0
            self.correct_answer = 0

            ledger_required = 0
            y_val = 0
            ledger_pos = 0

            # I need to parameterize 20, notes_dict,  random.randint(0, 20) 20 should be parameterized.
            self.clef = App.get_running_app().clef_selected
            # print("Clef=" + str(self.clef))
            if self.clef == 'Both':
                self.clef = random.choice(['Treble', 'Bass'])

            add_note_list = [None] * self.NUMBER_OF_NOTES

            # If no notes were selected in the menu, we default to first 10 notes.
            if len(self.notes_index) == 0:
                self.notes_index = [10, 11, 12, 13, 14, 15, 16, 17, 18]

            # Clef is Bass
            if self.clef == 'Bass':
                # filtered_list = [value for value in self.notes_index if value <= 16]
                # Generate a random number between 0 and 1
                selector = random.randint(0, 1)
                if selector == 0 and len([value for value in self.notes_index if 8 <= value <= 16]) >= 3:
                    filtered_list = [value for value in self.notes_index if 8 <= value <= 16]
                elif selector == 1 and len([value for value in self.notes_index if 0 <= value < 8]) >= 3:
                    filtered_list = [value for value in self.notes_index if 0 <= value < 8]
                else:
                    filtered_list = [value for value in self.notes_index if value <= 16]

            # Clef is Treble
            elif self.clef == 'Treble':
                # Generate a random number between 0 and 1
                selector = random.randint(0, 1)
                if selector == 0 and len([value for value in self.notes_index if value >= 10 and value < 21]) >= 3:
                    filtered_list = [value for value in self.notes_index if value >= 10 and value < 21]
                elif selector == 1 and len([value for value in self.notes_index if value >= 21]) >= 3:
                    filtered_list = [value for value in self.notes_index if value >= 21]
                else:
                    filtered_list = [value for value in self.notes_index if value >= 10]

            for i in range(0, self.NUMBER_OF_NOTES):
                ledger_required = 0
                # print("==================================")
                # print(self.notes_index)

                # print("filtered_list")
                # print(self.notes_index)
                #print(filtered_list)
                random_number = random.choice(filtered_list)
                #print(random_number)
                #print(self.notes_mapping_to_dict[random_number])
                generated_note = self.notes_mapping_to_dict[random_number]

                if i == 0:
                    add_note_list.append(generated_note)

                actual_note = self.notes_mapping_to_dict[random_number]
                generated_note = generated_note[0]  # doing this because the data we get is like C4, D4, B5 etc.

                if self.clef == "Bass":
                    if random_number <= 16:  # we have notes only till 0-28 so stopping at 16.
                        random_number = random_number + 12

                if random_number == 0:
                    pass
                elif random_number == 1:
                    pass
                elif random_number == 2:
                    pass
                elif random_number == 3:
                    pass
                elif random_number == 4:
                    pass
                elif random_number == 5:
                    pass
                elif random_number == 6:
                    pass
                elif random_number == 7:
                    pass
                elif random_number == 8:
                    pass
                elif random_number == 9:
                    y_val = self.y_A5  # A5
                    self.notes[i].note_staff_line_nbr = 3

                elif random_number == 10:
                    y_val = self.y_F3  # requires ledger.
                    self.notes[i].note_staff_line_nbr = 0
                    ledger_required = 3
                    ledger_pos = -1
                elif random_number == 11:
                    y_val = self.y_G3  # requires ledger.
                    self.notes[i].note_staff_line_nbr = 0
                    ledger_required = 2
                    ledger_pos = -1
                elif random_number == 12:
                    y_val = self.y_A4  # requires ledger.
                    self.notes[i].note_staff_line_nbr = 0
                    ledger_required = 2
                    ledger_pos = -1

                elif random_number == 13:
                    y_val = self.y_B4  # requires ledger.
                    self.notes[i].note_staff_line_nbr = 0
                    ledger_required = 1
                    ledger_pos = -1

                elif random_number == 14:

                    y_val = self.y_C4  # requires ledger.
                    self.notes[i].note_staff_line_nbr = 0
                    ledger_required = 1
                    ledger_pos = -1

                elif random_number == 15:
                    y_val = self.y_D4
                    self.notes[i].note_staff_line_nbr = 0

                elif random_number == 16:
                    y_val = self.y_E4
                    self.notes[i].note_staff_line_nbr = 1

                elif random_number == 17:
                    y_val = self.y_F4  # F4
                    self.notes[i].note_staff_line_nbr = 2

                elif random_number == 18:
                    y_val = self.y_G4
                    self.notes[i].note_staff_line_nbr = 2

                elif random_number == 19:
                    y_val = self.y_A5  # A5
                    self.notes[i].note_staff_line_nbr = 3

                elif random_number == 20:
                    y_val = self.y_B5
                    self.notes[i].note_staff_line_nbr = 3

                elif random_number == 21:
                    y_val = self.y_C5  # C5
                    self.notes[i].note_staff_line_nbr = 4

                elif random_number == 22:
                    y_val = self.y_D5
                    self.notes[i].note_staff_line_nbr = 4

                elif random_number == 23:
                    y_val = self.y_E5  # E5
                    self.notes[i].note_staff_line_nbr = 5

                elif random_number == 24:
                    y_val = self.y_F5
                    self.notes[i].note_staff_line_nbr = 5

                elif random_number == 25:
                    y_val = self.y_G5  # G5
                    self.notes[i].note_staff_line_nbr = 6

                elif random_number == 26:
                    y_val = self.y_A6  # requires ledger.
                    self.notes[i].note_staff_line_nbr = 6
                    ledger_required = 1
                    ledger_pos = 1

                elif random_number == 27:
                    y_val = self.y_B6  # requires ledger.
                    self.notes[i].note_staff_line_nbr = 6
                    ledger_required = 1
                    ledger_pos = 1

                elif random_number == 28:
                    y_val = self.y_C6  # requires ledger.
                    self.notes[i].note_staff_line_nbr = 6
                    ledger_required = 2
                    ledger_pos = 1

                # self.note_1_pos_x = self.x_start + (self.x_end - self.x_start) * 0.2 + (i * self.x_start * 1.7)
                self.note_1_pos_x = self.x_start + (self.x_end - self.x_start) * 0.333 + (
                        i * self.x_start * 2.3)  # for 3 note staff

                self.notes[i].pos = (self.note_1_pos_x,
                                     y_val)  # F4 Note # placing th note 30% from the start of the staff line
                self.notes[i].note_value = [generated_note, actual_note]
                self.notes[i].size = self.note_size
                self.notes[i].set_stem(y_val)
                self.notes[i].set_label('F', y_val)
                if i == 0:
                    self.notes[i].set_rect(self.distance_between_lines)
                # print("Note value" + str(self.notes[i].note_value))
                if ledger_required > 0:
                    if ledger_pos == -1:  # ledger_pos == -1 means its below the first staff line like middle C etc.
                        self.notes[i].set_ledger(ledger_required, ledger_pos, self.y_F4, self.distance_between_lines)
                    else:
                        self.notes[i].set_ledger(ledger_required, ledger_pos, self.y_G5, self.distance_between_lines)

            # Set clef Signs
            if self.clef == "Bass":
                self.treble_clef_sign.source = 'images/F_Clef.png'
                self.treble_clef_sign.pos = (self.x_start - 20, self.y_F4 - (self.distance_between_lines * 2))
                self.treble_clef_sign.size = (self.distance_between_lines * 6, self.distance_between_lines * 8.2)
            else:
                self.treble_clef_sign.source = 'images/G_Clef.png'
                self.treble_clef_sign.pos = (self.x_start - 20, self.y_F4 - (self.distance_between_lines * 2))
                self.treble_clef_sign.size = (self.distance_between_lines * 6, self.distance_between_lines * 8.2)

    def game_over(self):
        # print("Game over!!!")
        game_over_status = ""
        if self.correct_answer_in_set >= 8:
            game_over_status = "Great Job!!! That was Awesome"
        elif self.correct_answer_in_set >= 5:
            game_over_status = "Good Job!!! Well tried"
        else:
            game_over_status = "Perfection is not the goal, progress is."

        app = MDApp.get_running_app()
        app.change_palette(theme='Dark', prim_palette='Cyan')
        # #print("self.correct_answer***********************************=" + str(self.correct_answer_in_set))
        app.root.get_screen('end_screen').set_result_motivation(game_over_status)
        app.root.get_screen('end_screen').set_correct_answers(self.correct_answer_in_set)
        app.root.get_screen('end_screen').set_wrong_answers(self.wrong_answer_in_set)
        app.root.get_screen('end_screen').set_session_review_questions(self.quiz_sets)

        #print(self.quiz_set)

        app.root.current = 'end_screen'

    def add_notes_staff(self, y, pos):
        if pos == 1:
            self.note_1.pos = (self.note_1_pos_x, self.y)

        # self.label_1 = Label(text='F', font_size=50, color=(1, 0, 0, 1),
        #                pos=(self.note_1_pos_x, self.y1 + (self.y1 * .20)))

    def validate_answer(self, instance):
        if instance is None:
            choose_button_val = "C"
        else:
            choose_button_val = instance.val[0]

        if self.b_end_game:
            return

        #print("current index---------------------" + str(self.current_note_index))
        # print("Note value =" + str(self.notes[0].note_value))
        #print("Note choose_button_val[0] =" + str(choose_button_val[0]))
        self.attempted_answer = self.attempted_answer + 1

        if self.NUMBER_OF_NOTES == self.attempted_answer - 1:
            # print("All answer attempted we can show next set.")
            self.snackbar.dismiss()
            self.snackbar = None
            self.next_set_notes_sound.play()
            self.update_json_data()
            # self.reset_staff_show_next()
            Clock.schedule_once(self.wait_before_reset_show_next, 0.5)
            return

        if choose_button_val[0] == self.notes[self.current_note_index].note_value[0]:
            # print("Correct answer")
            if self.attempted_answer <= 4:
                self.correct_answer_sound_2.play()
            else:
                self.correct_answer_sound_1.play()

            AnimationHelper.spawn_animation(self.notes[self.current_note_index].button_anim)
            # instance.background_color = [0, 1, 0, 1]

            self.notes[self.current_note_index].label.text = self.notes[self.current_note_index].note_value[0]  # 'F'
            self.notes[self.current_note_index].label.color = (0, 1, 0, 1)
            self.notes[self.current_note_index].set_rect(self.distance_between_lines, 'GREEN')
            self.notes[self.current_note_index].texture = self.correct_note_tex.texture
            self.notes_attempted[self.notes[self.current_note_index].note_value[1]] = 1

            self.correct_answer = self.correct_answer + 1
            self.correct_answer_in_set = self.correct_answer_in_set + 1
            #print("correct_answer_in_set after adding=" + str(self.correct_answer_in_set))

            ledger_point = [None] * 4
            for k in range(self.notes[self.current_note_index].num_of_ledger):
                ledger_point[k] = self.notes[self.current_note_index].note_ledger[k].points

            self.quiz_set.add_clef(self.clef)
            self.quiz_set.add_question(self.notes[self.current_note_index].note_value[0],
                                       self.notes[self.current_note_index].label.text, True,
                                       self.notes[self.current_note_index].stem.points,
                                       self.notes[self.current_note_index].label_pos,
                                       self.notes[self.current_note_index].label.size,
                                       self.notes[self.current_note_index].label.text,
                                       self.notes[self.current_note_index].num_of_ledger,
                                       self.notes[self.current_note_index].pos,
                                       self.notes[self.current_note_index].size,
                                       ledger_point
                                       )
            self.quiz_set.add_notes(self.notes[self.current_note_index])
        else:
            # print("Wrong answer")
            self.wrong_answer_sound.play()
            self.notes[self.current_note_index].label.text = self.notes[self.current_note_index].note_value[0]  # 'F'
            self.notes[self.current_note_index].label.color = (1, 0, 0, 1)
            self.notes[self.current_note_index].set_rect(self.distance_between_lines, 'RED')
            self.notes_attempted[self.notes[self.current_note_index].note_value[1]] = 0
            self.notes[self.current_note_index].texture = self.wrong_note_tex.texture
            self.wrong_answer_in_set = self.wrong_answer_in_set + 1

            ledger_point = [None] * 4
            for k in range(self.notes[self.current_note_index].num_of_ledger):
                ledger_point[k] = self.notes[self.current_note_index].note_ledger[k].points

            self.quiz_set.add_clef(self.clef)
            self.quiz_set.add_question(self.notes[self.current_note_index].note_value[0],
                                       self.notes[self.current_note_index].label.text, False,
                                       self.notes[self.current_note_index].stem.points,
                                       self.notes[self.current_note_index].label_pos,
                                       self.notes[self.current_note_index].label.size,
                                       self.notes[self.current_note_index].label.text,
                                       self.notes[self.current_note_index].num_of_ledger,
                                       self.notes[self.current_note_index].pos,
                                       self.notes[self.current_note_index].size,
                                       ledger_point
                                       )

            self.quiz_set.add_notes(self.notes[self.current_note_index])

        if self.current_note_index < self.NUMBER_OF_NOTES - 1:
            self.current_note_index += 1
            self.notes[self.current_note_index].set_rect(self.distance_between_lines, 'GRAY')
            # print(self.current_note_index)

        # print("self.attempted_answer=" + str(self.attempted_answer))
        if self.NUMBER_OF_NOTES == self.attempted_answer:

            self.number_of_sets_completed = self.number_of_sets_completed + 1
            self.quiz_sets.append(self.quiz_set)

            if self.number_of_sets_completed >= self.NUMBER_OF_SETS:
                # print(len(self.quiz_sets))
                # End game condition met.
                self.b_end_game = True
                #Clock.schedule_once(self.game_over_callback, 1)
                self.show_continue_snackbar(end_flag=True)
                # self.play_bg_music("wrong", n=self.correct_answer) # play sound on game over.

            else:
                # self.reset_staff_event = Clock.schedule_once(self.reset_staff_callback, 5)
                self.reset_staff_event = self.show_continue_snackbar()

                if self.speech_play == 1:
                    self.speech_play = 0
                    if self.correct_answer > self.NUMBER_OF_NOTES - 1:
                        self.play_bg_music("correct")
                    else:
                        self.play_bg_music("wrong", n=self.correct_answer)
                else:
                    self.speech_play += 1

    # dt means delta-time
    def reset_staff_callback(self, dt):
        self.reset_staff_show_next()

    def game_over_callback(self):
        app = MDApp.get_running_app()
        app.g_quiz_sets = self.quiz_sets
        self.b_end_game = True
        self.game_over()

    def play_bg_music(self, answer, n=5):
        pass
        # if answer == "correct":
        #     r = random.randint(0, 3)
        #     if r == 0:
        #         self.correct_1.play()
        #     elif r == 1:
        #         self.correct_2.play()
        #     elif r == 2:
        #         self.correct_3.play()
        #     else:
        #         self.correct_4.play()
        #
        # else:
        #     if n == self.NUMBER_OF_NOTES - 1:
        #         r = random.randint(0, 2)
        #         if n == 0:
        #             self.correct_6.play()
        #         elif r == 1:
        #             self.wrong_1.play()
        #         else:
        #             self.correct_5.play()
        #
        #     elif n == self.NUMBER_OF_NOTES - 2:
        #         r = random.randint(0, 3)
        #         if r == 0:
        #             self.wrong_2.play()
        #         elif r == 1:
        #             self.wrong_3.play()
        #         else:
        #             self.wrong_4.play()
        #
        #     else:
        #         r = random.randint(0, 3)
        #         if r == 0:
        #             self.wrong_4.play()
        #         elif r == 3:
        #             self.wrong_5.play()
        #         else:
        #             self.wrong_6.play()

    def stop_bg_music(self):
        self.correct.stop()

    def update_json_data(self):
        pass

    def new_game_init(self):
        self.b_end_game = False
        self.number_of_sets_completed = 0
        self.correct_answer_in_set = 0
        self.wrong_answer_in_set = 0
        self.quiz_set = SightReaderQuizSet([], "", [])
        self.quiz_sets = []
        self.speech_play = 0
        self.attempted_answer = 0
        self.correct_answer = 0
        app = MDApp.get_running_app()
        self.NUMBER_OF_SETS = app.g_number_of_slide
        #print("app.g_number_of_slide-Sight Reader" + str(self.NUMBER_OF_SETS))

    def wait_before_reset_show_next(self, dt):
        self.reset_staff_show_next()

    def reset_staff_show_next(self):
        self.cancel_reset_staff_event()
        if not self.b_end_game:
            for i in range(0, self.NUMBER_OF_NOTES):
                self.notes[i].reset_note()
                self.notes[i].label.text = ''
                self.notes[i].texture = CoreImage('images/tex_note.png').texture
                self.notes[i].texture = CoreImage('images/tex_note.png').texture
            # self.reset_staff()
            self.current_note_index = 0
            self.update_staff_lines()
            self.quiz_set = SightReaderQuizSet([], "", [])

    def update_note(self, y):
        # y=0 middle C, 1= D, 2 = E .. and so on. -1=ledger b, -2=A
        # print("Called Update_note")
        # y will be generated ramdomly.

        if y == 3:
            y_val = self.y_F4  # F Note
        elif y == 5:
            y_val = self.y_A5  # A Note
        elif y == 7:
            y_val = self.y_C5  # C Note
        elif y == 9:
            y_val = self.y_E5  # E Note
        elif y == 11:
            y_val = self.y_G5  # G Note
        else:
            y_val = self.y_C5  # C Note

        # self.note_1.pos = (self.note_1_pos_x, y_val)


    def show_continue_snackbar(self, end_flag= False):
        num_of_correct = self.correct_answer
        t = ""
        if num_of_correct > 3:
            t = "[color=#FF69B4][font=littledays][size=32]Awesome!!! You got {} correct".format(num_of_correct)
        elif num_of_correct > 2:
            t = "[color=#FF69B4][font=littledays][size=32]Good Job!!! You got {} correct".format(num_of_correct)
        elif num_of_correct > 0:
            t = "[color=#FF69B4][font=littledays][size=32]Ok, few slip-ups there. You got {} correct".format(
                num_of_correct)
        else:
            t = "[color=#FF69B4][font=littledays][size=25]Oopsie daisy!"

        self.snackbar = Snackbar(
            text=t,
            # duration=10,
            auto_dismiss=False,
            font_size=35
        )
        self.snackbar.size_hint_y = (0.20)
        # self.snackbar.size_hint = (0.35, 0.20)
        # self.snackbar.pos_hint = {"center_x": 0.7, "center_y": 0.1}
        if end_flag == True:
            self.snackbar.buttons = [
            MDFillRoundFlatButton(
                text="[color=#030304][font=littledays][size=18]Continue",
                md_bg_color="4dffff",
                on_release=self.snack_bar_dismiss_and_end_quiz,
                size_hint=(0.45, None),
                pos_hint={'center_x': 0.5, 'center_y': 0.5}
            ),
            ]
            self.snackbar.open()
        else:
            self.snackbar.buttons = [
                MDFillRoundFlatButton(
                    text="[color=#030304][font=littledays][size=18]Continue",
                    md_bg_color="4dffff",
                    on_release=self.snack_bar_dismiss,
                    size_hint=(0.45, None),
                    pos_hint={'center_x': 0.5, 'center_y': 0.5}
                ),
            ]
            self.snackbar.open()

    def snack_bar_dismiss_and_end_quiz(self,instance):
        if self.snackbar is not None:
            self.snackbar.dismiss()
            self.game_over_callback()

    def snack_bar_dismiss(self, instance):
        if self.snackbar is not None:
            self.snackbar.dismiss()
            self.next_set_notes_sound.play()
            # self.validate_answer(instance)
            self.validate_answer(None)

    def cleanup_exit(self):
        if self.snackbar is not None:
            self.snackbar.dismiss()
            self.snackbar = None


class KeyboardButton(Button, MagicBehavior):
    val = None
    key_num = 0


class KeyBoardLayout(RelativeLayout):

    def note_press(self, instance):
        if instance.val[0] == self.app.root.get_screen('sight_reader').ids.staff.note_value[0]:
            # print("Correct Answer!!!")
            self.app.score = self.app.score + 10

        self.app.root.get_screen('sight_reader').ids.staff.validate_answer(instance)
        self.app.root.get_screen('sight_reader').ids.staff.update_note(3)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = App.get_running_app()
        # #print("self.root--" + str(self.height))
        pos_increment_steps = .07  # Earlier value was .12 when there were only 8 white keys.
        val_size_hint_x = .07  # Earlier value was .12 when there were only 8 white keys.
        notes_list = ['C', 'D', 'E', 'F', 'G', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'A', 'B']
        # White Keys
        for i in range(0, 14):
            b = KeyboardButton(size_hint_x=val_size_hint_x, pos_hint={"x": i * pos_increment_steps},
                               background_normal='images/white_key_2.png')
            b.val = [notes_list[i]]
            b.bind(on_press=self.note_press)
            self.add_widget(b)

        first_black_key_pos = .045  # Earlier value was .07 when there were only 8 white keys.
        two_black = True
        skip_a_note = False
        black_notes_count = 0
        # .07 + (i*.12)
        black_notes_list = ['C#|Db', 'D#|Eb', '', 'F#|Gb', 'G#|Ab', 'A#|Bb', '', '', 'C#|Db', 'D#|Eb', '', 'F#|Gb',
                            'G#|Ab', 'A#|Bb']
        black_val_size_hint_x = .045  # Earlier value was .07 when there were only 8 white keys.
        black_val_size_hint_y = .6
        for i in range(0, 13):
            if not skip_a_note:
                key_pos = first_black_key_pos + (i * pos_increment_steps)
                if two_black:
                    black_notes_count = black_notes_count + 1
                    b = KeyboardButton(size_hint_x=black_val_size_hint_x, size_hint_y=black_val_size_hint_y,
                                       pos_hint={"x": key_pos, "top": 1},
                                       background_normal='images/black-key.jpg')
                    b.val = black_notes_list[i].split("|")
                    self.add_widget(b)
                    if black_notes_count >= 2:
                        two_black = False
                        skip_a_note = True
                        black_notes_count = 0
                else:
                    black_notes_count = black_notes_count + 1
                    b = KeyboardButton(size_hint_x=black_val_size_hint_x, size_hint_y=black_val_size_hint_y,
                                       pos_hint={"x": key_pos, "top": 1},
                                       background_normal='images/black-key.jpg')
                    b.val = black_notes_list[i].split("|")
                    self.add_widget(b)
                    if black_notes_count >= 3:
                        two_black = True
                        skip_a_note = True
                        black_notes_count = 0
            else:
                skip_a_note = False

    def on_size(self, *args):
        self.height = self.parent.size[1] * 0.9
        # #print("self.height--"+str(self.height))


class RedBox(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Load an image and convert it to a texture
        #image_path = 'images/velvet.jpg'

        with self.canvas:
            Color(0.58, 0, 0, 0.9)  # set the color to red
            #Color(1, 1, 1, 1)  # set the color to white for texture
            s = (self.size[0], self.size[1] - 6)
            Rectangle(pos=self.pos, size=s)  # draw a rectangle
            #r.texture = CoreImage(image_path).texture

    def on_size(self, *args):
        self.canvas.clear()
        image_path = 'images/velvet.jpg'
        with self.canvas:
            Color(0.58, 0, 0, 0.9)  # set the color to red
            #Color(1, 1, 1, 1)  # set the color to White
            s = (self.size[0] - 20, self.size[1] - 16)
            Rectangle(pos=self.pos, size=s)  # draw a rectangle
            #r.texture = CoreImage(image_path).texture
