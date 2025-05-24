"""
Цель: анимированный показ законов ускорения тел в свободном падении, выведение
формул, отслеживание графиков, нужных для более глубокого изучения темы.
"""

import math
from manim import *


# Ускорение свободного падения
GRAVITY = 9.80665

# Русский шрифт
rus_text_template = TexTemplate(
    tex_compiler="xelatex",
    output_format=".xdv",
    preamble=r"""
        \usepackage{polyglossia}
        \setmainlanguage{russian}
        \usepackage{fontspec}
        \setmainfont{Times New Roman}
    """,
)


class AnimateFreeFall(Animation):
    """
    Активация свободного падения.
    """

    def __init__(
        self,
        falling_mobject: Mobject,
        duration: float,
        gravity: float = GRAVITY,
        cam_zoom: float = 1.0,
        **kwargs
    ):
        # Инициализация родителя
        super().__init__(falling_mobject, run_time=duration, rate_func=linear, **kwargs)

        # Отслеживающе переменные
        self.falling_mobject = falling_mobject
        self.start_coords = falling_mobject.get_center()
        self.gravity = gravity
        self.cam_zoom = cam_zoom

    def interpolate_mobject(self, alpha):
        real_alpha = self.rate_func(alpha)
        time = self.run_time * real_alpha
        self.falling_mobject.move_to(
            self.start_coords + DOWN * (time**2) * self.gravity * 0.5 * self.cam_zoom
        )


class TennisBall(VMobject):
    """
    Теннисный мячик - самый наглядный пример для показа.
    """

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
        # МЯЧ
        # Тело + трасер
        tennis_ball = TennisBall(radius=0.45, fill_color=RED, stroke_width=6.0)
        tennis_ball_traced_path = TracedPath(
            tennis_ball.get_center,
            stroke_width=tennis_ball.body.radius * 100,
            stroke_color=tennis_ball.body.color,
            stroke_opacity=[1, 0],
            dissipating_time=0.25,
        )

        # Показ мяча
        self.wait()
        self.play(GrowFromCenter(tennis_ball), run_time=2)
        self.wait()
        self.play(tennis_ball.animate.to_edge(config.top))
        self.wait()

        # СВОБОДНОЕ ПАДЕНИЕ № 1
        self.play(AnimateFreeFall(falling_mobject=tennis_ball, duration=5))
        self.play(tennis_ball.animate.move_to(ORIGIN))

        # СВОБОДНОЕ ПАДЕНИЕ № 2
        duration = 10
        # Числовая система
        number_plane = NumberPlane(
            x_range=[0, duration, 1.5],
            y_range=[0, max(duration * GRAVITY, duration**2 * GRAVITY * 0.5), 50],
            x_length=config.frame_width / 2 - DEFAULT_MOBJECT_TO_EDGE_BUFFER,
            y_length=config.frame_height - (DEFAULT_MOBJECT_TO_EDGE_BUFFER * 2),
            faded_line_style={"stroke_color": WHITE},
            background_line_style={"stroke_color": ORANGE, "stroke_opacity": 0.5},
            axis_config={"include_numbers": True},
            tips=True
        )

        # Графики функций (plots)
        free_fall_speed_func_plot = number_plane.plot(
            lambda time: time * GRAVITY, use_vectorized=True, color=YELLOW
        )
        free_fall_dist_func_plot = number_plane.plot(
            lambda time: time**2 * GRAVITY * 0.5, use_vectorized=True, color=RED_B
        )
        func_plots = VGroup(free_fall_speed_func_plot, free_fall_dist_func_plot)

        VGroup(number_plane, func_plots).to_edge(RIGHT)

        # Вывод
        # Сдвиг/маштабирование мяча
        scale_factor = 0.4
        self.play(tennis_ball.animate.to_corner(UL))
        self.play(tennis_ball.animate.scale(scale_factor))
        self.wait()
        # График скорости
        self.play(Create(number_plane, lag_ratio=0.5), run_time=4)
        self.wait()
        # Падение
        self.play(
            Create(func_plots, lag_ratio=0, run_time=duration, rate_func=linear),
            AnimateFreeFall(tennis_ball, duration, cam_zoom=scale_factor),
        )
        self.wait()
        # Выделение графиков
        for _ in range(2):
            self.play(Indicate(func_plots))
            self.wait(0.25)
        # Подъём
        self.play(
            Uncreate(func_plots),
            tennis_ball.animate.to_edge(LEFT),
            run_time=5,
            lag_ration=0,
        )
        # Очистка
        self.play(
            Uncreate(VGroup(*[func_plots, tennis_ball, number_plane]), lag_ration=0),
            run_time=4,
        )
        self.wait()


class Equation(Scene):
    def construct(self):
        font_size = 80
        gravity_text = Tex(
            r"$g=9.8\frac{m}{s^2}$",
            font_size=font_size,
        )
        speed_text = Tex(r"$v=g*t$", font_size=font_size)
        dist_text = Tex(r"$s=g*t^{2}*0.5$", font_size=font_size)
        self.play(Write(gravity_text))
        self.wait()
        self.play(gravity_text.animate.shift(UP * 2), Write(speed_text))
        self.wait()
        self.play(Write(dist_text.shift(DOWN * 2)))
        self.wait()
        self.play(Unwrite(VGroup(gravity_text, speed_text, dist_text)))
        self.wait()


class NonGravity(Scene):
    def construct(self):
        # Земля
        planet = Circle(
            radius=config.frame_height / 2 - 2,
            color=GREEN,
            fill_color=GREEN,
            fill_opacity=0.25,
        )
        self.play(Create(planet))
        self.wait()
        self.play(planet.animate.scale(10).shift(DOWN * (planet.radius * 10 + 3)))
        self.wait()
        # Мяч
        tennis_ball = TennisBall(radius=0.2, fill_color=RED, stroke_width=5).shift(
            UP * 2
        )
        self.play(Create(tennis_ball))
        self.wait()
