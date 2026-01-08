from manim import *
import numpy as np

# Vertical video formatting
config.frame_width = 9
config.frame_height = 16
config.pixel_width = 1080
config.pixel_height = 1920
config.frame_rate = 30

class HarmonicGrid(Scene):
    def construct(self):
        self.camera.background_color = BLACK

        # Title
        title = Text("Harmonic Grid", color=WHITE, weight=BOLD).scale(1.2)
        title.move_to(UP * 3.5)
        self.play(Write(title))

        # Equation
        equation = MathTex(r"a \cdot \sin(x) + \sin(y) = 0", color=YELLOW).scale(0.8)
        equation.next_to(title, DOWN, buff=0.4)
        self.play(Write(equation))

        # Axes setup
        axes = Axes(
            x_range=[-8, 8],
            y_range=[-8, 8],
            x_length=6,
            y_length=6,
            tips=False,
            axis_config={"color": GRAY}
        ).move_to(DOWN * 2)
        self.play(Create(axes))

        # Parameter a values
        a_values = [0.5,0.6,0.7,0.8,0.9,1]
        colors = color_gradient([BLUE, GREEN, YELLOW, ORANGE, RED], len(a_values))

        # Display label for changing 'a'
        a_label = MathTex("a = 0.5", color=YELLOW).scale(0.85)
        a_label.next_to(equation, DOWN, buff=0.4)
        self.play(Write(a_label))

        for i, a in enumerate(a_values):
            new_label = MathTex(f"a = {a}", color=YELLOW).scale(0.85)
            new_label.move_to(a_label.get_center())

            def func(x, y, a=a):
                return a * np.sin(x) + np.sin(y)

            # Plot the implicit curve
            curve = axes.plot_implicit_curve(
                lambda x, y: func(x, y),
                color=colors[i],
                stroke_width=2.5,
                min_depth=0.01,
            )

            self.play(Transform(a_label, new_label), Create(curve), run_time=1.2)
            self.add(curve)
            self.wait(0.2)

        self.wait(2)
