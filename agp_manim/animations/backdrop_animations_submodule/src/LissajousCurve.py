from manim import *
import numpy as np

config.frame_width = 9
config.frame_height = 16
config.pixel_width = 1080
config.pixel_height = 1920
config.frame_rate = 30

class MalteseCrossAlgebraic(Scene):
    def construct(self):
        self.camera.background_color = BLACK

        title = Text("The Maltese Cross", color=WHITE, weight=BOLD).scale(1.2)
        title.move_to(UP * 3.5)

        equation = MathTex(
            r"f(x, y) = \frac{a}{2}xy(x^2 - y^2) - x^2 - y^2",
            color=YELLOW
        ).scale(0.8).next_to(title, DOWN, buff=0.4)

        self.play(Write(title), Write(equation))

        axes = Axes(
            x_range=[-2.5, 2.5],
            y_range=[-2.5, 2.5],
            x_length=6,
            y_length=6,
            tips=False,
            axis_config={"color": GRAY}
        ).move_to(DOWN * 2.0)
        self.play(Create(axes))

        a_values = [1, 1.5, 2, 3, 4, 5, 7, 10, 12]
        colors = color_gradient([BLUE, TEAL, GREEN, YELLOW, ORANGE, RED], len(a_values))

        a_label = MathTex("a = 0.00", color=YELLOW).scale(0.85)
        a_label.next_to(equation, DOWN, buff=0.4)
        self.play(Write(a_label))

        for i, a in enumerate(a_values):
            new_label = MathTex(f"a = {a}", color=YELLOW).scale(0.85)
            new_label.move_to(a_label.get_center())

            def f(x, y):
                return (a / 2) * x * y * (x**2 - y**2) - x**2 - y**2

            curve = axes.plot_implicit_curve(
                lambda x, y: f(x, y),
                color=colors[i],
                stroke_width=2.5,
                min_depth=0.01
            )

            self.play(Transform(a_label, new_label), Create(curve), run_time=1.3)
            self.add(curve)
            self.wait(0.3)

        self.wait(2)
