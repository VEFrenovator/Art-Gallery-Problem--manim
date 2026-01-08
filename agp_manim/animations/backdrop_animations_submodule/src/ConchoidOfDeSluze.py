from manim import *
import numpy as np

# Vertical video configuration
config.frame_width = 9
config.frame_height = 16
config.pixel_width = 1080
config.pixel_height = 1920
config.frame_rate = 30

class ConchoidOfDeSluze(Scene):
    def construct(self):
        self.camera.background_color = BLACK

        # Title
        title = Text("Conchoid of de Sluze", color=WHITE, weight=BOLD).scale(1.2)
        title.move_to(UP * 3.5)
        self.play(Write(title))

        # Equation display
        eq = MathTex(r"(x - 1)(x^2 + y^2) - a x^2 = 0", color=YELLOW).scale(0.8).next_to(title, DOWN, buff=0.4)
        eq.next_to(title, DOWN, buff=0.4)
        self.play(Write(eq))

        # Axes
        axes = Axes(
            x_range=[-7, 12],
            y_range=[-10, 10],
            x_length=6,
            y_length=6,
            tips=False,
            axis_config={"color": GRAY}
        ).move_to(DOWN * 2)
        self.play(Create(axes))

        # Parameters
        a_values = list(range(-7, 11))
        colors = color_gradient([BLUE, GREEN, YELLOW, ORANGE, RED], len(a_values))

        # a-Label
        a_label = MathTex("a = 0", color=YELLOW).scale(0.85)
        a_label.next_to(eq, DOWN, buff=0.4)
        self.play(Write(a_label))

        # Animate curve family
        for i, a in enumerate(a_values):
            new_label = MathTex(f"a = {a}", color=YELLOW).scale(0.85)
            new_label.move_to(a_label.get_center())

            def f(x, y, a=a):
                return (x - 1)*(x**2 + y**2) - a * x**2

            curve = axes.plot_implicit_curve(
                lambda x, y: f(x, y),
                color=colors[i],
                stroke_width=2.5,
                min_depth=0.01
            )

            self.play(Transform(a_label, new_label), Create(curve), run_time=1.2)
            self.add(curve)

        self.wait(2)
