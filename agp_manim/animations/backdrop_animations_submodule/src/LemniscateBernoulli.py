from manim import *
import numpy as np

# Configuration for vertical video
config.frame_width = 9
config.frame_height = 16
config.pixel_width = 1080
config.pixel_height = 1920
config.frame_rate = 30

class LemniscateBernoulli(Scene):
    def construct(self):
        self.camera.background_color = BLACK

        # Title
        title = Text("Lemniscate of Bernoulli", color=WHITE, weight=BOLD).scale(1.2)
        title.move_to(UP * 3.5)

        # Main equation
        equation = MathTex(
            r"(x^2 + y^2)^2 - 2a^2(x^2 - y^2) = 0",
            color=YELLOW
        ).scale(0.8).next_to(title, DOWN, buff=0.4)
        self.play(Write(title), Write(equation))

        # Axes
        axes = Axes(
            x_range=[-22, 22],
            y_range=[-22, 22],
            x_length=6,
            y_length=6,
            axis_config={"color": GRAY},
            tips=False
        ).move_to(DOWN * 2.0)

        self.play(Create(axes))

        # Label for parameter 'a'
        a_label = MathTex("a = 0", color=YELLOW).scale(0.85)
        a_label.next_to(equation, DOWN, buff=0.4)
        self.play(Write(a_label))

        # Parameter range and color gradient
        a_values = list(range(2, 16))
        colors = color_gradient([BLUE, GREEN, YELLOW, ORANGE, RED], len(a_values))

        for i, a in enumerate(a_values):
            new_label = MathTex(f"a = {a}", color=YELLOW).scale(0.85)
            new_label.move_to(a_label.get_center())

            def f(x, y):
                return (x**2 + y**2)**2 - 2 * (a**2) * (x**2 - y**2)

            curve = axes.plot_implicit_curve(
                lambda x, y: f(x, y),
                color=colors[i],
                stroke_width=2.5,
                min_depth=0.01
            )

            self.play(Transform(a_label, new_label), Create(curve), run_time=1)
            self.add(curve)
            self.wait(0.15)

        self.wait(2)
