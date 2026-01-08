from manim import *
import numpy as np

# Configuration for vertical video
config.frame_width = 9
config.frame_height = 16
config.pixel_width = 1080
config.pixel_height = 1920
config.frame_rate = 30

class DeltoidCurve(Scene):
    def construct(self):
        self.camera.background_color = BLACK

        # Title
        title = Text("Deltoid Curve", color=WHITE, weight=BOLD).scale(1.2)
        title.move_to(UP * 3.5)
        self.play(Write(title))

        # Equations
        eq1 = MathTex(
            r"x(t) = 2R\cos(t) + R\cos(2t)",
            color=YELLOW
        ).scale(0.85)
        eq1.next_to(title, DOWN, buff=0.5)

        eq2 = MathTex(
            r"y(t) = 2R\sin(t) - R\sin(2t)",
            color=YELLOW
        ).scale(0.85)
        eq2.next_to(eq1, DOWN, buff=0.5)

        self.play(Write(eq1), Write(eq2))

        # Axes
        axes = Axes(
            x_range=[-4, 7],
            y_range=[-6, 6],
            x_length=6,
            y_length=6,
            axis_config={"color": GRAY},
            tips=False
        ).move_to(DOWN * 2.5)
        self.play(Create(axes))

        # Parameters
        R = 2
        t_vals = np.linspace(0, 2 * np.pi, 800)

        def param(t):
            x = 2 * R * np.cos(t) + R * np.cos(2 * t)
            y = 2 * R * np.sin(t) - R * np.sin(2 * t)
            return axes.c2p(x, y)

        points = [param(t) for t in t_vals]
        curve = VMobject(color=YELLOW).set_points_as_corners(points)

        self.play(Create(curve, run_time=6))
        self.wait(2)