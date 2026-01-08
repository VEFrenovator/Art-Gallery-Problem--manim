from manim import *
import numpy as np

# Vertical video configuration
config.frame_width = 9
config.frame_height = 16
config.pixel_width = 1080
config.pixel_height = 1920
config.frame_rate = 30

class ButterflyCurve(Scene):
    def construct(self):
        self.camera.background_color = BLACK

        # Title
        title = Text("The Butterfly Curve", color=WHITE, weight=BOLD).scale(1.2).move_to(UP * 3.5)
        self.play(Write(title))
        self.add(title)

        # Equation
        equation = MathTex(
            r"r(t) = e^{\sin(t)} - 2\cos(4t) + \sin^5\left(\frac{2t - \pi}{24}\right)",
            color=YELLOW
        ).scale(0.8).next_to(title, DOWN, buff=0.4)
        self.play(Write(equation))
        self.add(equation)

        # Axes
        axes = Axes(
            x_range=[-4, 4],
            y_range=[-4, 4],
            x_length=6,
            y_length=6,
            axis_config={"color": GRAY},
            tips=False,
        ).move_to(DOWN * 2.0)
        self.play(Create(axes))
        self.add(axes)

        # Butterfly polar function
        def r(t):
            return np.exp(np.sin(t)) - 2 * np.cos(4 * t) + np.sin((2 * t - np.pi) / 24) ** 5

        def parametric_func(t):
            return axes.c2p(r(t) * np.cos(t), r(t) * np.sin(t))

        # Generate the butterfly curve
        curve = VMobject(color=PINK, stroke_width=2.5)
        points = [parametric_func(t) for t in np.linspace(0, 24 * PI, 3000)]
        curve.set_points_smoothly(points)

        self.play(Create(curve), run_time=6)
        self.add(curve)
        self.wait(2)
