from manim import *
import numpy as np

# Vertical format
config.frame_width = 9
config.frame_height = 16
config.pixel_width = 1080
config.pixel_height = 1920
config.frame_rate = 30

class ComplexPolarSineCurve(Scene):
    def construct(self):
        self.camera.background_color = BLACK

        # Title and static equation
        title = Text("Polar Sine Curve", color=WHITE, weight=BOLD).scale(1.2)
        title.move_to(UP * 3.5)

        equation = MathTex(r"r(\theta) = 10 + \sin(2\pi\theta)", color=YELLOW).scale(0.8)
        equation.next_to(title, DOWN, buff=0.4)

        self.play(Write(title), Write(equation))

        # Polar plane
        axes = Axes(
            x_range=[-10, 10],
            y_range=[-10, 10],
            x_length=6,
            y_length=6,
            tips=False,
            axis_config={"color": GRAY},
        ).move_to(DOWN * 2.0)

        # Function and label to animate θ
        def r(theta):
            return 10 + np.sin(2 * np.pi * theta)

        theta_tracker = ValueTracker(0)
        theta_label = always_redraw(lambda: MathTex(
            r"\theta = " + f"{theta_tracker.get_value():.2f}",
            color=YELLOW
        ).scale(0.8).next_to(equation, DOWN, buff=0.4))

        self.play(Write(theta_label))

        # Path and updater to animate the polar plot
        path = VMobject(color=ORANGE, stroke_width=2)
        path.set_points_as_corners([axes.polar_to_point(r(0), 0)])  # initial point
        self.add(path)

        def update_path(mob):
            theta_vals = np.linspace(0, theta_tracker.get_value(), 1000)
            points = [axes.polar_to_point(r(theta), theta) for theta in theta_vals]
            if len(points) >= 2:
                mob.set_points_smoothly(points)

        path.add_updater(update_path)

        # Animate θ from 0 to 20π
        self.play(theta_tracker.animate.set_value(20 * np.pi), run_time=6, rate_func=linear)

        path.remove_updater(update_path)
        self.wait(2)
