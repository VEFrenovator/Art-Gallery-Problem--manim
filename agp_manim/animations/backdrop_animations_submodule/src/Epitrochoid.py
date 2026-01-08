from manim import *
import numpy as np

# Configuration for vertical video
config.frame_width = 9
config.frame_height = 16
config.pixel_width = 1080
config.pixel_height = 1920
config.frame_rate = 30

class Epitrochoid(Scene):
    def construct(self):
        self.camera.background_color = BLACK

        # Title
        title = Text("Epitrochoid Curve", color=WHITE, weight=BOLD).scale(1.2)
        title.move_to(UP * 3.5)
        self.play(Write(title))

        # Equations
        eq1 = MathTex(
            r"x(t) = (R + r)\cos(t) - d\cos\left(\frac{R + r}{r}t\right)",
            color=YELLOW
        ).scale(0.8)
        eq1.next_to(title, DOWN, buff=0.3)

        eq2 = MathTex(
            r"y(t) = (R + r)\sin(t) - d\sin\left(\frac{R + r}{r}t\right)",
            color=YELLOW
        ).scale(0.8)
        eq2.next_to(eq1, DOWN, buff=0.3)

        self.play(Write(eq1), Write(eq2))

        # Axes
        axes = Axes(
            x_range=[-8, 8],
            y_range=[-8, 8],
            x_length=6,
            y_length=6,
            axis_config={"color": GRAY},
            tips=False
        ).move_to(DOWN * 2.5)
        self.play(Create(axes))

        # Parameters
        R, r, d = 4, 1, 3
        t_vals = np.linspace(0, 2 * np.pi * r * 6, 1000)

        def param(t):
            x = (R + r) * np.cos(t) - d * np.cos((R + r) / r * t)
            y = (R + r) * np.sin(t) - d * np.sin((R + r) / r * t)
            return axes.c2p(x, y)

        points = [param(t) for t in t_vals]
        curve = VMobject(color=YELLOW).set_points_as_corners(points)

        self.play(Create(curve, run_time=6))
        self.wait(2)