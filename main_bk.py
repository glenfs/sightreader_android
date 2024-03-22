import json

from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from kivy.core.text import LabelBase
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import ScreenManager, Screen

from kivymd.app import MDApp
from kivymd.theming import ThemeManager
from kivymd.uix.button import MDRoundFlatIconButton


from menu_v2 import SightReaderMenu
from settingsscreen import SettingsScreen
import os, sys
from kivy.resources import resource_add_path, resource_find

from SightReader import MusicStaff
from SightReaderTimer import MusicStaffTimer
from SightReaderEndReview import MusicStaffReview
from utils import StyledLabel

class SightReaderScreen(Screen):
    def go_to_menu(self):
        app = MDApp.get_running_app()

        app.root.get_screen('sight_reader').ids.staff.cleanup_exit()

        app.root.get_screen('menu').stop_music()
        app.play_bg_music()
        app.reset_app()
        self.manager.current = 'menu'
        app.change_palette(theme='Dark', prim_palette='Cyan')


class SightReaderMenuScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "menu"  # Give the screen a name

        float_layout = FloatLayout()

        scroll_view = SightReaderMenu()
        # float_layout.add_widget(grid_layout)

        # Create Start button
        start_button = MDRoundFlatIconButton(
            icon="music-note",
            text='Start', halign="center",
            font_name="littledays",
            font_size=17,
            text_color="FE5BAC"
        )

        # Create Start timer button
        start_timer_button = MDRoundFlatIconButton(
            icon="music-note",
            text='Timer mode', halign="center",
            font_name="littledays",
            font_size=17,
            text_color="FE5BAC"
        )
        self.add_widget(scroll_view)

        # start_button = MDFillRoundFlatButton(text="Start", halign="center")
        start_button.pos_hint = {"center_x": 0.9, "center_y": 0.85}
        start_button.size_hint_x = dp(0.18)
        start_button.bind(on_release=self.go_to_sight_reader)

        # start_button = MDFillRoundFlatButton(text="Start", halign="center")
        start_timer_button.pos_hint = {"center_x": 0.9, "center_y": 0.78}
        start_timer_button.size_hint_x = dp(0.18)
        start_timer_button.bind(on_release=self.go_to_sight_reader_timer_mode)

        float_layout.add_widget(start_button)
        float_layout.add_widget(start_timer_button)

        options_button = MDRoundFlatIconButton(
            icon="wrench",
            text='Advanced options', size_hint_y=None, height=dp(40),
            font_name="littledays",
            font_size=17,
            text_color="FE5BAC"
        )
        options_button.pos_hint = {"x": 0.05, "center_y": 0.85}
        options_button.bind(on_release=self.on_settings)
        float_layout.add_widget(options_button)

        self.add_widget(float_layout)
        self.bg_music = SoundLoader.load('sounds/jazzy-161990.mp3')



    def go_to_sight_reader(self, instance):
        # for i in range(0, 17):
        app = MDApp.get_running_app()

        app.stop_bg_music()
        self.play_music()
        app.reset_app()
        self.manager.current = 'sight_reader'
        app.change_palette(theme='Light', prim_palette='BlueGray')
        app.root.get_screen('sight_reader').ids.staff.notes_selection_for_sight_reader()

        app.root.get_screen('end_screen').reset_quiz_sets()
        app.root.get_screen('sight_reader').ids.staff.new_game_init()
        app.root.get_screen('sight_reader').ids.staff.reset_staff_show_next()

    def go_to_sight_reader_timer_mode(self, instance):
        # for i in range(0, 17):
        app = MDApp.get_running_app()

        app.stop_bg_music()
        self.play_music()
        app.reset_app()
        self.manager.current = 'sight_reader_timer'
        app.change_palette(theme='Light', prim_palette='BlueGray')
        app.root.get_screen('sight_reader_timer').reset_timer()
        app.root.get_screen('sight_reader_timer').ids.staff.notes_selection_for_sight_reader()
        app.root.get_screen('sight_reader_timer').ids.staff.new_game_init()
        app.root.get_screen('sight_reader_timer').ids.staff.reset_staff_show_next()

    def on_settings(self, instance):
        # print("settings called")
        app = MDApp.get_running_app()
        app.stop_bg_music()
        self.manager.current = 'settings'
        app.change_palette(theme='Dark', prim_palette='BlueGray')

    def play_music(self):
        self.bg_music.volume = 0.15
        self.bg_music.play()

    def stop_music(self):
        self.bg_music.stop()


class EndScreen(Screen):
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
        #print(len(review_question_list_set))
        self.quiz_sets = review_question_list_set
        # app.g_quiz_sets = self.quiz_sets # we are setting this in the SightReader Gameover method.
        app.g_quiz_sets_current_slide = 0

    def go_to_review_screen(self):
        app = MDApp.get_running_app()
        app.stop_bg_music()

        app.change_palette(theme='Light', prim_palette='BlueGray')

        # Reset the slide to 0
        app.g_quiz_sets_current_slide = 0

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


class EndScreenTimer(Screen):
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

        app.root.get_screen('menu').stop_music()
        app.play_bg_music()
        app.reset_app()
        self.manager.current = 'menu'
        app.change_palette(theme='Dark', prim_palette='Cyan')

    def play_again(self):
        # for i in range(0, 17):
        app = MDApp.get_running_app()

        app.stop_bg_music()
        self.play_music()
        app.reset_app()
        self.manager.current = 'sight_reader_timer'
        app.change_palette(theme='Light', prim_palette='BlueGray')
        app.root.get_screen('sight_reader_timer').reset_timer()
        app.root.get_screen('sight_reader_timer').ids.staff.notes_selection_for_sight_reader()
        app.root.get_screen('sight_reader_timer').ids.staff.new_game_init()
        app.root.get_screen('sight_reader_timer').ids.staff.reset_staff_show_next()

    def play_music(self):
        app = MDApp.get_running_app()
        app.root.get_screen('menu').stop_music()
        app.root.get_screen('menu').play_music()
        # app.play_bg_music()


class SightReaderEndReviewScreen(Screen):
    def show_next_set(self):
        app = MDApp.get_running_app()
        app.g_quiz_sets_current_slide = app.g_quiz_sets_current_slide + 1

        #print("app.g_quiz_sets_current_slide=" + str(app.g_quiz_sets_current_slide))

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
        #print("app.g_quiz_sets_current_slide=" + str(app.g_quiz_sets_current_slide))
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


class SightReaderTimerScreen(Screen):
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

        app.root.get_screen('menu').stop_music()
        app.stop_bg_music()
        app.play_bg_music()
        app.reset_app()
        self.manager.current = 'menu'
        app.change_palette(theme='Dark', prim_palette='Cyan')


class SightReaderApp(MDApp):
    global sm
    sm = ScreenManager()
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
    g_timer_secs = 10
    g_timer_highscore = 1000

    # Load value from settings.json file
    try:
        with open("settings.json", "r") as f:
            data = json.load(f)
            g_number_of_slide = data.get("numOfSets", 5)
            g_timer_secs = data.get("timerSecs", 10)
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

    def change_palette(self, theme='Dark', prim_palette='Cyan'):
        self.theme_cls.theme_style = theme
        self.theme_cls.primary_palette = prim_palette

    def on_start(self):
        #print("on start")
        # Delay time for splash screen before transitioning to main screen
        Clock.schedule_once(self.spash_screen, 3)  # Delay for 10 seconds
        self.play_bg_music()

    def spash_screen(self, dt):
        sm.current = "menu"

    def on_stop(self):
        self.bg_music.stop()
        self.bg_music.unload()

    def play_bg_music(self):
        self.bg_music.volume = 0.15
        self.bg_music.play()

    def stop_bg_music(self):
        self.bg_music.stop()

    def play_ticker_music(self):
        self.ticker_music.volume = 0.2
        self.ticker_music.play()

    def stop_ticker_music(self):
        self.ticker_music.stop()

    def play_ticker_end_music(self):
        self.ticker_end_music.volume = 0.1
        self.ticker_end_music.play()

    def reset_app(self):
        self.g_quiz_sets_current_slide = 0
        self.g_quiz_sets = None

    def build(self):
        # Clock.max_iteration = 100
        self.icon = 'images/music.png'
        self.theme_cls = ThemeManager()
        self.theme_cls.theme_style = "Dark"  # Options: "Light" or "Dark"
        self.theme_cls.primary_palette = "Cyan"  # Options: "Red", "Pink", "Purple", "DeepPurple", "Indigo", "Blue", "LightBlue", "Cyan", "Teal", "Green", "LightGreen", "Lime", "Yellow", "Amber", "Orange", "DeepOrange", "Brown", "Gray", "BlueGray"

        # Register custom fonts
        LabelBase.register(name="littledays",
                           fn_regular="fonts/Basic Comical Regular NC.ttf",
                           fn_bold="fonts/Basic Comical Regular NC.ttf")

        # sm.transition = MDTransitionStack()
        sm.add_widget((Builder.load_file("splashScreen.kv")))
        sm.add_widget(SightReaderMenuScreen(name='menu'))
        sm.add_widget(SightReaderScreen(name='sight_reader'))
        sm.add_widget(SettingsScreen(name='settings'))
        sm.add_widget(EndScreen(name='end_screen'))
        sm.add_widget(SightReaderEndReviewScreen(name='review_screen'))
        sm.add_widget(SightReaderTimerScreen(name='sight_reader_timer'))
        sm.add_widget(EndScreenTimer(name='end_screen_timer'))

        # Set the initial screen (MenuScreen) as the current screen
        sm.current = "SplashScreen"
        self.bg_music = SoundLoader.load('sounds/soft-openin.mp3')
        self.ticker_music = SoundLoader.load('sounds/ticker.wav')
        self.ticker_end_music = SoundLoader.load('sounds/ticker_end.wav')
        return sm


if __name__ == '__main__':
    # Window.clearcolor = (0.9, 0.9, 0.89, 1)
    # Window.orientation = 'auto'
    #Window.size = (1080, 1920) # Set window size
    Window.size = (800,600)  # Set window size
    # Window.size = (600, 1000) # Set window size
    if hasattr(sys, '_MEIPASS'):
        resource_add_path(os.path.join(sys._MEIPASS))
    SightReaderApp().run()
