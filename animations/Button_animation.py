from kivy.app import App
from kivy.core.audio import SoundLoader
from kivy.metrics import dp
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, Ellipse
from kivy.animation import Animation
from kivy.core.image import Image as CoreImage
from kivy.uix.label import Label


class AnimationHelper:

    def __init__(self, **kwargs):
        self.correct_answer_sound_1 = SoundLoader.load('sounds/streak.mp3')
        self.correct_answer_sound_1.volume = 0.2
        self.wrong_answer_sound_1 = SoundLoader.load('sounds/wrong_note.mp3')
        self.wrong_answer_sound_1.volume = 0.2

    @staticmethod
    def bind_remove_circle(instance, ellipse):
        return lambda *args: AnimationHelper.remove_circle(instance, ellipse)

    def streak_animation(self, instance, pos, streak_num, score):
        # pos = pos

        updated_pos = (pos[0], pos[1] - 60)
        with instance.canvas.before:
            Color(1, 1, 1)  # Set color to white


            if score > 0:
                ellipse = Ellipse(pos=updated_pos, size=(50, 50))
                image_path = 'images/streak_Green.png'
                t = f'{streak_num} in a row. [color=22ff44]+{score}[/color]'
                self.correct_answer_sound_1.play()
                ellipse.texture = CoreImage(image_path).texture
            else:
                #image_path = 'images/Red_note.png'
                t = f'[color=7f0000] {score}[/color]'
                self.wrong_answer_sound_1.play()

            # Create Label
            label = Label(text=t, font_size=dp(18), pos=updated_pos,
                          opacity=1,
                          color="FC0FC0",
                          font_name="littledays",
                          font_blended=True,
                          markup=True)


        # Animation to move the ellipse up, shrink, and fade out
        if score > 0:
            ellipse_anim = Animation(pos=(ellipse.pos[0], ellipse.pos[1] + 100), size=(15, 15), duration=3)
            ellipse_anim += Animation(size=(0, 0), duration=0.14)
            # ellipse_anim.bind(on_complete=AnimationHelper.remove_circle(instance, ellipse))
            # ellipse_anim.start(ellipse)
            # ellipse_anim.bind(on_complete=AnimationHelper.bind_remove_circle(instance, ellipse))
            ellipse_anim.start(ellipse)

        # Animate Label
        label_anim = Animation(y=label.y + 100, opacity=0, duration=3)
        # label_anim.bind(on_complete=remove_label())
        label_anim.start(label)

    @staticmethod
    def spawn_animation(instance):
        star_size = (13, 13)
        # Get the button position
        button_pos = instance.pos

        # Create a small ellipse
        with instance.canvas.before:
            Color(0, 1, 0, 1)  # Green color
            ellipse = Ellipse(pos=(button_pos[0], button_pos[1] + instance.size[1] / 2), size=star_size)
            ellipse2 = Ellipse(pos=(button_pos[0] + instance.size[0], button_pos[1] + instance.size[1] / 2),
                               size=star_size)
            # ellipse3= Ellipse(pos=(button_pos[0] , button_pos[1] ), size=(10, 10))
            # ellipse4 = Ellipse(pos=(button_pos[0] + instance.size[0], button_pos[1]), size=(10, 10))
            Color(0, 0.6, 0.3, 1)  # Red color
            ellipse5 = Ellipse(pos=(button_pos[0] + instance.size[0] / 2, button_pos[1]), size=star_size)
            ellipse6 = Ellipse(pos=(button_pos[0] + instance.size[0] / 2, button_pos[1] + instance.size[1]),
                               size=star_size)

        # Animation to move the ellipse up, shrink, and fade out
        anim = Animation(pos=(ellipse.pos[0] - 25, ellipse.pos[1]), size=(3, 3), duration=0.25)
        anim += Animation(size=(0, 0), duration=0.16)
        anim2 = Animation(pos=(ellipse2.pos[0] + 25, ellipse2.pos[1]), size=(3, 3), duration=0.25)
        anim2 += Animation(size=(0, 0), duration=0.14)
        # anim3 = Animation(pos=(ellipse3.pos[0] - 10, ellipse3.pos[1] - 25), size=(3, 3), duration=0.25)
        # anim3 += Animation(size=(0, 0), duration=0.12)
        # anim4 = Animation(pos=(ellipse4.pos[0] + 10, ellipse4.pos[1] - 25), size=(3, 3), duration=0.25)
        # anim4 += Animation(size=(0, 0), duration=0.1)

        anim5 = Animation(pos=(ellipse5.pos[0], ellipse5.pos[1] - 25), size=(3, 3), duration=0.25)
        anim5 += Animation(size=(0, 0), duration=0.13)
        anim6 = Animation(pos=(ellipse6.pos[0], ellipse6.pos[1] + 25), size=(3, 3), duration=0.25)
        anim6 += Animation(size=(0, 0), duration=0.15)

        anim.start(ellipse)
        anim2.start(ellipse2)
        # anim3.start(ellipse3)
        # anim4.start(ellipse4)
        anim5.start(ellipse5)
        anim6.start(ellipse6)


class EllipseAnimationApp(App):
    def build(self):
        layout = FloatLayout()
        self.bg_music = SoundLoader.load('../sounds/correct_2.mp3')
        button = Button(text='Click me!', size_hint=(None, None), size=(100, 50), pos=(250, 250))
        button.bind(on_press=self.correct_answer)
        layout.add_widget(button)

        return layout

    def correct_answer(self, instance):
        self.bg_music.play()
        self.spawn_animation(instance)
        instance.background_color = [0, 1, 0, 1]

    @staticmethod
    def spawn_animation(self, instance):
        # Get the button position
        button_pos = instance.pos

        # Create a small ellipse
        with instance.canvas:
            Color(0, 1, 0, 1)  # Green color
            ellipse = Ellipse(pos=(button_pos[0], button_pos[1] + instance.size[1] / 2), size=(10, 10))
            ellipse2 = Ellipse(pos=(button_pos[0] + instance.size[0], button_pos[1] + instance.size[1] / 2),
                               size=(10, 10))
            # ellipse3= Ellipse(pos=(button_pos[0] , button_pos[1] ), size=(10, 10))
            # ellipse4 = Ellipse(pos=(button_pos[0] + instance.size[0], button_pos[1]), size=(10, 10))
            Color(1, 1, 0, 1)  # Red color
            ellipse5 = Ellipse(pos=(button_pos[0] + instance.size[0] / 2, button_pos[1]), size=(10, 10))
            ellipse6 = Ellipse(pos=(button_pos[0] + instance.size[0] / 2, button_pos[1] + instance.size[1]),
                               size=(10, 10))

        # Animation to move the ellipse up, shrink, and fade out
        anim = Animation(pos=(ellipse.pos[0] - 25, ellipse.pos[1]), size=(3, 3), duration=0.25)
        anim += Animation(size=(0, 0), duration=0.16)
        anim2 = Animation(pos=(ellipse2.pos[0] + 25, ellipse2.pos[1]), size=(3, 3), duration=0.25)
        anim2 += Animation(size=(0, 0), duration=0.14)
        # anim3 = Animation(pos=(ellipse3.pos[0] - 10, ellipse3.pos[1] - 25), size=(3, 3), duration=0.25)
        # anim3 += Animation(size=(0, 0), duration=0.12)
        # anim4 = Animation(pos=(ellipse4.pos[0] + 10, ellipse4.pos[1] - 25), size=(3, 3), duration=0.25)
        # anim4 += Animation(size=(0, 0), duration=0.1)

        anim5 = Animation(pos=(ellipse5.pos[0], ellipse5.pos[1] - 25), size=(3, 3), duration=0.25)
        anim5 += Animation(size=(0, 0), duration=0.13)
        anim6 = Animation(pos=(ellipse6.pos[0], ellipse6.pos[1] + 25), size=(3, 3), duration=0.25)
        anim6 += Animation(size=(0, 0), duration=0.15)

        anim.start(ellipse)
        anim2.start(ellipse2)
        # anim3.start(ellipse3)
        # anim4.start(ellipse4)
        anim5.start(ellipse5)
        anim6.start(ellipse6)


if __name__ == '__main__':
    EllipseAnimationApp().run()
