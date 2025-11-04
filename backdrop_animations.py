"""
The animations in this file are provided by the author emhayki from the repository
[emhayki/Animated-Mathematics](https://github.com/emhayki/Animated-Mathematics)
so this file has been licensed twice.

MIT License

Copyright © 2025 emhayki
Copyright © 2025 VEFrenovator

Permission is hereby granted, free of charge, to any person obtaining a copy of this software
and associated documentation files (the "Software"), to deal in the Software without restriction,
including without limitation the rights to use, copy, modify, merge, publish, distribute,
sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or
substantial portions of the Software.

---

*Общее описание*
Этот файл является логическим продолжение основного файла slides_animation и представляет из себя
короткометражные анимации, которые можно включить в конце выступления, когда хронометраж не
заполнен значащей информацией, а также когда аудитория задаёт вопросы.
"""

# Импорт библиотек
import numpy as np
from manim import *
from slides_animation import rus_tex_template
from copyrighting import *


config.frame_height = 16
config.frame_width = 16 * 16 / 9

CREDIT = CopyrightMark("emhayki", 2025, "MIT")


class CardioidAndNefroid(Scene):
    """Показ способов построения кардиоиды и нефроиды"""

    def construct(self):  # pylint: disable=missing-function-docstring
        # Copyright
        self.play(CreateCopyrightMark(CREDIT))

        # Кардиоида
        title = Text("Кардиоида", color=WHITE, weight=BOLD).scale(1.2).move_to(UP * 3.5)
        self.play(Write(title))

        circle = Circle(radius=3, color=WHITE)
        circle.move_to(DOWN * 1.5)
        self.play(Create(circle))

        n = 120
        lines = VGroup()
        for i in range(1, n + 1):
            start_angle = i * TAU / n
            end_angle = (2 * i) % n * TAU / n
            start = circle.point_at_angle(start_angle)
            end = circle.point_at_angle(end_angle)
            line = Line(start, end, stroke_color=YELLOW, stroke_opacity=0.4)
            lines.add(line)

        self.play(Create(lines), run_time=3)
        self.wait(3)
        cardioid_group = VGroup(title, circle, lines)

        # Нефроида
        title2 = (
            Text("Нефроида", color=WHITE, weight=BOLD)
            .scale(1.2)
            .move_to(UP * 3.5)
            .shift(RIGHT * config.frame_width / 4 * 0.7)
        )
        self.play(
            AnimationGroup(
                cardioid_group.animate.shift(LEFT * config.frame_width / 4 * 0.7),
                Write(title2),
            )
        )

        circle2 = Circle(radius=3, color=WHITE)
        circle2.move_to(DOWN * 1.5).shift(RIGHT * config.frame_width / 4 * 0.7)
        self.play(Create(circle2))

        n = 200
        a = 3
        b = 2
        lines2 = VGroup()

        for i in range(n):
            start_angle = i * TAU / n
            end_angle = ((a * i + b) % n) * TAU / n
            start = circle2.point_at_angle(start_angle)
            end = circle2.point_at_angle(end_angle)
            line = Line(start, end, stroke_color=YELLOW, stroke_opacity=0.3)
            lines2.add(line)

        self.play(Create(lines2), run_time=4)
        self.wait(3)

        # Отчистка экрана
        self.play(
            AnimationGroup(
                Uncreate(circle),
                Uncreate(circle2),
                Uncreate(lines),
                Uncreate(lines2),
                Unwrite(title),
                Unwrite(title2),
            )
        )
        self.wait()


class GaussianDistribution(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=70 * DEGREES, theta=45 * DEGREES)

        # Copyright
        self.add_fixed_in_frame_mobjects(CREDIT)

        # Title and subtitle
        title = (
            Text(r"Трёхмерное Гауссово распределение", weight=BOLD)
            .scale(1.2)
            .move_to(UP * 4)
        )
        equation = (
            MathTex(r"z(x, y) = 2 e^{-(x^2 + y^2)}", color=YELLOW)
            .scale(0.8)
            .next_to(title, DOWN, buff=0.4)
        )
        self.add_fixed_in_frame_mobjects(title, equation)
        self.play(Write(title), Write(equation))

        # Axes
        self.begin_ambient_camera_rotation(rate=0.1)
        axes = ThreeDAxes(
            x_range=[-3, 3],
            y_range=[-3, 3],
            z_range=[0, 2.5],
            x_length=6,
            y_length=6,
            z_length=4,
            tips=False,
            axis_config={"color": GRAY},
        ).shift(-OUT * 2.75)

        self.play(Create(axes))
        self.bring_to_front(axes)

        # Surface
        def gaussian(x, y):
            return 2 * np.exp(-(x**2 + y**2))

        surface = Surface(
            lambda u, v: np.array([u, v, gaussian(u, v)]),
            u_range=[-2.5, 2.5],
            v_range=[-2.5, 2.5],
            resolution=(64, 32),
            fill_opacity=0.9,
            checkerboard_colors=[BLUE_D, BLUE_E],
            stroke_color=GRAY_E,
        ).shift(-OUT * 2.25)

        self.play(Create(surface, scale=0.3))

        self.wait(10)

        # Отчистка
        self.play(
            AnimationGroup(
                Uncreate(surface), Uncreate(axes), Unwrite(equation), Unwrite(title)
            )
        )
        self.wait()
