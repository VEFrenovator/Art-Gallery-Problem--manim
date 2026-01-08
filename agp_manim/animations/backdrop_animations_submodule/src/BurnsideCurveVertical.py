from manim import *
import numpy as np

# Vertical video configuration
config.frame_width = 9
config.frame_height = 16
config.pixel_width = 1080
config.pixel_height = 1920
config.frame_rate = 30

class BurnsideCurve(Scene):
    def construct(self):
        self.camera.background_color = BLACK

        # Title and equation
        title = Text("Burnside Curve", color=WHITE, weight=BOLD).scale(1.2).move_to(UP * 3.5)
        equation = MathTex(r"y^2 - x(x^4 - a) = 0", color=YELLOW).scale(0.8).next_to(title, DOWN, buff=0.4)
        self.play(Write(title), Write(equation))

        # Axes
        axes = Axes(
            x_range=[-3.5, 3.5],
            y_range=[-3.5, 3.5],
            x_length=6,
            y_length=6,
            tips=False,
            axis_config={"color": GRAY}
        ).move_to(DOWN * 2.0)
        self.play(Create(axes))

        # Parameter values for 'a' and corresponding colors
        a_values = [-1, -0.5, 0, 1.25, 1.5, 2, 2.5, 3, 4, 5, 7]
        colors = color_gradient([BLUE, TEAL, GREEN, YELLOW, ORANGE, RED], len(a_values))

        # Initial parameter label
        a_label = MathTex("a = -1", color=YELLOW).scale(0.85)
        a_label.next_to(equation, DOWN, buff=0.4)
        self.play(Write(a_label))

        # Draw each curve with updated parameter
        for i, a in enumerate(a_values):
            new_label = MathTex(f"a = {a}", color=YELLOW).scale(0.85).move_to(a_label.get_center())

            def f(x, y):
                return y**2 - x * (x**4 - a)

            curve = axes.plot_implicit_curve(
                lambda x, y: f(x, y),
                color=colors[i],
                stroke_width=2.8,
                min_depth=0.01
            )

            self.play(Transform(a_label, new_label), Create(curve), run_time=1.1)
            self.add(curve)
            self.wait(0.2)

        self.wait(2)
