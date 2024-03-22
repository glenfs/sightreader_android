from random import random

from kivy.app import App
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from kivy.core.text import LabelBase
from kivy.graphics import Color, Line, Rectangle
from kivy.properties import DictProperty, NumericProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.widget import Widget
from kivymd.app import MDApp
from kivymd.uix.behaviors import MagicBehavior
from kivymd.uix.button import MDFillRoundFlatButton
from kivymd.uix.snackbar import Snackbar

from Lesson.Lesson_conversation import Lesson
from animations.Button_animation import AnimationHelper
from note import Note
from kivy.core.image import Image as CoreImage

class LessonScreen(Screen):
    def on_size(self, *args):
        # print(self.ids)
        self.ids.staff.lesson_master()


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
    clef = None
    NUMBER_OF_SETS = 1  # this value is set in the main program. Initialized here in the constructor. 2 is default value.
    NUMBER_OF_NOTES = 3
    LESSON_PROGRESS = 0
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
    attempted_answer = 0

    def __init__(self, **kwargs):
        super(MusicStaff, self).__init__(**kwargs)

        self.app = MDApp.get_running_app()
        self.NUMBER_OF_SETS = self.app.g_number_of_slide
        self.speech_play = 0
        self.notes_selection_menu = None
        self.notes_selection_menu_treble = None

        self.label_1 = None
        self.note_1_pos_x = NumericProperty(0)
        self.note_1_rect = None
        self.notes = [None] * self.NUMBER_OF_NOTES

        self.current_note_index = 0
        self.create_staff_lines()

        self.clef = App.get_running_app().clef_selected
        # #print("app.notes_selection_menu_Treble=====")
        # #print(app.notes_selection_menu_Treble)
        self.notes_attempted = {}

        self.number_of_sets_completed = 0
        self.b_end_game = False
        self.reset_staff_event = None
        self.snackbar = None
        self.attempted_answer
        self.LESSON_PROGRESS = 0
        self.snackbar_active = False
        self.lesson = None
        self.lesson_notes = None


    def cancel_reset_staff_event(self):
        if self.reset_staff_event is not None:
            Clock.unschedule(self.reset_staff_event)

    def reset_staff(self):
        self.label_1 = None
        self.note_1_pos_x = NumericProperty(0)
        self.note_1_rect = None
        self.notes = [None] * self.NUMBER_OF_NOTES
        self.current_note_index = 0
        self.create_staff_lines()

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def on_parent(self, widget, parent):
        print("On parent size  W:" + str(self.width) + " H:" + str(self.height))

    def on_size(self, *args):
        # placing the logic here as we need to set the notes selected once after the selection is made, so cannot do in __init method.
        self.staff_lines_initialize()
        self.update_staff_lines_init()

    def create_staff_lines(self):
        line_width = 1.0
        stem_line_width = 1.2

        with self.canvas:
            Color(0, 0, 0, 0.6)  # black color
            self.line_1 = Line(points=[0, 100, 2, 100], width=line_width)
            #Color(0, 1, 0, 1)  # Green color
            self.line_2 = Line(points=[0, 100, 2, 100], width=line_width)
            #Color(0.9, 0.8, 0, 1)  # yellow color
            self.line_3 = Line(points=[0, 100, 2, 100], width=line_width)
            #Color(1, 0, 1, 1)
            self.line_4 = Line(points=[0, 100, 2, 100], width=line_width)
            #Color(0.6, 0.4, 0.2, 1)
            self.line_5 = Line(points=[0, 100, 2, 100], width=line_width)
            self.treble_clef_sign = Rectangle(source='', pos=(self.start_x - 50, self.start_y - 20), size=(106, 106))

            #Color(0, 0, 0, 1)  # black color
            self.note_size = (0, 0)

            # self.note_1 = Note(pos=(0, 0), size=self.note_size)
            for i in range(self.NUMBER_OF_NOTES):
                self.notes[i] = Note(pos=(0, 0), size=self.note_size)

                # if i == 0:
                # self.notes[i].note_show = True

    def staff_lines_initialize(self):
        self.pos = [self.pos[0], self.parent.size[1] / 2]
        w = self.width
        # 87.5 was calculated by trial and error by having a screen width of 800 and 700 being the max width appeared almost right.  800-100 = 700, so percentage to minus is 87.5%
        max_width_staff_lines = ((w * 80) / 100)
        min_width_staff_lines = ((w * 42) / 100)

        w = max_width_staff_lines if w >= max_width_staff_lines else min_width_staff_lines if w <= min_width_staff_lines else w
        self.x_end = int(w * 1.1)
        self.x_start = int(w * .1)  # making the staff start from the x most cooardinates

        h = self.height
        max_height_staff_lines = ((h * 72.5) / 100)
        min_height_staff_lines = ((h * 49.16) / 100)
        h = max_height_staff_lines if h >= max_height_staff_lines else min_height_staff_lines if h <= min_height_staff_lines else h
        self.distance_between_lines = int(h * 0.07)

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

        print("self.x_start=" + str(self.x_start))
        print("self.y_F4=" + str(self.y_F4))
        print("self.x_end=" + str(self.x_end))
        print("width=" + str(self.width))

        self.line_1.points = [self.x_start, self.y_F4, self.x_end, self.y_F4]
        self.line_2.points = [self.x_start, self.y_A5, self.x_end, self.y_A5]
        self.line_3.points = [self.x_start, self.y_C5, self.x_end, self.y_C5]
        self.line_4.points = [self.x_start, self.y_E5, self.x_end, self.y_E5]
        self.line_5.points = [self.x_start, self.y_G5, self.x_end, self.y_G5]

        self.note_size = (w * .045, h * .07)
        #self.note_size = (100, 130)

        # Set clef Signs
        if self.clef == "Bass":
            self.treble_clef_sign.source = 'images/F_Clef.png'
            self.treble_clef_sign.pos = (self.x_start - 20, self.y_F4 - (self.distance_between_lines * 2))
            self.treble_clef_sign.size = (self.distance_between_lines * 6, self.distance_between_lines * 8.2)
        else:
            self.treble_clef_sign.source = 'images/G_Clef.png'
            self.treble_clef_sign.pos = (self.x_start - 20, self.y_F4 - (self.distance_between_lines * 2))
            self.treble_clef_sign.size = (self.distance_between_lines * 6, self.distance_between_lines * 8.2)

    def update_staff_lines_init(self):
        if self.lesson_notes != None:
            print("called update")
            if not self.b_end_game:

                ledger_required = 0
                y_val = 0
                ledger_pos = 0

                # I need to parameterize 20, notes_dict,  random.randint(0, 20) 20 should be parameterized.
                # self.clef = App.get_running_app().clef_selected
                self.clef = 'Treble'
                # print("Clef=" + str(self.clef))

                for i in range(0, self.NUMBER_OF_NOTES):
                    ledger_required = 0

                    # C4 is 15
                    random_number = self.lesson_notes[i]
                    generated_note = self.notes_dict[random_number]
                    actual_note = self.notes_dict[random_number]
                    generated_note = generated_note[0]  # doing this because the data we get is like C4, D4 B5 etc.

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
                        self.note_staff_line_nbr = 4

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


                    if self.notes[i].note_show == True:
                        self.note_1_pos_x = self.x_start + (self.x_end - self.x_start) * 0.2 + (i * self.x_start * 1.7)
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
                                self.notes[i].set_ledger(ledger_required, ledger_pos, self.y_F4,
                                                         self.distance_between_lines)
                            else:
                                self.notes[i].set_ledger(ledger_required, ledger_pos, self.y_G5,
                                                         self.distance_between_lines)

    def update_staff_lines(self, i):
        if self.lesson_notes != None:
            print("called update")
            if not self.b_end_game:

                ledger_required = 0
                y_val = 0
                ledger_pos = 0

                # I need to parameterize 20, notes_dict,  random.randint(0, 20) 20 should be parameterized.
                # self.clef = App.get_running_app().clef_selected
                self.clef = 'Treble'
                # print("Clef=" + str(self.clef))

                ledger_required = 0

                # C4 is 15
                random_number = self.lesson_notes[i]
                generated_note = self.notes_dict[random_number]
                actual_note = self.notes_dict[random_number]
                generated_note = generated_note[0]  # doing this because the data we get is like C4, D4 B5 etc.

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
                    self.note_staff_line_nbr = 4

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

                if self.notes[i].note_show == True:
                    self.note_1_pos_x = self.x_start + (self.x_end - self.x_start) * 0.2 + (i * self.x_start * 1.7)
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
                            self.notes[i].set_ledger(ledger_required, ledger_pos, self.y_F4,
                                                     self.distance_between_lines)
                        else:
                            self.notes[i].set_ledger(ledger_required, ledger_pos, self.y_G5,
                                                     self.distance_between_lines)

    def game_over(self):
        # print("Game over!!!")
        game_over_status = ""
        self.quiz_set.add_clef(self.clef)

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

        app.root.current = 'end_screen'

    def add_notes_staff(self, y, pos):
        if pos == 1:
            self.note_1.pos = (self.note_1_pos_x, self.y)

        # self.label_1 = Label(text='F', font_size=50, color=(1, 0, 0, 1),
        #                pos=(self.note_1_pos_x, self.y1 + (self.y1 * .20)))

    def validate_answer(self, instance):
        choose_button_val = instance.val[0]

        if self.b_end_game:
            return

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
            # if self.attempted_answer <= 4:
            # self.correct_answer_sound_2.play()
            # else:
            # self.correct_answer_sound_1.play()
            AnimationHelper.spawn_animation(instance)
            instance.background_color = [0, 1, 0, 1]

            self.notes[self.current_note_index].label.text = self.notes[self.current_note_index].note_value[0]  # 'F'
            self.notes[self.current_note_index].label.color = (0, 1, 0, 1)
            self.notes[self.current_note_index].set_rect(self.distance_between_lines, 'GREEN')
            self.notes_attempted[self.notes[self.current_note_index].note_value[1]] = 1

            # Set the progress bar for the lesson.
            self.lesson.lesson_structure.finish_step()
            progress_value = self.app.root.get_screen('lesson').ids.lesson_progress.value
            self.app.root.get_screen('lesson').ids.lesson_progress.value = progress_value + 10

            # if self.LESSON_PROGRESS == 3:
            #     self.show_continue_snackbar("Press continue to proceed.")
            #     self.app.root.get_screen(
            #         'lesson').ids.dialogue.text = "Good Job!!!."

            ledger_point = [None] * 4
            for k in range(self.notes[self.current_note_index].num_of_ledger):
                ledger_point[k] = self.notes[self.current_note_index].note_ledger[k].points

            if self.current_note_index < self.NUMBER_OF_NOTES - 1:
                self.current_note_index += 1
                self.notes[self.current_note_index].set_rect(self.distance_between_lines, 'GRAY')
                self.notes[self.current_note_index].note_show = True
                # print(self.current_note_index)

        else:
            # print("Wrong answer")
            self.wrong_answer_sound.play()
            self.notes[self.current_note_index].label.text = self.notes[self.current_note_index].note_value[0]  # 'F'
            self.notes[self.current_note_index].label.color = (1, 0, 0, 1)
            self.notes[self.current_note_index].set_rect(self.distance_between_lines, 'RED')
            self.notes_attempted[self.notes[self.current_note_index].note_value[1]] = 0

            ledger_point = [None] * 4
            for k in range(self.notes[self.current_note_index].num_of_ledger):
                ledger_point[k] = self.notes[self.current_note_index].note_ledger[k].points

        # print("self.attempted_answer=" + str(self.attempted_answer))
        if self.NUMBER_OF_NOTES == self.attempted_answer:

            self.number_of_sets_completed = self.number_of_sets_completed + 1
            self.quiz_sets.append(self.quiz_set)

            if self.number_of_sets_completed >= self.NUMBER_OF_SETS:
                # print(len(self.quiz_sets))
                # End game condition met.
                self.b_end_game = True
                Clock.schedule_once(self.game_over_callback, 1)

                # self.play_bg_music("wrong", n=self.correct_answer) # play sound on game over.

            else:
                # self.reset_staff_event = Clock.schedule_once(self.reset_staff_callback, 5)
                # self.reset_staff_event = self.show_continue_snackbar()

                if self.speech_play >= 2:
                    self.speech_play = 0
                    if self.correct_answer > 4:
                        self.play_bg_music("correct")
                    else:
                        self.play_bg_music("wrong", n=self.correct_answer)
                else:
                    self.speech_play += 1

    # dt means delta-time
    def reset_staff_callback(self, dt):
        self.reset_staff_show_next()

    def game_over_callback(self, dt):
        app = MDApp.get_running_app()
        app.g_quiz_sets = self.quiz_sets
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
        self.b_end_game = False
        self.number_of_sets_completed = 0
        self.correct_answer_in_set = 0
        self.wrong_answer_in_set = 0

    def wait_before_reset_show_next(self, dt):
        self.reset_staff_show_next()

    def reset_staff_show_next(self):
        self.cancel_reset_staff_event()
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

    def snack_bar_dismiss(self, instance):
        self.snackbar.dismiss()
        self.snackbar = None
        self.snackbar_active = False
        self.update_conversation()
        # self.validate_answer(['C'])

    def add_note(self, ):
        pass

    def show_continue_snackbar(self, t):
        if not self.snackbar_active:
            print("show_continue_snackbar")
            self.snackbar = Snackbar(
                text='[color=#FFFF00][font=littledays][size=18]' + t,
                # duration=10,
                auto_dismiss=False,
                font_size=25,
            )
            self.snackbar.size_hint_y = (0.20)
            self.snackbar.buttons = [
                MDFillRoundFlatButton(
                    text="[color=#030304][font=littledays][size=18]Continue",
                    md_bg_color="yellow",
                    on_release=self.snack_bar_dismiss,
                    size_hint=(0.45, None),
                    pos_hint={'center_x': 0.5, 'center_y': 0.5}
                ),
            ]
            self.snackbar.open()
            self.snackbar_active = True

    def character_conversation(self, dt):
        self.app.root.get_screen('lesson').ids.gif.opacity = 1
        self.app.root.get_screen('lesson').ids.dialogue.opacity = 1
        self.LESSON_PROGRESS = self.LESSON_PROGRESS + 1
        # Schedule the function to be called after a delay of 2 seconds
        # Clock.schedule_once(lambda dt: self.show_continue_snackbar("When you are done, click on continue"), 2)

    def update_conversation(self):
        print("Update Conversations")
        self.LESSON_PROGRESS = self.LESSON_PROGRESS + 1
        print("self.LESSON_PROGRESS=" + str(self.LESSON_PROGRESS))
        if self.LESSON_PROGRESS == 3:
            self.app.root.get_screen(
                'lesson').ids.dialogue.text = "Highlighted key represents the note in the staff. now click on it."
            self.app.root.get_screen('lesson').ids.mykeyboard.opacity = 1
        elif self.LESSON_PROGRESS == 4:
            self.reset_staff_show_next()

        # self.snackbar.dismiss()

    def start_lesson(self, dt):
        print("lesson starts")
        print("self.LESSON_PROGRESS=" + str(self.LESSON_PROGRESS))
        self.app.root.get_screen('lesson').ids.staff.opacity = 1

    def show_snackbar(self, dt):
        self.show_continue_snackbar("When you are done, click on continue")

    def lesson_master(self):
        if self.LESSON_PROGRESS == 0:
            self.LESSON_PROGRESS = 1
            return

        lesson1 = Lesson(1, 1)
        lesson1.add_conversation("Hello, how are you?")
        lesson1.add_conversation("I'm fine, thank you.")
        lesson1.add_snackbar_text("Great Thank you.")
        lesson1.add_snackbar_text("Bye.")

        lesson1.notes = [14, 15, 16]
        self.lesson_notes = lesson1.notes

        self.lesson = lesson1

        lesson1.run_lesson()

        # for i in range(lesson1.num_of_steps):
        #    Clock.schedule_once(self.add_delay, 2*i)

        # Clock.schedule_once(self.start_lesson, 2)

        # Clock.schedule_once(self.start_lesson, 2)
        # Clock.schedule_once(self.character_conversation, 3)
        # Clock.schedule_once(self.show_snackbar, 4)

    def add_delay(self, dt):
        print("just delay it")
        self.lesson.run_lesson()
        self.update_staff_lines()


class KeyboardButton(Button, MagicBehavior):
    val = None
    id_num = 0

    def __init__(self,id_num, **kwargs):
        super().__init__(**kwargs)
        self.id_num = id_num


    def set_id(self,id):
        self.id_num = id


class KeyBoardLayout(RelativeLayout):

    def note_press(self, instance):
        # This method will be called when the button is released
        # #print("Button released")
        # print("instance.val=" + str(instance.val))
        # MusicStaff.update_note(3)
        # app = App.get_running_app()
        # self.staff = app.root.ids.root_widget_1

        # #print(self.app.root.ids)
        # #print(self.app.root.get_screen('sight_reader').ids.staff.note_value)
        # #print(self.app.score)
        # #print(self.app.root.ids.staff.note_value)

        # if instance.val[0] == self.app.root.ids.staff.note_value[0]:
        if instance.val[0] == self.app.root.get_screen('lesson').ids.staff.note_value[0]:
            # print("Correct Answer!!!")
            self.app.score = self.app.score + 10
            # print("Score=" + str(self.app.score))

        # self.app.root.ids.staff.validate_answer(instance.val[0])
        # self.app.root.ids.staff.update_note(3)
        self.app.root.get_screen('lesson').ids.staff.validate_answer(instance)
        self.app.root.get_screen('lesson').ids.staff.update_note(3)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = App.get_running_app()
        # #print("self.root--" + str(self.height))
        pos_increment_steps = .07  # Earlier value was .12 when there were only 8 white keys.
        val_size_hint_x = .07  # Earlier value was .12 when there were only 8 white keys.
        notes_list = ['C', 'D', 'E', 'F', 'G', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'A', 'B']
        # White Keys
        for i in range(0, 14):
            if i == 7:
                b = KeyboardButton(size_hint_x=val_size_hint_x, pos_hint={"x": i * pos_increment_steps},
                                   background_normal='images/white_key_2.png', background_color=(0.7, 0.9, 0.3, 1),id_num=i)
            else:
                b = KeyboardButton(size_hint_x=val_size_hint_x, pos_hint={"x": i * pos_increment_steps},
                                   background_normal='images/white_key_2.png',id_num=i)
            b.val = [notes_list[i]]
            #b.set_id(i)
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
                                       background_normal='images/black-key.jpg',id_num=100+i)
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
                                       background_normal='images/black-key.jpg',id_num=100+i)
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
            s = (self.size[0], self.size[1] - 6)
            Rectangle(pos=self.pos, size=s)  # draw a rectangle

    def on_size(self, *args):
        self.canvas.clear()
        with self.canvas:
            Color(0.58, 0, 0, 0.9)  # set the color to red
            s = (self.size[0] - 20, self.size[1] - 16)
            Rectangle(pos=self.pos, size=s)  # draw a rectangle


class LessonApp(MDApp):
    score = 0
    bg_music = None

    notes_selection_menu_Treble = [False, False, False, False, False, False, False, False, False, False, False, False,
                                   False,
                                   False, False, False, False, False, False, False, False, False, False, False, False,
                                   False, False, False, False]
    notes_selection_menu_Bass = [False, False, False, False, False, False, False, False, False, False, False, False,
                                 False,
                                 False, False, False, False, False, False, False, False, False, False, False, False,
                                 False, False, False, False]

    notes_selection_menu = [False, False, False, False, False, False, False, False, False, False, True, True,
                            True,
                            True, True, True, True, True, True, False, False, False, False, False, False,
                            False, False, False, False]

    clef_selected = "Treble"
    difficulty_selected = "Beginner"
    metric_screen = None
    g_quiz_sets = None
    g_quiz_sets_current_slide = 0
    g_number_of_slide = 3

    def build(self):
        # Register custom fonts
        LabelBase.register(name="littledays",
                           fn_regular="fonts/Basic Comical Regular NC.ttf",
                           fn_bold="fonts/Basic Comical Regular NC.ttf")

        sm = ScreenManager()
        # sm.transition = MDTransitionStack()
        sm.add_widget(LessonScreen(name='lesson'))
        # Set the initial screen (MenuScreen) as the current screen
        sm.current = "lesson"
        return sm


if __name__ == '__main__':
    LessonApp().run()
