import json
import random

from kivy.animation import Animation
from kivy.app import App
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from kivy.graphics import Rectangle, Line, Color, Mesh, Ellipse
from kivy.metrics import dp
from kivy.properties import DictProperty, NumericProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.widget import Widget
from kivymd.app import MDApp
from kivymd.uix.behaviors import MagicBehavior
from kivy.core.image import Image as CoreImage

from SightReaderQuizSet import SightReaderQuizSet
from StreakWidget import StreakWidget
from animations.Button_animation import AnimationHelper
from note import Note


class KeyboardTimer(BoxLayout):
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


class MusicStaffTimer(Widget):
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
    number_of_notes_completed = 0
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

    notes_dict_alphabet_only = {'C': [0, 1, 2, 3, 3, 2, 1], 'D': [1, 0, 1, 2, 3, 3, 2], 'E': [2, 1, 0, 1, 2, 3, 3],
                                'F': [3, 2, 1, 0, 1, 2, 3], 'G': [3, 3, 2, 1, 0, 1, 2], 'A': [2, 3, 3, 2, 1, 0, 1],
                                'B': [1, 2, 3, 3, 2, 1, 0]}

    notes_dict_alphabet_index = {'C': 0, 'D': 1, 'E': 2, 'F': 3, 'G': 4, 'A': 5, 'B': 6}

    notes_index = []
    notes_attempted = {}
    quiz_set = None
    reset_staff_event = None

    def __init__(self, **kwargs):
        super(MusicStaffTimer, self).__init__(**kwargs)

        self.app = MDApp.get_running_app()
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
        self.notes_attempted = {}

        self.correct_answer_sound_1 = SoundLoader.load('sounds/correct_1.mp3')
        self.correct_answer_sound_1.volume = 0.15
        self.correct_answer_sound_2 = SoundLoader.load('sounds/correct_2.mp3')
        self.correct_answer_sound_2.volume = 0.15

        self.wrong_answer_sound = SoundLoader.load('sounds/error.mp3')
        self.wrong_answer_sound.volume = 0.15
        self.next_set_notes_sound = SoundLoader.load('sounds/next_set.mp3')
        self.next_set_notes_sound.volume = 0.15

        self.number_of_notes_completed = 0
        self.b_end_game = False
        self.reset_staff_event = None
        self.long_calculation_saved = 0
        self.long_multiplication_saved = 0
        self.score = 0
        self.streak = 0
        self.animation_helper = AnimationHelper()

    def cancel_reset_staff_event(self):
        pass
        # if self.reset_staff_event is not None:
        # Clock.unschedule(self.reset_staff_event)

    def reset_staff(self):
        self.attempted_answer = 0
        self.correct_answer = 0
        self.label_1 = None
        self.note_1_pos_x = NumericProperty(0)
        self.note_1_rect = None
        self.notes = [None] * self.NUMBER_OF_NOTES
        self.current_note_index = 0
        self.game_over_flag = False
        self.create_staff_lines()
        # self.quiz_set = SightReaderQuizSet()

    def update_rect(self, *args):
        # Update the position and size of the rectangle
        # #print(self.pos)
        # #print(self.size)
        self.rect.pos = self.pos
        self.rect.size = self.size

    def on_parent(self, widget, parent):
        print("On parent size  W:" + str(self.width) + " H:" + str(self.height))

    def on_size(self, *args):
        # #print("On on_size size  W:" + str(self.width) + " H:" + str(self.height))
        # self.start_x = self.width/2
        # self.height = self.height * 0.75
        # self.length_staff = self.width * 0.8

        # placing the logic here as we need to set the notes selected once after the selection is made, so cannot do in __init method.
        self.notes_selection_for_sight_reader()
        self.init_constant_values()
        self.update_staff_lines()

    def notes_selection_for_sight_reader(self):
        number_of_notes = 0
        app = App.get_running_app()
        self.notes_selection_menu_treble = app.notes_selection_menu_Treble
        self.notes_selection_menu = app.notes_selection_menu
        true_count = self.notes_selection_menu.count(True)
        self.notes_index = [None] * true_count

        for index, item in enumerate(self.notes_selection_menu):

            if item:  # if True

                self.notes_index[number_of_notes] = index
                self.notes_mapping_to_dict[index] = self.notes_dict[index]
                number_of_notes = number_of_notes + 1

    def create_staff_lines(self):
        line_width = 1.0
        stem_line_width = 1.2

        with self.canvas:
            Color(1, 1, 1, 1)  # White color
            self.line_1 = Line(points=[0, 100, 2, 100], width=line_width)
            self.line_2 = Line(points=[0, 100, 2, 100], width=line_width)
            self.line_3 = Line(points=[0, 100, 2, 100], width=line_width)
            self.line_4 = Line(points=[0, 100, 2, 100], width=line_width)
            self.line_5 = Line(points=[0, 100, 2, 100], width=line_width)
            self.treble_clef_sign = Rectangle(source='', pos=(self.start_x - 50, self.start_y - 20), size=(106, 106))

            #Color(0, 0, 0, 1)  # black color
            self.note_size = (0, 0)

            #image_path = 'images/tex_note_white_2.png'

            # self.note_1 = Note(pos=(0, 0), size=self.note_size)
            for i in range(self.NUMBER_OF_NOTES):
                self.notes[i] = Note(pos=(0, 0), size=self.note_size,mode='timer')
               # self.notes[i].texture = CoreImage(image_path).texture

            Color(1, 1, 1)  # Set color to red
            self.streak_baloon = Ellipse(pos=(0, 0), size=(0, 0))
            image_path = 'images/streak_Green.png'
            self.streak_baloon.texture = CoreImage(image_path).texture

            # Create Label
            self.streak_baloon_label = Label(text='', font_size=dp(13), pos=(0, 0),
                                             opacity=1,
                                             color="cyan")
            self.add_widget(self.streak_baloon_label)

    def init_constant_values(self):
        #print("Clock.max_iteration-prog")
        #print(Clock.max_iteration)

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

        # self.note_size = (w * .045, h * .07)
        self.note_size = (w * .085, h * .13)

        # I need to parameterize 20, notes_dict,  random.randint(0, 20) 20 should be parameterized.
        self.clef = App.get_running_app().clef_selected

        self.long_calculation_saved = self.x_start + (self.x_end - self.x_start) * 0.333
        self.long_multiplication_saved = self.x_start * 2.3

    def update_staff_lines(self):
        if not self.b_end_game:
            self.attempted_answer = 0
            self.correct_answer = 0

            # self.note_1.pos = (self.x_start + dp(50), y1)  # F4 Note
            # #print("self.x_end , self.x_start=" + str(self.x_end) + "--" + str(self.x_start))
            ledger_required = 0
            y_val = 0
            ledger_pos = 0

            # I need to parameterize 20, notes_dict,  random.randint(0, 20) 20 should be parameterized.
            self.clef = App.get_running_app().clef_selected

            # print("Clef=" + str(self.clef))
            if self.clef == 'Both':
                self.clef = random.choice(['Treble', 'Bass'])

            for i in range(0, self.NUMBER_OF_NOTES):
                ledger_required = 0

                # Clef is Bass
                if self.clef == 'Bass':
                    filtered_list = [value for value in self.notes_index if value <= 16]

                # Clef is Treble
                elif self.clef == 'Treble':
                    filtered_list = [value for value in self.notes_index if value >= 10]

                random_number = random.choice(filtered_list)
                generated_note = self.notes_mapping_to_dict[random_number]
                actual_note = self.notes_mapping_to_dict[random_number]
                generated_note = generated_note[0]  # doing this because the data we get is like C4, D4 B5 etc.
                # self.notes_mapping_to_dict[random_number].split('|')[2] this gives values as A4,C4, B4 etc, we will only get the first character in this.

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

                self.note_1_pos_x = self.long_calculation_saved + (
                        i * self.long_multiplication_saved)  # for 3 note staff
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
                self.treble_clef_sign.source = 'images/F_Clef_inv.png'
                self.treble_clef_sign.pos = (self.x_start - 20, self.y_F4 - (self.distance_between_lines * 2))
                self.treble_clef_sign.size = (self.distance_between_lines * 6, self.distance_between_lines * 8.2)
            else:
                self.treble_clef_sign.source = 'images/G_Clef_inv.png'
                self.treble_clef_sign.pos = (self.x_start - 20, self.y_F4 - (self.distance_between_lines * 2))
                self.treble_clef_sign.size = (self.distance_between_lines * 6, self.distance_between_lines * 8.2)

    def game_over(self):
        # print("Game over!!!")
        self.b_end_game = True
        self.app.root.get_screen('sight_reader_timer').ids.game_over_button.opacity = 0.8
        game_over_status = "Time Up"

        self.app.root.get_screen('end_screen_timer').set_result_motivation(game_over_status)
        self.app.root.get_screen('end_screen_timer').set_correct_answers(self.correct_answer_in_set)
        self.app.root.get_screen('end_screen_timer').set_score(self.score)
        Clock.schedule_once(self.wait_before_end_screen, 3)
        # app.root.current = 'end_screen_timer'

    def wait_before_end_screen(self, dt):
        self.app.change_palette(theme='Dark', prim_palette='Cyan')
        self.app.root.current = 'end_screen_timer'

    def cleanup_on_exit(self):
        #print("Cleanup called")
        self.score = 0
        Clock.unschedule(self.wait_before_end_screen)  # Stop the timer
        self.streak = 0

    def add_notes_staff(self, y, pos):
        if pos == 1:
            self.note_1.pos = (self.note_1_pos_x, self.y)

        # self.label_1 = Label(text='F', font_size=50, color=(1, 0, 0, 1),
        #                pos=(self.note_1_pos_x, self.y1 + (self.y1 * .20)))

    def validate_answer(self, choose_button_val):
        if self.b_end_game:
            return

        if choose_button_val[0] == self.notes[self.current_note_index].note_value[0]:
            # print("Correct answer")
            self.streak = self.streak + 1
            self.correct_answer_sound_1.play()
            self.notes[self.current_note_index].label.text = self.notes[self.current_note_index].note_value[0]  # 'F'
            self.notes[self.current_note_index].label.color = (0, 1, 0, 1)
            self.notes[self.current_note_index].set_rect(self.distance_between_lines, 'GREEN')
            self.notes_attempted[self.notes[self.current_note_index].note_value[1]] = 1
            self.correct_answer = self.correct_answer + 1
            self.correct_answer_in_set = self.correct_answer_in_set + 1
            self.score = self.score + 5

            if self.streak == 5:
                # p =(self.notes[self.current_note_index].label.pos[0], self.notes[self.current_note_index].label.pos[1] - 50)
                score_add = 10
                p = self.app.root.get_screen('sight_reader_timer').ids.score.pos
                self.animation_helper.streak_animation(self.notes[self.current_note_index].label, pos=p,
                                                       streak_num=self.streak, score=score_add)
                self.score = self.score + score_add

            if self.streak == 10:
                # p = (
                # self.notes[self.current_note_index].label.pos[0], self.notes[self.current_note_index].label.pos[1] - 50)
                score_add = 20
                p = self.app.root.get_screen('sight_reader_timer').ids.score.pos
                self.animation_helper.streak_animation(self.notes[self.current_note_index].label, pos=p,
                                                       streak_num=self.streak, score=score_add)
                self.score = self.score + score_add
            if self.streak == 15:
                # p = (
                # self.notes[self.current_note_index].label.pos[0], self.notes[self.current_note_index].label.pos[1] - 50)
                score_add = 30
                p = self.app.root.get_screen('sight_reader_timer').ids.score.pos
                self.animation_helper.streak_animation(self.notes[self.current_note_index].label, pos=p,
                                                       streak_num=self.streak, score=score_add)
                self.score = self.score + score_add

            if self.current_note_index < self.NUMBER_OF_NOTES - 1:
                self.current_note_index += 1
                self.notes[self.current_note_index].set_rect(self.distance_between_lines, 'GRAY')
                # print(self.current_note_index)

            # print("self.attempted_answer=" + str(self.attempted_answer))
            if self.NUMBER_OF_NOTES == self.correct_answer:
                self.reset_staff_show_next()

        else:
            # print("Wrong answer")
            self.streak = 0
            self.wrong_answer_sound.play()

            choosen_note = self.notes_dict_alphabet_only[choose_button_val[0]]
            actual_note_diff = choosen_note[
                self.notes_dict_alphabet_index[self.notes[self.current_note_index].note_value[0]]]
            score_add = (actual_note_diff * 2)
            self.score = self.score - score_add
            p = self.notes[self.current_note_index].pos
            self.animation_helper.streak_animation(self.notes[self.current_note_index].label, pos=p,
                                                   streak_num=self.streak, score=-score_add)

        if self.score > 0:
            self.app.root.get_screen(
                'sight_reader_timer').ids.score.text = '[color=00FF00]' + str(
                self.score) + '[/color]'
        elif self.score < 0:
            self.app.root.get_screen(
                'sight_reader_timer').ids.score.text = '[color=b20000]' + str(
                self.score) + '[/color]'
        else:
            self.app.root.get_screen(
                'sight_reader_timer').ids.score.text = '[color=000000]' + str(
                self.score) + '[/color]'

    def game_over_callback(self, dt):
        self.b_end_game = True
        self.game_over()

    def play_bg_music(self, answer, n=5):
        if answer == "correct":
            r = random.randint(0, 5)
            if r == 0:
                self.correct_1.play()
            elif r == 1:
                self.correct_2.play()
            elif r == 2:
                self.correct_3.play()
            elif r == 3:
                self.correct_4.play()
            elif r == 4:
                self.correct_5.play()
            else:
                self.correct_6.play()
        else:
            if n == 4:
                r = random.randint(0, 2)
                if n == 0:
                    self.few_wrongs.play()
                elif r == 1:
                    self.wrong_2.play()
                else:
                    self.making_great_effort.play()

            elif n == 3:
                r = random.randint(0, 2)
                if r == 0:
                    self.wrong_6.play()
                elif r == 1:
                    self.few_wrongs.play()
                else:
                    self.wrong_4.play()

            elif n == 2:
                r = random.randint(0, 2)
                if r == 0:
                    self.wrong_6.play()
                elif r == 1:
                    self.wrong_5.play()
                else:
                    self.wrong_4.play()
            elif n == 1:
                r = random.randint(0, 2)
                if r == 0:
                    self.wrong_1.play()
                elif r == 1:
                    self.wrong_5.play()
                else:
                    self.wrong_3.play()
            else:
                r = random.randint(0, 1)
                if r == 0:
                    self.wrong_4.play()
                else:
                    self.wrong_1.play()

    def stop_bg_music(self):
        self.correct.stop()

    def new_game_init(self):
        app = MDApp.get_running_app()
        self.b_end_game = False
        self.correct_answer_in_set = 0
        self.wrong_answer_in_set = 0
        app.root.get_screen('sight_reader_timer').ids.game_over_button.opacity = 0
        self.score = 0
        app.root.get_screen('sight_reader_timer').ids.score.text = '[color=FB607F]0[/color]'
        self.streak = 0

    def reset_staff_show_next(self):
        # self.cancel_reset_staff_event()
        if not self.b_end_game:
            for i in range(0, self.NUMBER_OF_NOTES):
                self.notes[i].reset_note()
                self.notes[i].label.text = ''
            # self.reset_staff()
            self.current_note_index = 0
            self.update_staff_lines()

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


class KeyboardButton(Button, MagicBehavior):
    val = None


class KeyBoardLayoutTimer(RelativeLayout):

    def note_press(self, instance):
        # if instance.val[0] == self.app.root.get_screen('sight_reader_timer').ids.staff.note_value[0]:
        ## print("Correct Answer!!!")
        # self.app.score = self.app.score + 10
        ## print("Score=" + str(self.app.score))

        self.app.root.get_screen('sight_reader_timer').ids.staff.validate_answer(instance.val[0])
        # self.app.root.get_screen('sight_reader_timer').ids.staff.update_note(3)

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
        with self.canvas:
            Color(0.58, 0, 0, 0.9)  # set the color to red
            # s = (self.size[0], self.size[1] - 6)
            s = (self.size[0], self.size[1] - 6)
            Rectangle(pos=self.pos, size=s)  # draw a rectangle

    def on_size(self, *args):
        self.canvas.clear()
        with self.canvas:
            Color(0.58, 0, 0, 0.9)  # set the color to red
            s = (self.size[0] - 20, self.size[1] - 16)

            Rectangle(pos=self.pos, size=s)  # draw a rectangle

# class MusicNotesGameApp(App):
#     score = 0
#     # def on_button_click(self, instance):
#     # #print('Button clicked! ' + str(instance.val))
#
#
# Window.clearcolor = (0.9, 0.9, 0.89, 1)
# Window.orientation = 'auto'
# # Window.size = (1080, 1920) # Set window size
# # Window.size = (600, 1000) # Set window size
# MusicNotesGameApp().run()
