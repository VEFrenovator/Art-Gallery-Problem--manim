from manim import *
import numpy as np

# Vertical video configuration
config.frame_width = 9
config.frame_height = 16
config.pixel_width = 1080
config.pixel_height = 1920
config.frame_rate = 30

class FermatsSpiral(Scene):
    def construct(self):
        self.camera.background_color = BLACK

        # Title
        title = Text("Fermat's Spiral", color=WHITE, weight=BOLD).scale(1.2)
        title.move_to(UP * 3.5)
        self.play(Write(title))

        # Equation
        equation = MathTex(
            r"r(\theta) = \sqrt{\theta}",
            color=YELLOW
        ).scale(0.85).next_to(title, DOWN, buff=0.4)
        self.play(Write(equation))

        # Axes
        axes = Axes(
            x_range=[-6, 6],
            y_range=[-6, 6],
            x_length=6,
            y_length=6,
            axis_config={"color": GRAY},
            tips=False
        ).move_to(DOWN * 2.5)
        self.play(Create(axes))

        # Fermat's spiral parametric form
        def r(theta):
            return np.sqrt(theta)

        t_vals = np.linspace(0, 8 * PI, 1000)
        points = [axes.c2p(r(t) * np.cos(t), r(t) * np.sin(t)) for t in t_vals]

        spiral = VMobject(color=YELLOW).set_points_as_corners(points)
        self.play(Create(spiral, run_time=6))
        self.wait(2)