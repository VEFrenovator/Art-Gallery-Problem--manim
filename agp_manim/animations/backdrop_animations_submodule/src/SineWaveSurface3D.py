from manim import *
import numpy as np

config.frame_width = 9
config.frame_height = 16
config.pixel_width = 1080
config.pixel_height = 1920
config.frame_rate = 30

class SineWaveSurface3D(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=65 * DEGREES, theta=35 * DEGREES)
        self.camera.background_color = BLACK

        # Title and subtitle
        title = Text("3D Sine Wave", color=WHITE, weight=BOLD).scale(1).move_to(UP * 4)
        subtitle = Text("Sinusoidal Surface", color=YELLOW).scale(0.7).next_to(title, DOWN, buff=0.4)

        equation = MathTex(
            r"z = \sin(x) \cdot \cos(y)", color=YELLOW
        ).scale(0.9).next_to(subtitle, DOWN, buff=0.4)

        self.add_fixed_in_frame_mobjects(title, subtitle, equation)
        self.play(Write(title), Write(subtitle), Write(equation))

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
        ).shift(-OUT * 2.75)

        # Smaller sine surface
        sine_surface = Surface(
            lambda u, v: np.array([
                u,
                v,
                np.sin(u) * np.cos(v)
            ]),
            u_range=[-3, 3],
            v_range=[-3, 3],
            resolution=(42, 18),
            fill_opacity=0.9,
            checkerboard_colors=[BLUE_D, BLUE_E],
            stroke_color=GRAY_E,
        ).shift(-OUT * 2.25)

        self.play(FadeIn(sine_surface, scale=1))
        self.add(axes)
        self.bring_to_front(axes)

        # Rotate the surface
        self.play(Rotate(sine_surface, angle=2 * PI, axis=OUT, run_time=10))
        self.wait(2)
