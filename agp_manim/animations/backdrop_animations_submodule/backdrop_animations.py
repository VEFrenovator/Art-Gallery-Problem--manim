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
from agp_manim.animations.slides_animation import (
    rus_tex_template,
    BACKGROUND_COLOR_CODE,
)
from agp_manim.utils.copyrighting import (
    CopyrightMark,
    CreateCopyrightMark,
    UncreateCopyrightMark,
)


config.background_color = ManimColor(BACKGROUND_COLOR_CODE)
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

        self.play(Create(surface, lag_ration=0.2))

        self.wait(10)

        # Отчистка
        self.play(
            AnimationGroup(
                Uncreate(surface), Uncreate(axes), Unwrite(equation), Unwrite(title)
            )
        )
        self.wait()


class Fields(Scene):
    def construct(self):
        # ЗНАК КОПИРАЙТА
        self.add(CREDIT)

        # ПОДГОТОВКА ГРУПП ПОЛЕЙ
        # Круговое вихревое поле
        swirl_color = GREEN
        swirl_lines = (
            StreamLines(
                self.swirl_solver,
                x_range=[-4, 4, 0.4],
                y_range=[-4, 4, 0.4],
                stroke_width=1.2,
                max_anchors_per_line=50,
                virtual_time=4,
                dt=0.05,
                color=swirl_color,
            )
            .scale(0.6)
            .move_to(DOWN * 2.0)
        )
        swirl_title = (
            Text("Круговое вихревое поле", color=swirl_color, weight=BOLD)
            .scale(1.2)
            .move_to(UP * 3.5)
        )
        swirl_eq = (
            MathTex(r"\vec{F}(x, y) = (-y, x)", color=YELLOW)
            .scale(0.8)
            .next_to(swirl_title, DOWN, buff=0.4)
        )
        swirl_group = VDict(
            {
                "field": swirl_lines,
                "title": swirl_title,
                "eq": swirl_eq,
            }
        )

        # Поле радиального стока
        sink_color = PURPLE
        sink_lines = (
            StreamLines(
                self.sink_solver,
                x_range=[-4, 4, 0.3],
                y_range=[-4, 4, 0.3],
                stroke_width=1.2,
                max_anchors_per_line=50,
                virtual_time=4,
                dt=0.05,
                color=sink_color,
            )
            .scale(0.6)
            .move_to(DOWN * 2.0)
        )
        sink_title = (
            Text("Поле радиального стока", color=sink_color, weight=BOLD)
            .scale(1.2)
            .move_to(UP * 3.5)
        )
        sink_eq = (
            MathTex(
                r"\vec{F}(x, y) = \left(",
                r"-\frac{x}{\sqrt{x^2 + y^2}}, \quad -\frac{y}{\sqrt{x^2 + y^2}}",
                color=YELLOW,
            )
            .scale(0.8)
            .next_to(sink_title, DOWN, buff=0.4)
        )
        sink_group = VDict(
            {
                "field": sink_lines,
                "title": sink_title,
                "eq": sink_eq,
            }
        )

        # Синусоидальное поле
        sin_color = RED
        sin_lines = (
            StreamLines(
                self.sin_solver,
                x_range=[-4, 4, 0.1],
                y_range=[-4, 4, 0.1],
                stroke_width=1.2,
                max_anchors_per_line=50,
                virtual_time=4,
                dt=0.05,
                color=sin_color,
            )
            .scale(0.6)
            .move_to(DOWN * 2.0)
        )
        sin_title = (
            Text("Синусоидальное поле", color=sin_color, weight=BOLD)
            .scale(1.2)
            .move_to(UP * 3.5)
        )
        sin_eq = (
            MathTex(r"\vec{F}(x, y) = (-y, x)", color=YELLOW)
            .scale(0.8)
            .next_to(sin_title, DOWN, buff=0.4)
        )
        sin_group = VDict(
            {
                "field": sin_lines,
                "title": sin_title,
                "eq": sin_eq,
            }
        )

        # Внутренне-спиральное поле
        spiral_color = PURPLE
        spiral_lines = (
            StreamLines(
                self.spiral_solver,
                x_range=[-4, 4, 0.3],
                y_range=[-4, 4, 0.3],
                stroke_width=1.2,
                max_anchors_per_line=50,
                virtual_time=4,
                dt=0.05,
                color=spiral_color,
            )
            .scale(0.6)
            .move_to(DOWN * 2.0)
        )
        spiral_title = (
            Text("Внутренне-спиральное поле", color=spiral_color, weight=BOLD)
            .scale(1.2)
            .move_to(UP * 3.5)
        )
        spiral_eq = (
            MathTex(r"\vec{F}(x, y) = (-y, x)", color=YELLOW)
            .scale(0.8)
            .next_to(spiral_title, DOWN, buff=0.4)
        )
        spiral_group = VDict(
            {
                "field": spiral_lines,
                "title": spiral_title,
                "eq": spiral_eq,
            }
        )

        # ВЫВОД ГРУППОЙ
        self.add(swirl_lines, sink_lines, sin_lines, spiral_lines)
        groups = (
            Group(swirl_group, sink_group, sin_group, spiral_group)
            .arrange_in_grid(rows=2, cols=2, buff=LARGE_BUFF)
            .scale_to_fit_height(config.frame_height * 0.95)
            .scale_to_fit_width(config.frame_width * 0.95)
        )

        for group in groups:
            group["field"].start_animation()
            self.play(Write(group["title"]), Write(group["eq"]))

        self.wait(10)

        for group in groups:
            self.play(
                group["field"].end_animation(),
                Unwrite(group["title"]),
                Unwrite(group["eq"]),
            )
        self.wait()

    @staticmethod
    def swirl_solver(pos) -> np.ndarray:
        x, y = pos[:2]
        return np.array([-y, x, 0])

    @staticmethod
    def sink_solver(pos) -> np.ndarray:
        x, y = pos[:2]
        r = np.sqrt(x**2 + y**2) + 0.1  # avoid division by zero
        return np.array([-x / r, -y / r, 0])

    @staticmethod
    def sin_solver(pos) -> np.ndarray:
        x, y = pos[:2]
        return 0.2 * np.array([np.sin(y), np.sin(x), 0])

    @staticmethod
    def spiral_solver(pos) -> np.ndarray:
        x, y = pos[:2]
        return np.array([-y - x, x - y, 0])
