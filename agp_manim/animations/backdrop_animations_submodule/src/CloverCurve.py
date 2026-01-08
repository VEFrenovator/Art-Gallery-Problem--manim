from manim import *
import numpy as np

# Vertical video configuration
config.frame_width = 9
config.frame_height = 16
config.pixel_width = 1080
config.pixel_height = 1920
config.frame_rate = 30

class CloverCurve(Scene):
    def construct(self):
        self.camera.background_color = BLACK

        # Title and equation
        title = Text("A Clover Function", color=WHITE, weight=BOLD).scale(1.2).move_to(UP * 3.5)
        equation = MathTex(
            r"(x^2 + y^2)^3 - 4x^2y^2(a^2 + 1) = \dfrac{a}{100000}",
            color=YELLOW
        ).scale(0.8).next_to(title, DOWN, buff=0.4)
        self.play(Write(title), Write(equation))

        # Axes
        axes = Axes(
            x_range=[-10, 10],
            y_range=[-10, 10],
            x_length=6,
            y_length=6,
            tips=False,
            axis_config={"color": GRAY}
        ).move_to(DOWN * 2.0)
        self.play(Create(axes))

        # Parameter label and values
        a_values = list(range(1, 11))
        colors = color_gradient([BLUE, TEAL, GREEN, YELLOW, ORANGE, RED], len(a_values))
        a_label = MathTex("a = 0", color=YELLOW).scale(0.85).next_to(equation, DOWN, buff=0.4)
        self.play(Write(a_label))

        # Draw and animate the clover curves
        for i, a in enumerate(a_values):
            new_label = MathTex(f"a = {a}", color=YELLOW).scale(0.85).move_to(a_label.get_center())

            def clover_fn(x, y):
                return (x**2 + y**2)**3 - 4 * x**2 * y**2 * (a**2 + 1) - a / 100000

            curve = axes.plot_implicit_curve(
                clover_fn,
                color=colors[i],
                stroke_width=2.5,
                min_depth=0.01
            )

            self.play(Transform(a_label, new_label), Create(curve), run_time=1.2)
            self.add(curve)
            self.wait(0.2)

        self.wait(2)
