from manim import *
import numpy as np

# Vertical video configuration
config.frame_width = 9
config.frame_height = 16
config.pixel_width = 1080
config.pixel_height = 1920
config.frame_rate = 30

class DevilsCurve(Scene):
    def construct(self):
        self.camera.background_color = BLACK

        # Title and equation
        title = Text("Devil’s Curve", color=WHITE, weight=BOLD).scale(1.2).move_to(UP * 3.5)
        equation = MathTex(
            r"y^4 - \left(\frac{a}{3}\right)^2 y^2 - x^4 + \left(\frac{a}{2}\right)^2 x^2 = 0",
            color=YELLOW
        ).scale(0.8).next_to(title, DOWN, buff=0.4)
        self.play(Write(title), Write(equation))

        # Axes
        axes = Axes(
            x_range=[-6, 6],
            y_range=[-6, 6],
            x_length=6,
            y_length=6,
            tips=False,
            axis_config={"color": GRAY}
        ).move_to(DOWN * 2.0)
        self.play(Create(axes))

        # Parameter values and color gradient
        a_values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        colors = color_gradient([BLUE, TEAL, GREEN, YELLOW, ORANGE, RED], len(a_values))

        # Initial label
        a_label = MathTex("a = 0", color=YELLOW).scale(0.85).next_to(equation, DOWN, buff=0.4)
        self.play(Write(a_label))

        # Draw devil's curves
        for i, a in enumerate(a_values):
            new_label = MathTex(f"a = {a}", color=YELLOW).scale(0.85).move_to(a_label.get_center())

            def f(x, y):
                return y**4 - (a / 3)**2 * y**2 - x**4 + (a / 2)**2 * x**2

            curve = axes.plot_implicit_curve(
                lambda x, y: f(x, y),
                color=colors[i],
                stroke_width=2.5,
                min_depth=0.01
            )

            self.play(Transform(a_label, new_label), Create(curve), run_time=1.2)
            self.add(curve)
            self.wait(0.2)

        self.wait(2)
