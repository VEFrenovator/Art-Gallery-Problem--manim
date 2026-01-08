from manim import *
import numpy as np

# Vertical video configuration
config.frame_width = 9
config.frame_height = 16
config.pixel_width = 1080
config.pixel_height = 1920
config.frame_rate = 30

class HeartCurve(Scene):
    def construct(self):
        self.camera.background_color = BLACK

        # --- Title and Equation ---
        title = Text("Heart Curve", color=WHITE, weight=BOLD).scale(1.2)
        title.move_to(UP * 3.5)

        equation = MathTex(
            r"x^2 + \left(y - (x^2)^{1/3} \right)^2 - a^2 = 0",
            color=YELLOW
        ).scale(0.8).next_to(title, DOWN, buff=0.4)

        self.play(Write(title), Write(equation))

        # --- Axes ---
        axes = Axes(
            x_range=[-12, 12],
            y_range=[-12, 12],
            x_length=6,
            y_length=6,
            tips=False,
            axis_config={"color": GRAY}
        ).move_to(DOWN * 2.0)
        self.play(Create(axes))

        # --- a values + label ---
        a_values = list(range(1, 11))
        colors = color_gradient([BLUE, TEAL, GREEN, YELLOW, ORANGE, RED], len(a_values))

        a_label = MathTex("a = 0", color=YELLOW).scale(0.85)
        a_label.next_to(equation, DOWN, buff=0.4)
        self.play(Write(a_label))

        # --- Plot Each Heart Curve ---
        for i, a in enumerate(a_values):
            new_label = MathTex(f"a = {a}", color=YELLOW).scale(0.85)
            new_label.move_to(a_label.get_center())

            def f(x, y):
                root_term = np.cbrt(x**2)  # safe cube root
                return x**2 + (y - root_term)**2 - a**2

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
