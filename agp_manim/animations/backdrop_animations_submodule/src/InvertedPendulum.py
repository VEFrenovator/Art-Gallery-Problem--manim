from manim import *
import numpy as np

# Configuration
config.frame_width = 9
config.frame_height = 16
config.pixel_width = 1080
config.pixel_height = 1920
config.frame_rate = 30

class InvertedPendulum(Scene):
    def construct(self):
        self.camera.background_color = BLACK

        # Constants
        length = 2
        g = 9.8
        theta0 = 0.05  # Small initial angle deviation (radians)
        omega = 0

        # Title
        title = Text("Inverted Pendulum", color=WHITE, weight=BOLD).scale(1.2)
        title.move_to(UP * 3.5)
        self.play(Write(title))

        # Equation
        equation = MathTex(
            r"\ddot{\theta}(t) - \frac{g}{L} \sin(\theta(t)) = 0",  # inverted pendulum
            color=YELLOW
        ).scale(0.85).next_to(title, DOWN, buff=0.4)
        self.play(Write(equation))

        # Axes
        axes = Axes(
            x_range=[-4, 4],
            y_range=[-3, 6],
            x_length=6,
            y_length=6,
            axis_config={"color": GRAY},
            tips=False
        ).move_to(DOWN * 2.0)
        self.play(Create(axes))

        # Lower pendulum
        pendulum_offset = DOWN * 1.5
        theta_tracker = ValueTracker(theta0)

        def get_pendulum(theta):
            pivot = pendulum_offset
            bob = pivot + length * np.array([np.sin(theta), np.cos(theta), 0])
            rod = Line(pivot, bob, color=BLUE)
            ball = Dot(bob, radius=0.12, color=BLUE)
            return VGroup(rod, ball)

        pendulum = always_redraw(lambda: get_pendulum(theta_tracker.get_value()))
        pivot_dot = Dot(pendulum_offset, color=GRAY)

        path = TracedPath(lambda: get_pendulum(theta_tracker.get_value())[1].get_center(),
                          stroke_color=YELLOW, stroke_width=2)

        theta_display = always_redraw(
            lambda: MathTex(
                r"\theta = {:.2f}^\circ".format(np.degrees(theta_tracker.get_value())),
                color=YELLOW
            ).scale(0.85).next_to(equation, DOWN, buff=0.4)
        )

        self.add(pendulum, path, pivot_dot, theta_display)

        def update(dt):
            nonlocal omega
            theta = theta_tracker.get_value()
            alpha = (g / length) * np.sin(theta)  # positive sign for inverted
            omega += alpha * dt
            theta += omega * dt
            theta_tracker.set_value(theta)

        self.add_updater(update)
        self.wait(12)
        self.remove_updater(update)
