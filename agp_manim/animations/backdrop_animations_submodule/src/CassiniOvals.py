from manim import *
import numpy as np

# Vertical video setup
config.frame_width = 9
config.frame_height = 16
config.pixel_width = 1080
config.pixel_height = 1920
config.frame_rate = 30

class CassiniOvals(Scene):
    def construct(self):
        self.camera.background_color = BLACK

        # Title and equation
        title = Text("Cassini Oval", color=WHITE, weight=BOLD).scale(1.2).move_to(UP * 3.5)
        equation = MathTex(
            r"(x^2 + y^2)^2 - 2(x^2 - y^2) + 1 - a^4 = 0",
            color=YELLOW
        ).scale(0.8).next_to(title, DOWN, buff=0.4)
        self.play(Write(title), Write(equation))

        # Axes
        axes = Axes(
            x_range=[-2, 2],
            y_range=[-2, 2],
            x_length=6,
            y_length=6,
            axis_config={"color": GRAY},
            tips=False
        ).move_to(DOWN * 2)
        self.play(Create(axes))

        # Initial parameter label
        a_label = MathTex("a = 0.8", color=YELLOW).scale(0.85)
        a_label.next_to(equation, DOWN, buff=0.4)
        self.play(Write(a_label))

        # Parameter values and color gradient
        a_values = [0.8, 1, 1.1, 1.2, 1.3, 1.4, 1.6]
        colors = color_gradient([BLUE, GREEN, YELLOW, ORANGE, RED], len(a_values))

        # Draw Cassini ovals for each 'a'
        for i, a in enumerate(a_values):
            def f(x, y, a=a):
                return (x**2 + y**2)**2 - 2 * (x**2 - y**2) + 1 - a**4

            curve = axes.plot_implicit_curve(
                lambda x, y: f(x, y),
                color=colors[i],
                stroke_width=3,
                min_depth=0.01
            )

            new_label = MathTex(f"a = {a}", color=YELLOW).scale(0.85).move_to(a_label.get_center())
            self.play(Transform(a_label, new_label), Create(curve), run_time=1.0)
            self.add(curve)

        self.wait(2)
