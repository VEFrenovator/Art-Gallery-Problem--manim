from manim import *
import numpy as np

# Vertical video configuration
config.frame_width = 9
config.frame_height = 16
config.pixel_width = 1080
config.pixel_height = 1920
config.frame_rate = 30

class ButterflyCurve2(Scene):
    def construct(self):
        self.camera.background_color = BLACK

        # Title
        title = Text("Butterfly Curve", color=WHITE, weight=BOLD).scale(1.2).move_to(UP * 3.5)
        self.play(Write(title))
        self.add(title)

        # Equation
        equation = MathTex(
            r"r = e^{\sin(\theta)} - 2\cos(4\theta) + 5\left(\sin\left(\frac{2\theta - \pi}{24}\right)\right)^5",
            color=YELLOW
        ).scale(0.8).next_to(title, DOWN, buff=0.4)
        self.play(Write(equation))
        self.add(equation)

        # Polar coordinate grid
        axes = PolarPlane(
            size=3.75,
        ).move_to(DOWN * 2.5)

        # Polar butterfly function
        def butterfly(theta):
            r = (
                np.exp(np.sin(theta))
                - 2 * np.cos(4 * theta)
                + 5 * (np.sin((2 * theta - np.pi) / 24)) ** 5
            )
            x = r * np.cos(theta)
            y = r * np.sin(theta)
            return axes.c2p(x, y)

        # Curve and animated dot
        curve = VMobject(color=ORANGE, stroke_width=4)
        dot = Dot(color=WHITE).scale(0.5)
        theta_tracker = ValueTracker(0)

        # Curve updater
        curve.add_updater(
            lambda m: m.set_points_as_corners(
                [butterfly(t) for t in np.linspace(0, theta_tracker.get_value(), 300)]
            )
        )

        # Dot updater
        dot.add_updater(lambda m: m.move_to(butterfly(theta_tracker.get_value())))

        # Theta label
        theta_label = always_redraw(
            lambda: MathTex(
                r"\theta = " + f"{theta_tracker.get_value():.2f}",
                color=YELLOW
            ).scale(0.8).next_to(equation, DOWN, buff=0.4)
        )

        self.add(curve, dot, theta_label)
        self.play(theta_tracker.animate.set_value(12 * PI), run_time=6, rate_func=linear)
        self.wait(2)
