from manim import *
import numpy as np

config.frame_width = 9
config.frame_height = 16
config.pixel_width = 1080
config.pixel_height = 1920
config.frame_rate = 30

class Torus3D(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=60 * DEGREES, theta=30 * DEGREES)
        self.camera.background_color = BLACK

        # Fixed title and subtitle
        title = Text("3D Torus Visualization", color=WHITE, weight=BOLD).scale(1.).move_to(UP * 4.)
        subtitle = Text("Parametric Surface: Toroidal Shape", color=YELLOW).scale(0.8).next_to(title, DOWN, buff=0.4)
        torus_eq = MathTex(
            r"""
            \begin{cases}
            x(u,v) = (R + r \cos v)\cos u \\
            y(u,v) = (R + r \cos v)\sin u \\
            z(u,v) = r \sin v
            \end{cases}
            """, color=YELLOW).scale(0.8).next_to(subtitle, DOWN, buff=0.4)

        self.add_fixed_in_frame_mobjects(title, subtitle, torus_eq)
        self.play(Write(title), Write(subtitle), Write(torus_eq))

        # Axes
        axes = ThreeDAxes(
            x_range=[-5, 5], 
            y_range=[-5, 5], 
            z_range=[-5, 5],
            x_length=7, 
            y_length=7, 
            z_length=6,
            tips=False,
            axis_config={"color": GRAY}
        ).shift(- OUT * 2.75)

        # Torus params
        R = 2
        r = 0.7

        torus = Surface(
            lambda u, v: np.array([
                (R + r * np.cos(v)) * np.cos(u),
                (R + r * np.cos(v)) * np.sin(u),
                r * np.sin(v)
            ]),
            u_range=[0, TAU],
            v_range=[0, TAU],
            resolution=(42, 18),
            fill_opacity=0.9,
            checkerboard_colors=[BLUE_D, BLUE_E],
            stroke_color=GRAY_E,
        ).shift(- OUT * 2.25)

        self.play(FadeIn(torus, scale=0.3))
        self.add(axes)
        self.bring_to_front(axes)

        # Rotate torus only (not axes)
        self.play(Rotate(torus, angle=2 * PI, axis=OUT, run_time=10))

        self.wait(2)
