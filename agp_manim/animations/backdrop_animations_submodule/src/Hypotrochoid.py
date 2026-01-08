from manim import *
import numpy as np

# Configuration for vertical output
config.frame_width = 9
config.frame_height = 16
config.pixel_width = 1080
config.pixel_height = 1920
config.frame_rate = 30

class Hypotrochoid(Scene):
    def construct(self):
        self.camera.background_color = BLACK

        # Title
        title = Text("Hypotrochoid Curve", color=WHITE, weight=BOLD).scale(1.2)
        title.move_to(UP * 3.5)
        self.play(Write(title))

        # Equation using MathTex (split into 2 lines to fit)
        equation1 = MathTex(
            r"x(t) = (R - r)\cos(t) + d\cos\left(\frac{R - r}{r}t\right)",
            color=YELLOW
        ).scale(0.8)
        equation1.next_to(title, DOWN, buff=0.3)

        equation2 = MathTex(
            r"y(t) = (R - r)\sin(t) - d\sin\left(\frac{R - r}{r}t\right)",
            color=YELLOW
        ).scale(0.8)
        equation2.next_to(equation1, DOWN, buff=0.3)

        self.play(Write(equation1), Write(equation2))

        # Axes
        axes = Axes(
            x_range=[-8, 8],
            y_range=[-7, 7],
            x_length=6,
            y_length=6,
            axis_config={"color": GRAY},
            tips=False
        ).move_to(DOWN * 2.5)
        self.play(Create(axes))

        # Parameters
        R, r, d = 5, 3, 5
        t_vals = np.linspace(0, 2 * np.pi * r, 600)

        # Parametric function
        def param(t):
            x = (R - r) * np.cos(t) + d * np.cos((R - r) / r * t)
            y = (R - r) * np.sin(t) - d * np.sin((R - r) / r * t)
            return axes.c2p(x, y)

        # Generate points and draw curve
        points = [param(t) for t in t_vals]
        curve = VMobject(color=YELLOW).set_points_as_corners(points)
        self.play(Create(curve, run_time=6))
        self.wait(2)