from manim import *
import numpy as np

# Vertical video configuration
config.frame_width = 9
config.frame_height = 16
config.pixel_width = 1080
config.pixel_height = 1920
config.frame_rate = 30

class DoublePendulum(Scene):
    def construct(self):
        self.camera.background_color = BLACK

        # Physical constants
        l1, l2 = 2, 1.5
        m1, m2 = 1, 1
        g = 9.8

        # Initial conditions
        theta1, theta2 = np.pi / 2, np.pi / 2
        omega1, omega2 = 0, 0

        # Title and equation
        title = Text("Double Pendulum", color=WHITE, weight=BOLD).scale(1.2).move_to(UP * 3.5)
        self.play(Write(title))

        eq = MathTex(r"\text{Nonlinear ODEs: Complex System}", color=YELLOW).scale(0.7).next_to(title, DOWN, buff=0.3)
        self.play(Write(eq))

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

        # Trackers
        theta1_tracker = ValueTracker(theta1)
        theta2_tracker = ValueTracker(theta2)

        # Pendulum components
        def get_position():
            t1 = theta1_tracker.get_value()
            t2 = theta2_tracker.get_value()

            x1, y1 = l1 * np.sin(t1), -l1 * np.cos(t1)
            x2, y2 = x1 + l2 * np.sin(t2), y1 - l2 * np.cos(t2)

            bob1 = np.array([x1, y1, 0])
            bob2 = np.array([x2, y2, 0])

            line1 = Line(ORIGIN, bob1, color=BLUE)
            line2 = Line(bob1, bob2, color=BLUE)
            dot1 = Dot(bob1, radius=0.12, color=BLUE)
            dot2 = Dot(bob2, radius=0.12, color=BLUE)

            return VGroup(line1, line2, dot1, dot2)

        pendulum = always_redraw(get_position)
        path = TracedPath(lambda: get_position()[3].get_center(), stroke_color=YELLOW, stroke_width=2)
        pivot = Dot(ORIGIN, color=GRAY)

        self.add(pendulum, path, pivot)

        # Physics update function
        def update_pendulum(dt):
            nonlocal theta1, theta2, omega1, omega2
            delta = theta2 - theta1

            den1 = (m1 + m2) * l1 - m2 * l1 * np.cos(delta)**2
            den2 = (l2 / l1) * den1

            a1 = (
                m2 * l1 * omega1**2 * np.sin(delta) * np.cos(delta)
                + m2 * g * np.sin(theta2) * np.cos(delta)
                + m2 * l2 * omega2**2 * np.sin(delta)
                - (m1 + m2) * g * np.sin(theta1)
            ) / den1

            a2 = (
                -m2 * l2 * omega2**2 * np.sin(delta) * np.cos(delta)
                + (m1 + m2) * g * np.sin(theta1) * np.cos(delta)
                - (m1 + m2) * l1 * omega1**2 * np.sin(delta)
                - (m1 + m2) * g * np.sin(theta2)
            ) / den2

            omega1 += a1 * dt
            omega2 += a2 * dt
            theta1 += omega1 * dt
            theta2 += omega2 * dt

            theta1_tracker.set_value(theta1)
            theta2_tracker.set_value(theta2)

        self.add_updater(update_pendulum)
        self.wait(12)
        self.remove_updater(update_pendulum)
