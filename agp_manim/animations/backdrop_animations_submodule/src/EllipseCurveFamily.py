from manim import *
import numpy as np

# Vertical video configuration
config.frame_width = 9
config.frame_height = 16
config.pixel_width = 1080
config.pixel_height = 1920
config.frame_rate = 30

class EllipseCurveFamily(Scene):
    def construct(self):
        self.camera.background_color = BLACK

        # Title and equation
        title = Text("Ellipse Curve Family", color=WHITE, weight=BOLD).scale(1.2).move_to(UP * 3.5)
        equation = MathTex(
            r"x^2 + y^2 \cdot a - a^2 = 0",
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

        # Parameter label
        a_label = MathTex("a = 0", color=YELLOW).scale(0.85).next_to(equation, DOWN, buff=0.4)
        self.play(Write(a_label))

        # Parameter values and colors
        a_values = list(range(-9, 10))
        colors = color_gradient([BLUE, GREEN, YELLOW, ORANGE, RED], len(a_values))

        # Animate ellipse curves
        for i, a in enumerate(a_values):
            new_label = MathTex(f"a = {a}", color=YELLOW).scale(0.85).move_to(a_label.get_center())

            def ellipse_fn(x, y):
                return x**2 + y**2 * a - a**2

            curve = axes.plot_implicit_curve(
                ellipse_fn,
                color=colors[i],
                stroke_width=2.4,
                min_depth=0.01
            )

            self.play(Transform(a_label, new_label), Create(curve), run_time=1.1)
            self.add(curve)
            self.wait(0.1)

        self.wait(2)
