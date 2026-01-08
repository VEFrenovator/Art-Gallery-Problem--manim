from manim import *
import numpy as np

# Vertical video configuration
config.frame_width = 9
config.frame_height = 16
config.pixel_width = 1080
config.pixel_height = 1920
config.frame_rate = 30

class SimplePendulum(Scene):
    def construct(self):
        self.camera.background_color = BLACK

        # Constants
        length = 3
        radius = 0.12
        pivot = ORIGIN
        theta0 = PI / 3
        g = 9.8

        # Title
        title = Text("Simple Pendulum", color=WHITE, weight=BOLD).scale(1.2)
        title.move_to(UP * 3.5)
        self.play(Write(title))

        # Equation
        equation = MathTex(r"\ddot{\theta}(t) + \frac{g}{L} \sin(\theta(t)) = 0", color=YELLOW)
        equation.scale(0.8).next_to(title, DOWN, buff=0.4)
        self.play(Write(equation))

        # Axes
        axes = Axes(
            x_range=[-4, 4],
            y_range=[-6, 2],
            x_length=6,
            y_length=6,
            tips=False,
            axis_config={"color": GRAY}
        ).move_to(DOWN * 2.0)
        self.play(Create(axes))

        # Tracker
        theta_tracker = ValueTracker(theta0)

        # Pendulum function
        def get_pendulum(theta):
            bob = pivot + length * np.array([np.sin(theta), -np.cos(theta), 0])
            rod = Line(pivot, bob, color=BLUE)
            ball = Dot(point=bob, radius=radius, color=BLUE)
            return VGroup(rod, ball)

        pendulum = always_redraw(lambda: get_pendulum(theta_tracker.get_value()))
        pivot_dot = Dot(pivot, color=GRAY)

        # Traced path
        path = TracedPath(
            lambda: get_pendulum(theta_tracker.get_value())[1].get_center(),
            stroke_color=YELLOW,
            stroke_width=2
        )

        # Live theta display
        theta_text = always_redraw(
            lambda: MathTex(
                r"\theta = " + f"{np.degrees(theta_tracker.get_value()):.1f}^\circ",
                color=YELLOW
            ).scale(0.85).next_to(equation, DOWN, buff=0.4)
        )

        self.add(pendulum, path, pivot_dot, theta_text)

        # Physics-based swing
        omega = 0  # angular velocity
        def swing_pendulum(dt):
            nonlocal omega
            theta = theta_tracker.get_value()
            alpha = -(g / length) * np.sin(theta)  # angular acceleration
            omega += alpha * dt
            theta += omega * dt
            theta_tracker.set_value(theta)

        self.add_updater(swing_pendulum)
        self.wait(12)
        self.remove_updater(swing_pendulum)
