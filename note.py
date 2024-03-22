from kivy.animation import Animation
from kivy.core.image import Image as CoreImage
from kivy.graphics import Line, Color, Ellipse
from kivy.uix.button import Button
from kivy.uix.label import Label


class Note(Ellipse):
    note_pos = None
    note_pos_temp = None
    note_size = None
    stem = None
    # stem_line_width = 1.2
    # ledger_line_width = 1.2
    stem_line_width = 2
    ledger_line_width = 1.5
    label = None
    rect_gray = None
    rect_green = None
    rect_red = None
    note_value = None
    note_staff_line_nbr = 0  # used to see which line the note is in, which determines if the stem goes up or down.
    note_ledger = []
    num_of_ledger = 0
    note_show = False
    label_pos = (0, 0)  # need this for review. as label.pos seems to be pass by reference.

    def reset_note(self):

        self.rect_gray.rounded_rectangle = (0, 0, 0, 0, 20, 50)
        self.rect_green.rounded_rectangle = (0, 0, 0, 0, 20, 50)
        self.rect_red.rounded_rectangle = (0, 0, 0, 0, 20, 50)
        self.note_pos = (0, 0)
        self.note_pos_temp = (0, 0)
        self.note_size = (0, 0)
        self.note_value = ''
        self.stem.points = [0, 100, 2, 100]
        self.label.outline_width = 0
        self.label_pos = (0, 0)
        for x in range(4):
            self.note_ledger[x].points = [0, 0, 0, 0]
        self.num_of_ledger = 0
        self.note_show = False

        # Load an image and convert it to a texture
        # image_path = 'tex_note.png'
        # self.texture = CoreImage(image_path).texture

    def __init__(self, pos, size, mode='default', ** kwargs):
        super().__init__(pos=pos, size=size, **kwargs)
        # Add any additional initialization code here

        Color(1, 1, 1, 1)  # white color
        # Load an image and convert it to a texture
        image_path = 'images/tex_note.png'
        image_path_2 = 'images/tex_note_white_2.png'  # for timer mode

        if mode == 'timer':
            self.texture = CoreImage(image_path_2).texture
        else:
            self.texture = CoreImage(image_path).texture

        self.note_pos = pos
        self.note_pos_temp = pos
        self.note_size = size
        if mode == 'timer':
            self.stem_color = Color(1, 1, 1, 0.7)  # Black color  # Initial color for the line
            self.stem_color
        else:
            self.stem_color = Color(0, 0, 0, 0.7)  # Black color  # Initial color for the line
            self.stem_color
        self.stem = Line(points=[0, 100, 2, 100], width=self.stem_line_width)
        self.label = Label(font_size=40,
                           pos=(0, 0), size_hint=(None, None), size=(0, 0), outline_color=(0, 0, 0, 1))
        self.label_pos = (0, 0)
        # Color(0.6, 0.6, 0.6, 1)  # gray color
        Color(0.8, 0.8, 0.8, 1)  # Yellow
        self.rect_gray = Line(rounded_rectangle=(0, 0, 0, 0, 20, 50), width=0)

        Color(0, 0.9, 0.3, 0.7)  # Green color
        self.rect_green = Line(rounded_rectangle=(0, 0, 0, 0, 20, 50), width=0)
        Color(1, 0, 0, 1)  # gray color
        self.rect_red = Line(rounded_rectangle=(0, 0, 0, 0, 20, 50), width=0)
        if mode == 'timer':
            Color(1, 1, 1, 0.7) #white
        else:
            Color(0, 0, 0, 0.3) #Black

        self.note_ledger = [None] * 4  # we allow only 4 ledgers in this sight reader, hence 4 hardcoded.
        for x in range(4):
            self.note_ledger[x] = Line(points=[0, 0, 0, 0], width=self.ledger_line_width)
        self.num_of_ledger = 0
        # Color(1, 1, 1, 1)  # White color
        Color(1, 0, 0, 0.2)  # Set color to red

        # button transparent- for button animation
        self.button_anim = Button(pos=self.pos, background_color=(0, 0, 0, 0))
        self.key_num = 0

    def set_stem(self, y):
        # [self.note_1_pos_x + self.note_size[0], self.y1 + (self.y1 * 0.016),self.note_1_pos_x + self.note_size[0], self.y1 + (self.y1 * 0.12)]
        # print("self.note_pos[0]==" + str(self.note_size[0]))
        stem_line_start_x_factor = 3  # with the line iwdth increase, the line shoud fget inside the note head to look good.
        if self.note_staff_line_nbr <= 3:
            # self.stem.points = [self.pos[0] + self.size[0], y + (y * 0.016),
            # self.pos[0] + self.size[0], y + (y * 0.13)]
            self.stem.points = [self.pos[0] + self.size[0] - stem_line_start_x_factor, y + (y * 0.025),
                                self.pos[0] + self.size[0] - stem_line_start_x_factor, y + (y * 0.2)]
        else:
            # self.stem.points = [self.pos[0], y + (y * 0.016),
            # self.pos[0], y - (y * 0.09)]
            self.stem.points = [self.pos[0] + stem_line_start_x_factor, y + (y * 0.018),
                                self.pos[0] + stem_line_start_x_factor, y - (y * 0.17)]

    def set_label(self, note_name_txt, y):
        # self.label.text = note_name_txt  # 'F'
        self.label.pos = (self.pos[0], y - (y * .09))
        self.label.size = self.size
        self.label.color = (0, 1, 0, 1)
        self.label.outline_color = (0, 0, 0, 1)
        self.label.outline_width = 2
        self.label_pos = (self.pos[0], y - (y * .09))

    # pos = 1 above the fifth staff line(like A), -1 below the first staff line ( like middle C).
    def set_ledger(self, num, pos, staff_line_y, distance_between_lines):
        x = self.pos[0]
        y = self.pos[1]
        s_x = self.size[0]
        s_y = self.size[1]
        x_val_1 = s_x * 0.357  # s_x * 0.357 making this so that we get right measurement for all screen size or note sizes. This value is 10 for 800x60
        x_val_2 = s_x * 1.388  # s_x * 1.388 making this so that we get right measurement for all screen size or note sizes. This value is 40 for 800x60
        # print("self.pos[0]=" + str(x))
        # print("Y=" + str(y))
        # print("s_y=" + str(s_y))
        # print("s_x=" + str(s_x))
        self.num_of_ledger = num
        # self.note_ledger.points = [x - x_val_1, y + (s_y / 2), x + x_val_2, y + (s_y / 2)]
        for i in range(num):
            j = i + 1  # doing x+1 to avoid multiplication by 0, we need the distance to double for each ledger.
            if pos == -1:
                y_val = staff_line_y - (distance_between_lines * j)
            else:
                y_val = staff_line_y + (distance_between_lines * j)
            # print("y_val=" + str(y_val))
            # print("x=" + str(x))
            # print("x - x_val_1=" + str(x - x_val_1))
            self.note_ledger[i].points = [x - x_val_1, y_val, x + x_val_2, y_val]

    def set_rect(self, distance_between_lines, color_code='GRAY'):
        # self.pos[1] * 4 multiply by 4 to take the bounding rectangle so high
        x1 = self.label.pos[0] - 10
        y1 = self.label.pos[1] - 15
        x2 = self.size[0] + 20
        y2 = self.pos[1] + distance_between_lines * 4 - self.label.pos[1] + 20
        y3 = y2 - y1

        if self.note_staff_line_nbr > 3:  # If ledger line is facing down.
            x1 = self.label.pos[0] - 10
            y1 = self.label.pos[1] - 50
            x2 = self.size[0] + 20
            y2 = y1 + y3 + 20

        rectangle_width = 1
        rectangle_width_green = 3

        self.button_anim.pos = (x1, y1)
        self.button_anim.size = (x2, y2)

        anim = Animation(width=3, duration=0.6)
        if color_code == 'GRAY':
            self.rect_gray.rounded_rectangle = (
                x1, y1, x2, y2, 20, 50)
            self.rect_gray.width = rectangle_width
            w = x2 - x1
            h = y2 - y1
            anim += Animation(width=rectangle_width)
            anim.repeat = True
            anim.start(self.rect_gray)

        elif color_code == 'GREEN':
            self.rect_green.rounded_rectangle = (
                x1, y1, x2, y2, 10, 40)
            self.rect_green.width = rectangle_width_green
            self.rect_gray.rounded_rectangle = (
                0, 0, 0, 0, 1, 1)
            self.rect_gray.width = 0.1
            self.rect_red.rounded_rectangle = (
                0, 0, 0, 0, 1, 1)
            self.rect_red.width = 0.1
        else:
            self.rect_red.rounded_rectangle = (
                x1, y1, x2, y2, 20, 50)
            self.rect_red.width = rectangle_width
            self.rect_gray.rounded_rectangle = (
                0, 0, 0, 0, 1, 1)
            self.rect_gray.width = 0.1
            self.rect_green.rounded_rectangle = (
                0, 0, 0, 0, 1, 1)
            self.rect_green.width = 0.1
