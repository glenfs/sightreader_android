import json

from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from kivy.core.text import LabelBase
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition, SlideTransition

from kivymd.app import MDApp
from kivymd.theming import ThemeManager
from kivymd.uix.button import MDIconButton, MDExtendedFabButtonIcon, MDButton, MDButtonIcon, MDButtonText
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.screen import MDScreen

from menu_v2 import SightReaderMenu
from settingsscreen import SettingsScreen

# Import time module
import time

import os, sys
# from kivy.resources import resource_add_path, resource_find

from SightReader import MusicStaff
from SightReaderTimer import MusicStaffTimer
from SightReaderEndReview import MusicStaffReview
from utils import StyledLabel


class CustomDropdownMenu(MDDropdownMenu):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Override the default font properties for menu items
        self.text_color = (1, 0, 0, 1)  # Custom text color
        self.font_name = "fonts/Roboto-Thin.ttf"  # Your custom font name
        self.item_height = dp(20)  # Custom item height


class SightReaderScreen(MDScreen):

    def go_to_menu(self):
        app = MDApp.get_running_app()

        app.root.get_screen('sight_reader').ids.staff.cleanup_exit()

        app.root.get_screen('menu').stop_music()
        app.play_bg_music()
        app.reset_app()
        self.manager.current = 'menu'
        app.change_palette(theme='Dark', prim_palette='Cyan')


class SightReaderMenuScreen(MDScreen):
    def on_size(self, *args):
        pass

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "menu"  # Give the screen a name
        self.size = Window.size

        float_layout = FloatLayout()
        start_button =  MDButton(
            MDButtonIcon(icon="music"),
            MDButtonText(
                text="start",font_name="littledays",font_size=dp(22),text_color="FE5BAC", theme_font_size='Custom',theme_font_name='Custom',theme_text_color='Custom'
            ),
            style='text',
        )
        # start_button = MDExtendedFabButtonIcon(
        #     icon="music-note",
        #     line_color=(0, 0, 0, 0),
        #     text='Start',  # halign="right",
        #     font_name="littledays",
        #     font_size=dp(18),
        #     text_color="FE5BAC",
        # )
        start_button.pos_hint = {"center_x": 0.85, "center_y": 0.5}
        start_button.size_hint = (0.1, 0.1)
        start_button.bind(on_release=self.go_to_sight_reader)

        # start_timer_button = MDExtendedFabButtonIcon(
        #     icon="music-note",
        #     line_color=(0, 0, 0, 0),
        #     text='Timer mode',  # halign="center",
        #     font_name="littledays",
        #     font_size=dp(18),
        #     text_color="FE5BAC",
        # )
        start_timer_button = MDButton(
            MDButtonIcon(icon="music"),
            MDButtonText(
                text="Timer mode",font_name="littledays",font_size=dp(22),text_color="FE5BAC",theme_font_size='Custom',theme_font_name='Custom',theme_text_color='Custom'
            ),
            style='text',
        )
        start_timer_button.pos_hint = {"center_x": 0.85, "center_y": 0.4}
        start_timer_button.size_hint = (0.1, 0.1)
        #start_timer_button.bind(on_release=self.go_to_sight_reader_timer_mode)
        start_timer_button.bind(on_release=self.go_countdown_screen)


        # options_button = MDExtendedFabButtonIcon(
        #     icon="wrench",
        #     line_color=(0, 0, 0, 0),
        #     text='Advanced options',
        #     font_name="littledays",
        #     font_size=11,
        #     text_color="FE5BAC",
        # )
        # options_button.pos_hint = {"center_x": 0.75, "center_y": 0.35}
        # float_layout.add_widget(options_button)

        main_layout = GridLayout(cols=1, rows=2, padding=dp(5), spacing=dp(8), size_hint_y=1, size_hint_x=1,
                                 pos_hint={"center_x": 0.5, "center_y": 0.2}
                                 )

        main_layout.size_hint = (1, 1)
        # main_layout.pos_hint = {"center_x": 0.5, "center_y": 0.5}

        scroll_view = SightReaderMenu()
        # scroll_view.opacity = 0.7
        # self.add_widget(scroll_view)

        top_app_bar = Label(text='Sight Reader Expert', font_name="littledays",  # font_size='36sp',
                            bold=True,
                            color='66ffff'  # , #size_hint_y=None, #height=dp(40)
                            )
        top_app_bar.size_hint_y = 0.1
        # main_layout.add_widget(top_app_bar)

        # diff_layout = GridLayout(cols=6, spacing=1, padding=2)
        # diff_layout.size_hint_y = 0.1
        # diff_layout.add_widget(Label(text="Easy", font_name="littledays"))
        # checkbox1 = CheckBox(active=False, group='diff')
        # diff_layout.add_widget(checkbox1)
        # diff_layout.add_widget(Label(text="Medium", font_name="littledays"))
        # checkbox2 = CheckBox(active=False, group='diff')
        # diff_layout.add_widget(checkbox2)
        # diff_layout.add_widget(Label(text="Hard", font_name="littledays"))
        # checkbox3 = CheckBox(active=False, group='diff')
        # diff_layout.add_widget(checkbox3)

        # float_layout.add_widget(diff_layout)
        scroll_view.size_hint_y = 0.9
        main_layout.add_widget(scroll_view)

        self.pos_hint = {"x": 0, "y": 0.3}
        self.add_widget(main_layout)
        float_layout.add_widget(start_button)
        float_layout.add_widget(start_timer_button)

        self.add_widget(float_layout)

        menu_button = MDIconButton(
            icon="menu",  # Set the icon
            on_release=self.open_menu,  # Define the on_release event handler # Define the on_release event handler

        )
        menu_button.pos_hint = {'x': 0.05, 'top': 0.70}
        #self.add_widget(menu_button)

        self.bg_music_2 = SoundLoader.load('sounds/bach-minuet.mp3')
        self.bg_music = SoundLoader.load('sounds/jazzy-161990.mp3')

        # Define menu options
        menu_items = [
            {"text": "options", "viewclass": "OneLineIconListItem",
             "on_release": self.on_settings},
        ]

        # Create the dropdown menu
        # app = MDApp.get_running_app()
        self.menu = CustomDropdownMenu(
            caller=menu_button,
            items=menu_items,
            width_mult=3,
            background_color='#FE5BAC',  # (1, 1, 1, 1),  # Example background color
            border_margin=10,  # Example border margin
            device_ios=False,  # Example iOS device style
            hor_growth='left',  # Example horizontal growth- Must be one of: ['left', 'right']
            max_height=dp(200),  # Example maximum height
            opacity=0.5,  # Example opacity
            #opening_transition='out_quad',  # Example opening transition
            position='auto',  # Example position
            radius=[7, 7, 7, 7],  # Example radius
            # theme_cls=app.theme_cls,  # Example theme class
            #widget_style='ios',  # Example widget style Must be one of: ['android', 'ios', 'desktop']
        )
        print("main_layout size=" + str(main_layout.size))
        print("menu screen size=" + str(self.size))

    # Options for 'opening_transition':  in above menu code
    # - in_expo - Accelerating motion. Starts slowly and speeds up as the animation progresses.
    # - in_out_expo  Accelerating motion at the beginning and decelerating motion at the end.
    # - out_expo Decelerating motion. Starts quickly and slows down as the animation progresses.
    # - in_quad Accelerating motion.
    # - in_out_quad
    # - out_quad
    # - in_cubic
    # - in_out_cubic
    # - out_cubic
    # - in_sine
    # - in_out_sine
    # - out_sine
    # - in_out_elastic
    # - in_out_back
    def open_menu(self, *args):
        # Open the dropdown menu
        self.menu.open()

    def menu_callback(self, instance):
        print("called menu")

    def go_to_sight_reader(self, instance):
        # for i in range(0, 17):
        app = MDApp.get_running_app()

        sm = self.manager
        if not (sm.has_screen('sight_reader')):
            sm.add_widget(SightReaderScreen(name='sight_reader'))
            app.root.get_screen('sight_reader').md_bg_color = 'white'

        if not (sm.has_screen('end_screen')):
            sm.add_widget(EndScreen(name='end_screen'))
        if not (sm.has_screen('review_screen')):
            sm.add_widget(SightReaderEndReviewScreen(name='review_screen'))

        app.stop_bg_music()
        self.play_music()
        app.reset_app()
        self.manager.current = 'sight_reader'
        app.change_palette(theme='Light', prim_palette='Aliceblue')

        # print(app.g_quiz_sets_current_slide)
        app.root.get_screen('sight_reader').ids.staff.notes_selection_for_sight_reader()
        app.root.get_screen('end_screen').reset_quiz_sets()
        app.root.get_screen('sight_reader').ids.staff.new_game_init()
        app.root.get_screen('sight_reader').ids.staff.reset_staff_show_next()

    def go_countdown_screen(self, instance):
        app = MDApp.get_running_app()

        sm = self.manager
        if not (sm.has_screen('count_down_screen')):
            sm.add_widget(CountdownScreen(name='count_down_screen'))

        app.root.get_screen('count_down_screen').initiate_countdown()
        self.manager.current = 'count_down_screen'


    def go_to_sight_reader_timer_mode(self):
        # for i in range(0, 17):
        app = MDApp.get_running_app()

        sm = self.manager
        if not (sm.has_screen('sight_reader_timer')):
            sm.add_widget(SightReaderTimerScreen(name='sight_reader_timer'))
        if not (sm.has_screen('end_screen_timer')):
            sm.add_widget(EndScreenTimer(name='end_screen_timer'))

        app.stop_bg_music()
        self.play_music_timer()
        app.reset_app()
        self.manager.current = 'sight_reader_timer'
        app.change_palette(theme='Dark', prim_palette='Darkgoldenrod')
        app.root.get_screen('sight_reader_timer').reset_timer()
        app.root.get_screen('sight_reader_timer').ids.staff.notes_selection_for_sight_reader()
        app.root.get_screen('sight_reader_timer').ids.staff.new_game_init()
        app.root.get_screen('sight_reader_timer').ids.staff.reset_staff_show_next()

    def on_settings(self):
        # print("settings called")
        app = MDApp.get_running_app()

        sm = self.manager
        if not (sm.has_screen('settings')):
            sm.add_widget(SettingsScreen(name='settings'))

        app.stop_bg_music()
        self.manager.current = 'settings'
        app.change_palette(theme='Dark', prim_palette='BlueGray')

    def play_music(self):
        self.bg_music_2.volume = 0.3
        self.bg_music_2.loop = True
        self.bg_music_2.play()

    def play_music_timer(self):
        self.bg_music.volume = 0.3
        self.bg_music.play()

    def stop_music(self):
        self.bg_music_2.stop()

    def stop_music_timer(self):
        self.bg_music.stop()


class CountdownScreen(MDScreen):
    def __init__(self, **kwargs):
        super(CountdownScreen, self).__init__(**kwargs)
        self.countdown_timer = 3
        self.name = kwargs.get('name', 'count_down_screen')
        self.label = Label(text='', font_size=dp(150), font_name="littledays")
        self.add_widget(self.label)

    def initiate_countdown(self):
        self.label.text = ''
        self.countdown_timer = 3
        self.start_countdown()

    def start_countdown(self):
        Clock.schedule_interval(self.update_countdown, 1)

    def update_countdown(self, dt):
        if self.countdown_timer > 0:
            self.label.text = str(self.countdown_timer)
            self.countdown_timer -= 1
        else:
            self.label.text = "Go..."
            Clock.schedule_once(self.transition_to_next_screen, 1)
            return False  # Stop the Clock schedule

    def transition_to_next_screen(self, dt):
        app = MDApp.get_running_app()
        app.root.get_screen('menu').go_to_sight_reader_timer_mode()


class EndScreen(MDScreen):
    quiz_sets = []

    def set_correct_answers(self, num_of_correct):
        self.ids.correct_answers.text = str(num_of_correct)

    def set_wrong_answers(self, num_of_wrong):
        self.ids.wrong_answers.text = str(num_of_wrong)

    def set_result_motivation(self, result_motivation_message):
        self.ids.result_motivation.text = result_motivation_message

    def reset_quiz_sets(self):
        self.quiz_sets = []

    def set_session_review_questions(self, review_question_list_set):
        app = MDApp.get_running_app()
        # print(len(review_question_list_set))
        self.quiz_sets = review_question_list_set
        # app.g_quiz_sets = self.quiz_sets # we are setting this in the SightReader Gameover method.
        app.g_quiz_sets_current_slide = 0

    def go_to_review_screen(self):
        app = MDApp.get_running_app()
        app.stop_bg_music()

        app.change_palette(theme='Light', prim_palette='Aquamarine')

        # Reset the slide to 0
        app.g_quiz_sets_current_slide = 0
        app.root.get_screen('review_screen').md_bg_color = 'white'
        app.root.get_screen('review_screen').ids.staff_review.init_review(app.g_quiz_sets,
                                                                          0)  # pass zero for current slide, first slide is always 0.
        # app.root.get_screen('review_screen').ids.staff_review.reset_staff_show_next()
        app.root.get_screen('review_screen').ids.staff_review.create_staff_lines(0)
        app.root.get_screen('review_screen').ids.staff_review.update_staff_lines(0)

        # For the first review we are showing the first quiz so the Prev will be disabled. Next button is enabled, as it could have been disabled in the previous session.
        app.root.get_screen('review_screen').ids.next_review.disabled = False
        app.root.get_screen('review_screen').ids.prev_review.disabled = True
        self.manager.current = 'review_screen'

    def go_to_menu(self):
        app = MDApp.get_running_app()

        app.root.get_screen('menu').stop_music()
        app.play_bg_music()
        app.reset_app()
        self.manager.current = 'menu'
        app.change_palette(theme='Dark', prim_palette='Cyan')

    def play_again(self):
        app = MDApp.get_running_app()
        app.root.get_screen('menu').go_to_sight_reader(self)


def set_new_highscore(score):
    # Load existing JSON data from the file
    try:
        with open("settings.json", "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        data = {}  # Create an empty dictionary if the file doesn't exist

    # Update the specific value
    try:
        # Update num_sets and save to settings.json
        score_int = int(score)
        app = MDApp.get_running_app()
        app.g_timer_highscore = score_int
        data["highScoreTimer"] = score_int
        # print("app.g_number_of_slide" + str(app.g_number_of_slide))
        with open("settings.json", "w") as f:
            json.dump(data, f)
    except ValueError:
        pass


class EndScreenTimer(MDScreen):
    def set_correct_answers(self, num_of_correct):
        self.ids.correct_answers.text = str(num_of_correct)

    def set_score(self, score):
        app = MDApp.get_running_app()
        high_score = app.g_timer_highscore

        if score > high_score and app.g_timer_secs <= 20:
            set_new_highscore(score)
            self.ids.total_score.text = str(score)
            self.ids.comments.text = '[color=FF407D]New Record!!!\nPrevious high was ' + str(
                high_score) + '[/color]'
            self.ids.high_score.text = str(score)
        else:
            self.ids.total_score.text = str(score)
            self.ids.high_score.text = str(high_score)

    def set_result_motivation(self, result_motivation_message):
        self.ids.result_motivation.text = result_motivation_message

    def go_to_menu(self):
        app = MDApp.get_running_app()

        app.root.get_screen('menu').stop_music_timer()
        app.play_bg_music()
        app.reset_app()
        self.manager.current = 'menu'
        app.change_palette(theme='Dark', prim_palette='Cyan')

    def play_again(self):
        # for i in range(0, 17):
        app = MDApp.get_running_app()
        app.root.get_screen('menu').stop_music_timer()
        app.root.get_screen('menu').go_countdown_screen(self)

        # app.stop_bg_music()
        # self.play_music()
        # app.reset_app()
        # self.manager.current = 'sight_reader_timer'
        # app.change_palette(theme='Light', prim_palette='BlueGray')
        # app.root.get_screen('sight_reader_timer').reset_timer()
        # app.root.get_screen('sight_reader_timer').ids.staff.notes_selection_for_sight_reader()
        # app.root.get_screen('sight_reader_timer').ids.staff.new_game_init()
        # app.root.get_screen('sight_reader_timer').ids.staff.reset_staff_show_next()

    def play_music(self):
        app = MDApp.get_running_app()
        app.root.get_screen('menu').stop_music()
        app.root.get_screen('menu').play_music()
        # app.play_bg_music()


class SightReaderEndReviewScreen(MDScreen):
    def show_next_set(self):
        app = MDApp.get_running_app()
        app.g_quiz_sets_current_slide = app.g_quiz_sets_current_slide + 1

        # print("app.g_quiz_sets_current_slide=" + str(app.g_quiz_sets_current_slide))

        if app.g_quiz_sets_current_slide + 1 >= app.g_number_of_slide:
            app.root.get_screen('review_screen').ids.next_review.disabled = True
        if app.g_quiz_sets_current_slide > 0:
            app.root.get_screen('review_screen').ids.prev_review.disabled = False

        app.root.get_screen('review_screen').ids.staff_review.show_next_set(app.g_quiz_sets)

        # app = MDApp.get_running_app()
        app.stop_bg_music()

    def show_prev_set(self):
        app = MDApp.get_running_app()
        app.g_quiz_sets_current_slide = app.g_quiz_sets_current_slide - 1
        # print("app.g_quiz_sets_current_slide=" + str(app.g_quiz_sets_current_slide))
        if app.g_quiz_sets_current_slide <= 0:
            app.root.get_screen('review_screen').ids.prev_review.disabled = True
        if app.g_quiz_sets_current_slide + 1 <= app.g_number_of_slide - 1:
            app.root.get_screen('review_screen').ids.next_review.disabled = False

        app.root.get_screen('review_screen').ids.staff_review.show_prev_set(app.g_quiz_sets)

        app = MDApp.get_running_app()
        app.stop_bg_music()

    def go_to_menu(self):
        app = MDApp.get_running_app()

        app.root.get_screen('menu').stop_music()
        app.play_bg_music()
        app.reset_app()
        self.manager.current = 'menu'
        app.change_palette(theme='Dark', prim_palette='Cyan')


class SightReaderTimerScreen(MDScreen):
    timer = 10  # default

    def __init__(self, **kwargs):
        app = MDApp.get_running_app()
        super().__init__(**kwargs)
        self.timer = app.g_timer_secs
        # Clock.schedule_interval(self.update_timer, 1)

    def reset_timer(self):
        app = MDApp.get_running_app()
        self.timer = app.g_timer_secs
        Clock.schedule_interval(self.update_timer, 1)

    def update_timer(self, dt):
        # print("Update Timer called to schedule")
        app = MDApp.get_running_app()

        self.timer -= 1
        app.root.get_screen('sight_reader_timer').ids.timer_label.text = f'{self.timer}'
        if self.timer == 5:
            app.play_ticker_music()

        if self.timer == 0:
            app.stop_ticker_music()
            app.play_ticker_end_music()
            # app.root.get_screen('menu').stop_music()
            app.root.get_screen('sight_reader_timer').ids.timer_label.text = '0'
            Clock.unschedule(self.update_timer)  # Stop the timer
            app.root.get_screen('sight_reader_timer').ids.staff.game_over()

    def cleanup_on_exit(self):
        app = MDApp.get_running_app()
        Clock.unschedule(self.update_timer)  # Stop the timer
        app.root.get_screen('sight_reader_timer').ids.staff.cleanup_on_exit()
        self.timer = 10
        app.root.get_screen('sight_reader_timer').ids.timer_label.text = ''
        app.root.get_screen('sight_reader_timer').ids.score.text = ''
        app.stop_ticker_music()

    def go_to_menu(self):
        app = MDApp.get_running_app()
        self.cleanup_on_exit()

        app.root.get_screen('menu').stop_music_timer()
        app.stop_bg_music()
        app.play_bg_music()
        app.reset_app()
        self.manager.current = 'menu'
        app.change_palette(theme='Dark', prim_palette='Cyan')


class SightReaderApp(MDApp):
    sm = None
    score = 0
    bg_music = None
    ticker_music = None
    ticker_end_music = None

    notes_selection_menu_Treble = [False, False, False, False, False, False, False, False, False, False, False, False,
                                   False,
                                   False, False, False, False, False, False, False, False, False, False, False, False,
                                   False, False, False, False]
    notes_selection_menu_Bass = [False, False, False, False, False, False, False, False, False, False, False, False,
                                 False,
                                 False, False, False, False, False, False, False, False, False, False, False, False,
                                 False, False, False, False]

    notes_selection_menu = [False, False, False, False, False, False, False, False, False, False, False, False,
                            False,
                            False, True, True, True, True, True, False, False, False, False, False, False,
                            False, False, False, False]

    clef_selected = "Treble"
    difficulty_selected = "Beginner"
    g_quiz_sets = None
    g_quiz_sets_current_slide = 0
    g_number_of_slide = 5
    g_timer_secs = 20
    g_timer_highscore = 0

    # Load value from settings.json file
    try:
        with open("settings.json", "r") as f:
            data = json.load(f)
            g_number_of_slide = data.get("numOfSets", 5)
            g_timer_secs = data.get("timerSecs", 20)
            g_timer_highscore = data.get("highScoreTimer", 0)
    except FileNotFoundError:
        pass

    def update_clef(self, clef):
        self.clef_selected = clef

    def update_difficulty(self, diff):
        self.difficulty_selected = diff

    def get_clef(self):
        return self.clef_selected

    def get_difficulty(self):
        return self.difficulty_selected

    def change_palette(self, theme='Light', prim_palette='Cyan'):
        self.theme_cls.theme_style = theme
        self.theme_cls.primary_palette = prim_palette

    def on_start(self):
        # print("on start")
        # Delay time for splash screen before transitioning to main screen
        Clock.schedule_once(self.spash_screen, 1.5)  # Delay for 10 seconds
        self.play_bg_music()

    def spash_screen(self, dt):
        self.sm.current = "menu"

    def on_stop(self):
        self.bg_music.stop()
        self.bg_music.unload()

    def play_bg_music(self):
        self.bg_music.volume = 0.3
        self.bg_music.play()

    def stop_bg_music(self):
        self.bg_music.stop()

    def play_ticker_music(self):
        self.ticker_music.volume = 0.3
        self.ticker_music.play()

    def stop_ticker_music(self):
        self.ticker_music.stop()

    def play_ticker_end_music(self):
        self.ticker_end_music.volume = 0.3
        self.ticker_end_music.play()

    def reset_app(self):
        self.g_quiz_sets_current_slide = 0
        self.g_quiz_sets = None

    def called(self):
        print("tets")

    def build(self):
        # record start time
        #print("record start time")
        #start = time.time()

        self.sm = ScreenManager(transition=NoTransition())
        # Clock.max_iteration = 100
        self.icon = 'images/music.png'
        self.theme_cls = ThemeManager()
        self.theme_cls.theme_style = "Dark"  # Options: "Light" or "Dark"
        self.theme_cls.primary_palette = "Aquamarine"  # Options: "Red", "Pink", "Purple", "DeepPurple", "Indigo", "Blue", "LightBlue", "Cyan", "Teal", "Green", "LightGreen", "Lime", "Yellow", "Amber", "Orange", "DeepOrange", "Brown", "Gray", "BlueGray"

        Builder.load_file('SightReader.kv')

        # Register custom fonts
        LabelBase.register(name="littledays",
                           fn_regular="fonts/Basic Comical Regular NC.ttf",
                           fn_bold="fonts/Basic Comical Regular NC.ttf")

        # sm.transition = MDTransitionStack()
        # Set the transition effect
        #self.sm.transition = SlideTransition()
        self.sm.add_widget((Builder.load_file("splashScreen.kv")))
        self.sm.add_widget(SightReaderMenuScreen(name='menu'))
        # sm.add_widget(SightReaderScreen(name='sight_reader'))
        # sm.add_widget(SettingsScreen(name='settings'))
        # sm.add_widget(EndScreen(name='end_screen'))
        # sm.add_widget(SightReaderEndReviewScreen(name='review_screen'))
        # sm.add_widget(SightReaderTimerScreen(name='sight_reader_timer'))
        # sm.add_widget(EndScreenTimer(name='end_screen_timer'))

        # Set the initial screen (MenuScreen) as the current screen
        self.sm.current = "SplashScreen"
        self.bg_music = SoundLoader.load('sounds/soft-openin.mp3')
        self.ticker_music = SoundLoader.load('sounds/ticker.wav')
        self.ticker_end_music = SoundLoader.load('sounds/ticker_end.wav')

        # record end time
        #end = time.time()
        # print the difference between start
        # and end time in milli. secs
        #print("The time of execution of above program is :",
              #(end - start) * 10 ** 3, "ms")

        return self.sm


if __name__ == '__main__':
    # Window.clearcolor = (0.9, 0.9, 0.89, 1)
    # Window.orientation = 'auto'
    # Window.size = (1080, 1920) # Set window size
    # Window.size = (500, 300)  # Set window size
    # Window.size = (600, 1000) # Set window size
    # if hasattr(sys, '_MEIPASS'):
    # resource_add_path(os.path.join(sys._MEIPASS))
    SightReaderApp().run()
