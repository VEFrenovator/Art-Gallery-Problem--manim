from manim import *
import numpy as np

# Video configuration (vertical)
config.frame_width = 9
config.frame_height = 16
config.pixel_width = 1080
config.pixel_height = 1920
config.frame_rate = 30

class FishCurve(Scene):
    def construct(self):
        self.camera.background_color = BLACK

        # Title and equations
        title = Text("The Fish Curve", color=WHITE, weight=BOLD).scale(1.2).move_to(UP * 3.5)
        self.play(Write(title))

        equation = MathTex(
            r"x = a(\cos(t) - \sin^2(t)/\sqrt{2})",
            color=YELLOW
        ).scale(0.8).next_to(title, DOWN, buff=0.4)

        a_label = MathTex(
            r"y = a\cos(t)\sin(t)",
            color=YELLOW
        ).scale(0.8).next_to(equation, DOWN, buff=0.4)

        self.play(Write(equation), Write(a_label))

        # Axes centered for fish shape
        axes = Axes(
            x_range=[-2, 9],
            y_range=[-5, 5],
            x_length=6,
            y_length=6,
            tips=False,
            axis_config={"color": GRAY}
        ).move_to(DOWN * 2.0)
        self.play(Create(axes))

        # Parameter values and colors
        a_values = np.linspace(1, 5, 8)
        colors = color_gradient([BLUE, TEAL, GREEN, YELLOW, ORANGE, RED], len(a_values))

        # Fish curve generator
        def fish_point(t, a):
            x = np.cos(t) - (np.sin(t) ** 2) / np.sqrt(2)
            y = np.cos(t) * np.sin(t)
            x_shifted = a * x + (0.75 * a)
            y_scaled = a * y
            return np.array([x_shifted, y_scaled, 0])

        # Plot fish curves
        for i, a in enumerate(a_values):
            curve = VMobject(color=colors[i], stroke_width=2.5)
            points = [axes.c2p(*fish_point(t, a)[:2]) for t in np.linspace(0, 2 * np.pi, 1000)]
            curve.set_points_smoothly(points)
            self.add(curve)
            self.wait(0.2)

        self.wait(2)
