from manim import *
import numpy as np

# Vertical video configuration
config.frame_width = 9
config.frame_height = 16
config.pixel_width = 1080
config.pixel_height = 1920
config.frame_rate = 30

class DurerFolium(Scene):
    def construct(self):
        self.camera.background_color = BLACK

        # Title and formula
        title = Text("The Dürer Folium", color=WHITE, weight=BOLD).scale(1.2).move_to(UP * 3.5)
        formula = MathTex(
            r"a^4 y^2 + 4(x^2 + y^2)^3 - 4a^2(x^2 + y^2)^2 = 0",
            color=YELLOW
        ).scale(0.8).next_to(title, DOWN, buff=0.4)
        self.play(Write(title), Write(formula))

        # Axes
        axes = Axes(
            x_range=[-11, 11],
            y_range=[-11, 11],
            x_length=6,
            y_length=6,
            axis_config={"color": GRAY},
            tips=False
        ).move_to(DOWN * 2.0)
        self.play(Create(axes))

        # Parameter label
        a_label = MathTex("a = 0", color=YELLOW).scale(0.85).next_to(formula, DOWN, buff=0.4)
        self.play(Write(a_label))

        # Values for a and color mapping
        a_values = [3, 4, 5, 6, 7, 8, 9, 10]
        colors = color_gradient([BLUE, TEAL, GREEN, YELLOW, ORANGE, RED], len(a_values))

        # Curve animation
        for i, a in enumerate(a_values):
            new_label = MathTex(f"a = {a}", color=YELLOW).scale(0.85).move_to(a_label.get_center())

            def folium_fn(x, y):
                r2 = x**2 + y**2
                return a**4 * y**2 + 4 * r2**3 - 4 * a**2 * r2**2

            curve = axes.plot_implicit_curve(
                folium_fn,
                color=colors[i],
                stroke_width=2.5,
                min_depth=0.01
            )

            self.play(Transform(a_label, new_label), Create(curve), run_time=1.2)
            self.add(curve)
            self.wait(0.2)

        self.wait(2)
