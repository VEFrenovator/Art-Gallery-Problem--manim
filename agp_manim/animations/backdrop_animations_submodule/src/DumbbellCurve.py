from manim import *
import numpy as np

# Vertical video configuration
config.frame_width = 9
config.frame_height = 16
config.pixel_width = 1080
config.pixel_height = 1920
config.frame_rate = 30

class DumbbellCurve(Scene):
    def construct(self):
        self.camera.background_color = BLACK

        # Title and formula
        title = Text("Dumbbell Curve", color=WHITE, weight=BOLD).scale(1.4).move_to(UP * 3.5)
        formula = MathTex(
            r"x^4(a^2 - x^2) - (0.8a)^4 y^2 = 0",
            color=YELLOW
        ).scale(0.8).next_to(title, DOWN, buff=0.4)
        self.play(Write(title), Write(formula))

        # Axes
        axes = Axes(
            x_range=[-12.5, 12.5],
            y_range=[-12.5, 12.5],
            x_length=6.5,
            y_length=6.5,
            tips=False,
            axis_config={"color": GRAY}
        ).move_to(DOWN * 2.0)
        self.play(Create(axes))

        # Initial parameter label
        a_label = MathTex("a = 0", color=YELLOW).scale(0.9).next_to(formula, DOWN, buff=0.4)
        self.play(Write(a_label))

        # Parameter values and colors
        a_values = [4, 5, 6, 7, 8, 9, 10, 11, 12]
        colors = color_gradient([BLUE, TEAL, GREEN, YELLOW, ORANGE, RED], len(a_values))

        # Draw and animate curves
        for i, a in enumerate(a_values):
            new_label = MathTex(f"a = {a}", color=YELLOW).scale(0.9).move_to(a_label.get_center())

            def dumbbell_fn(x, y):
                return x**4 * (a**2 - x**2) - (0.8 * a)**4 * y**2

            curve = axes.plot_implicit_curve(
                dumbbell_fn,
                color=colors[i],
                stroke_width=2.8,
                min_depth=0.01
            )

            self.play(Transform(a_label, new_label), Create(curve), run_time=1.3)
            self.add(curve)
            self.wait(0.2)

        self.wait(2)
