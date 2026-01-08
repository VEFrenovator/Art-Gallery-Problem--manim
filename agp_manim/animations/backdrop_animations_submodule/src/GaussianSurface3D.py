from manim import *
import numpy as np

# Configuration
config.frame_width = 9
config.frame_height = 16
config.pixel_width = 1080
config.pixel_height = 1920
config.frame_rate = 30

class GaussianSurface3D(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=70 * DEGREES, theta=45 * DEGREES)
        self.camera.background_color = BLACK

        # Title and Subtitle
        title = Text("3D Gaussian Surface", color=WHITE, weight=BOLD).scale(1).move_to(UP * 4)
        subtitle = Text("Gaussian Distribution Surface", color=YELLOW).scale(0.7).next_to(title, DOWN, buff=0.4)

        equation = MathTex(
            r"z(x, y) = 2 e^{-(x^2 + y^2)}",
            color=YELLOW
        ).scale(0.8).next_to(subtitle, DOWN, buff=0.4)

        self.add_fixed_in_frame_mobjects(title, subtitle, equation)
        self.play(Write(title), Write(subtitle), Write(equation))

        # Axes
        axes = ThreeDAxes(
            x_range=[-3, 3],
            y_range=[-3, 3],
            z_range=[0, 2.5],
            x_length=6,
            y_length=6,
            z_length=4,
            tips=False,
            axis_config={"color": GRAY}
        ).shift(-OUT * 2.75)

        self.add(axes)
        self.bring_to_front(axes)

        def gaussian(x, y):
            return 2 * np.exp(-(x**2 + y**2))

        surface = Surface(
            lambda u, v: np.array([u, v, gaussian(u, v)]),
            u_range=[-2.5, 2.5],
            v_range=[-2.5, 2.5],
            resolution=(64, 32),
            fill_opacity=0.9,
            checkerboard_colors=[BLUE_D, BLUE_E],
            stroke_color=GRAY_E,
        ).shift(-OUT * 2.25)

        self.play(FadeIn(surface, scale=0.3))
        self.begin_ambient_camera_rotation(rate=0.1)
        self.wait(10)
        self.stop_ambient_camera_rotation()
        self.wait(2)
