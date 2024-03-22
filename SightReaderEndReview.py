from kivy.graphics import Rectangle, Line, Color
from kivy.properties import DictProperty, NumericProperty
from kivy.uix.widget import Widget
from kivymd.app import MDApp

from SightReaderQuizSet import SightReaderQuizSet
from note import Note


class MusicStaffReview(Widget):
    NUMBER_OF_SETS = 2
    NUMBER_OF_NOTES = 3
    pos_hint = DictProperty({'x': 0, 'y': 0})

    start_x = NumericProperty(0)
    start_y = NumericProperty(0)
    line_1 = Line(points=[0, 100, 2, 100])
    line_2 = Line(points=[0, 100, 2, 100])
    line_3 = Line(points=[0, 100, 2, 100])
    line_4 = Line(points=[0, 100, 2, 100])
    line_5 = Line(points=[0, 100, 2, 100])

    treble_clef_sign = None
    note_size = None
    x_start = NumericProperty(0)
    x_end = NumericProperty(0)
    distance_between_lines = 0
    clef = None

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

    quiz_sets = [SightReaderQuizSet] * 2
    notes = []
    clef_sign = Rectangle()
    current_slide = 0
    number_of_slides_in_session = 0

    def __init__(self, **kwargs):
        super(MusicStaffReview, self).__init__(**kwargs)
        app = MDApp.get_running_app()
        self.slide_number = None
        self.notes = [None] * self.NUMBER_OF_NOTES
        self.NUMBER_OF_SETS = app.g_number_of_slide

    def show_next_set(self, qs):
        self.quiz_sets = qs
        self.reset_staff()
        self.canvas.clear()
        self.create_staff_lines(self.current_slide)
        self.init_size_values()
        self.update_staff_lines(self.current_slide)

    def show_prev_set(self, qs):
        self.quiz_sets = qs
        self.reset_staff()
        self.canvas.clear()
        self.create_staff_lines(self.current_slide)
        self.init_size_values()
        self.update_staff_lines(self.current_slide)

    def create_staff_lines(self, slide_number):
        app = MDApp.get_running_app()
        self.current_slide = app.g_quiz_sets_current_slide
        line_width = 1.0
        stem_line_width = 1.2
        number_of_slides_in_session = len(self.quiz_sets)
        # print("number_of_slides_in_session=" + str(number_of_slides_in_session))
        self.notes = [Note] * self.NUMBER_OF_NOTES

        self.canvas.clear()
        with self.canvas:
            Color(0, 0, 0, 1)  # Black color
            self.clef_sign = Rectangle(source='', pos=(self.start_x - 50, self.start_y - 20), size=(106, 106))

            self.line_1 = Line(points=[0, 100, 2, 100], width=line_width)
            self.line_2 = Line(points=[0, 100, 2, 100], width=line_width)
            self.line_3 = Line(points=[0, 100, 2, 100], width=line_width)
            self.line_4 = Line(points=[0, 100, 2, 100], width=line_width)
            self.line_5 = Line(points=[0, 100, 2, 100], width=line_width)
            # self.treble_clef_sign = Rectangle(source='', pos=(self.start_x - 50, self.start_y - 20), size=(0, 0))

            self.init_size_values()

            Color(0, 0, 0, 1)  # black color
            self.note_size = (0, 0)

            # self.note_1 = Note(pos=(0, 0), size=self.note_size)

            for i in range(self.NUMBER_OF_NOTES):
                is_corrrect = self.quiz_sets[slide_number].questions[i]['is_correct']

                self.notes[i].show = True
                self.notes[i] = Note(pos=self.quiz_sets[slide_number].questions[i]['note_pos'],
                                     size=self.quiz_sets[slide_number].questions[i]['note_size'])
                self.notes[i].stem.points = self.quiz_sets[slide_number].questions[i]['stem_points']
                self.notes[i].label.pos = self.quiz_sets[slide_number].questions[i]['label_pos']
                self.notes[i].label.size = self.quiz_sets[slide_number].questions[i]['label_size']
                self.notes[i].label.color = (0.3, 1, 0.4, 0.9)
                self.notes[i].label.outline_width = 2
                self.notes[i].label.text = self.quiz_sets[slide_number].questions[i]['label_text']
                self.notes[i].label.color = (0.3, 1, 0.4, 0.9)

                # if is_corrrect:
                # #print()
                # self.notes[i].rect_green.points = self.quiz_sets[slide_number].notes[i].rect_green.points
                # self.notes[i].rect_green.width = 2 #self.quiz_sets[slide_number].notes[i].rect_green.width
                # else:
                # #print()
                # self.notes[i].rect_red.points = self.quiz_sets[slide_number].notes[i].rect_red.points
                # self.notes[i].rect_red.width = 2 #self.quiz_sets[slide_number].notes[i].rect_red.width

                # num = self.quiz_sets[slide_number].questions[i]['num_of_ledger']
                # self.note_ledger.points = [x - x_val_1, y + (s_y / 2), x + x_val_2, y + (s_y / 2)]
                # for k in range(num):
                # self.notes[i].note_ledger[k].points = self.quiz_sets[slide_number].questions[i]['ledger_point'][k]
                ##self.notes[i].note_ledger[k].points = [[0, 0, 0, 0] #points=[0, 0, 0, 0]

            # Color(1, 0, 0, 1)
            # self.ellipse = Ellipse(pos=(292.0, 413.5), size=(12, 14))

    def init_size_values(self):
        self.pos = [self.pos[0], self.parent.size[1] / 2]
        w = self.width

        # #print("width=" + str(self.width))
        # print(self.note_size)
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
        # self.distance_between_lines = int(h * 0.07)
        self.distance_between_lines = int(h * 0.12)
        # self.note_size = (w * .045, h * .07)
        self.note_size = (w * .085, h * .13)

        # self.note_1.pos = (self.x_start + dp(50), y1)  # F4 Note
        # ##print("self.x_end , self.x_start=" + str(self.x_end) + "--" + str(self.x_start))
        ledger_required = 0
        y_val = 0
        ledger_pos = 0

        # I need to parameterize 20, notes_dict,  random.randint(0, 20) 20 should be parameterized.

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

        self.line_1.points = [self.x_start, self.y_F4, self.x_end, self.y_F4]
        self.line_2.points = [self.x_start, self.y_A5, self.x_end, self.y_A5]
        self.line_3.points = [self.x_start, self.y_C5, self.x_end, self.y_C5]
        self.line_4.points = [self.x_start, self.y_E5, self.x_end, self.y_E5]
        self.line_5.points = [self.x_start, self.y_G5, self.x_end, self.y_G5]

        # Set clef Signs
        if self.clef == "Bass":
            self.clef_sign.source = 'images/F_Clef.png'
            self.clef_sign.pos = (self.x_start - 20, self.y_F4 - (self.distance_between_lines * 2))
            self.clef_sign.size = (self.distance_between_lines * 6, self.distance_between_lines * 8.2)
        else:
            self.clef_sign.source = 'images/G_Clef.png'
            self.clef_sign.pos = (self.x_start - 20, self.y_F4 - (self.distance_between_lines * 2))
            self.clef_sign.size = (self.distance_between_lines * 6, self.distance_between_lines * 8.2)


    def update_staff_lines(self, slide_number):
        app = MDApp.get_running_app()
        self.current_slide = app.g_quiz_sets_current_slide
        # for quiz_set in self.quiz_sets:
        # quiz_set = self.quiz_sets[0]
        # print("slide_number")
        # print(slide_number)

        # self.clef = "Treble"
        self.clef = self.quiz_sets[slide_number].clef
        # self.notes = self.quiz_sets[slide_number].notes.copy()

        # for i in range(0, self.NUMBER_OF_NOTES):
        # #print(self.quiz_sets)
        # self.clef = quiz_set.clef
        # self.notes[i].pos = self.quiz_sets[0].notes[i].pos



        # print("len of quizset=" + str(self.quiz_sets))
        # print('self.treble_clef_sign.size')
        # print(self.treble_clef_sign.size)
        # print(self.distance_between_lines)

        # print("SLIDE NUBER =" + str(slide_number))
        try:
            print(self.quiz_sets[slide_number].notes[0].label.text)
        except IndexError:
            print("Index out of range. Cannot access self.notes[i]")

        try:

            for i in range(self.NUMBER_OF_NOTES):
                is_correct = self.quiz_sets[slide_number].questions[i]['is_correct']

                self.notes[i].show = True
                self.notes[i].pos = self.quiz_sets[slide_number].questions[i]['note_pos']
                self.notes[i].size = self.quiz_sets[slide_number].questions[i]['note_size']

                # print (self.quiz_sets[slide_number].questions[i]['note_pos'])
                # print(self.quiz_sets[slide_number].questions[i]['note_size'])

                self.notes[i].stem.points = self.quiz_sets[slide_number].questions[i]['stem_points']
                self.notes[i].label.pos = self.quiz_sets[slide_number].questions[i]['label_pos']
                self.notes[i].label.size = self.quiz_sets[slide_number].questions[i]['label_size']

                self.notes[i].label.outline_width = 2
                self.notes[i].label.text = self.quiz_sets[slide_number].questions[i]['label_text']
                if is_correct:
                    self.notes[i].label.color = (0.3, 1, 0.4, 0.9)
                else:
                    self.notes[i].label.color = (1, 0, 0, 0.9)

                # if is_corrrect:
                # #print()
                # self.notes[i].rect_green.points = self.quiz_sets[slide_number].notes[i].rect_green.points
                # self.notes[i].rect_green.width = 2 #self.quiz_sets[slide_number].notes[i].rect_green.width
                # else:
                # #print()
                # self.notes[i].rect_red.points = self.quiz_sets[slide_number].notes[i].rect_red.points
                # self.notes[i].rect_red.width = 2 #self.quiz_sets[slide_number].notes[i].rect_red.width

                num = self.quiz_sets[slide_number].questions[i]['num_of_ledger']
                # self.note_ledger.points = [x - x_val_1, y + (s_y / 2), x + x_val_2, y + (s_y / 2)]
                for k in range(num):
                    self.notes[i].note_ledger[k].points = self.quiz_sets[slide_number].questions[i]['ledger_point'][k]


        except IndexError:
            print("Index out of range. Cannot access self.notes[i]")
        self.open_quizset(slide_number)

    def on_size(self, *args):
        # print("On on_size size  W:" + str(self.width) + " H:" + str(self.height))
        # self.start_x = self.width/2
        # self.height = self.height * 0.75
        # self.length_staff = self.width * 0.8

        # placing the logic here as we need to set the notes selected once after the selection is made, so cannot do in __init method.
        # self.notes_selection_for_sight_reader()
        # self.update_staff_lines(0)

        app = MDApp.get_running_app()
        self.current_slide = app.g_quiz_sets_current_slide
        self.init_size_values()
        #self.update_staff_lines(self.current_slide)

    def init_review(self, quiz_sets, slide_number):
        app = MDApp.get_running_app()
        self.quiz_sets = quiz_sets
        self.current_slide = app.g_quiz_sets_current_slide

    def reset_staff(self):
        self.notes = [None] * self.NUMBER_OF_NOTES

    def open_quizset(self):
        for q in self.quiz_sets:
            try:
                print(q.print_data())
            except Exception as e:
                print("Error:", e)

        try:
            print(self.quiz_sets[0].print_data())
        except Exception as e:
            print("Error:", e)

    def open_quizset(self, i):

        try:
            print(self.quiz_sets[i].print_data())
        except Exception as e:
            print("Error:", e)
