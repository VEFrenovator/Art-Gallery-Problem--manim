import math
from manim import *


class TennisBall(VMobject):
    def __init__(
        self,
        radius: float = 1.0,
        fill_color: ParsableManimColor | None = None,
        stroke_width: float = 8.0,
        **kwargs
    ):
        super().__init__(**kwargs)

        # Создание мяча
        self.body = Circle(radius=radius, color=WHITE, stroke_width=stroke_width)

        if fill_color is not None:
            self.body.set_fill(fill_color, opacity=1)

        # Создание полос
        arc1 = Arc(
            radius=radius,
            angle=PI / 2,
            start_angle=PI / 4,
            stroke_color=WHITE,
            stroke_width=stroke_width / 2,
        ).flip(RIGHT)
        arc1.shift(arc1.radius * (1 - math.cos(arc1.angle / 2)) * DOWN)

        arc2 = Arc(
            radius=radius,
            angle=PI / 2,
            start_angle=PI / 4 + PI,
            stroke_color=WHITE,
            stroke_width=stroke_width / 2,
        ).flip(RIGHT)
        arc2.shift(arc2.radius * (1 - math.cos(arc2.angle / 2)) * UP)

        self.arcs = VGroup([arc1, arc2]).rotate(PI / 2)
        self.add(self.body, self.arcs)


class Greetings(Scene):
    """
    Класс отображения приветственного текста (тема и автор).
    """

    def construct(self):
        # Приветственный текст
        theme = Text(
            "Ускорение свободного падения",
            font_size=48,
        )

        author = Text(
            "Подготовил Емельяненко Владимир",
            font_size=28,
        )
        author.move_to(theme.get_bottom() + DOWN * 0.2)

        # Вывод
        text_out_group = VGroup(theme, author)
        out_lag_ratio = 1.5

        self.wait()
        self.play(AnimationGroup(Write(text_out_group), lag_ratio=out_lag_ratio))
        self.wait()
        self.play(AnimationGroup(Unwrite(text_out_group), lag_ratio=out_lag_ratio))
        self.wait()


class AccelerationOfFreeFall(Scene):
    def construct(self):
        # Мяч
        tennis_ball = TennisBall(radius=0.45, fill_color=RED, stroke_width=6.0)
        self.play(GrowFromCenter(tennis_ball), run_time=2)
        self.wait()
        # self.play(tennis_ball.animate.rotate(PI / 2, about_point=tennis_ball.body.get_center()))
        self.play(tennis_ball.animate.shift(UP * 3))

