from manim import *

config.frame_width = 9
config.frame_height = 16
config.pixel_width = 1080
config.pixel_height = 1920
config.frame_rate = 30

class PolarVsCartesian2(Scene):
    def construct(self):
        # === 1. Title ===
        title = Text("Cartesian vs Polar", color=WHITE).scale(0.8).move_to(UP * 5)
        self.play(Write(title))
        self.wait(1)

        # === 2. Show Both Equations ===
        cartesian_label = MathTex(
            r"y(x) = 3.5 \sin[3.73 \cdot \cos(1.78x)]",
            font_size=36
        ).move_to(UP * 3.8)

        polar_label = MathTex(
            r"r(\theta) = 3.5 \sin[3.73 \cdot \cos(1.78\theta)]",
            font_size=36
        ).move_to(DOWN * -0.1)

        self.play(Write(cartesian_label), Write(polar_label))
        self.wait(1.2)

        # === 3. Show Both Axes ===
        cartesian_axes = Axes(
            x_range=[0, 10 * PI],
            y_range=[-4, 4],
            x_length=6.5,
            y_length=3.0,
            axis_config={"color": GRAY},
            tips=False
        ).scale(0.85).move_to(UP * 2.2)

        polar_axes = PolarPlane(
            size=5.0,
            radius_max=4,
            azimuth_units="degrees",
            background_line_style={"stroke_color": GRAY, "stroke_opacity": 0.5}
        ).move_to(DOWN * 3.0)

        self.play(Create(cartesian_axes), Create(polar_axes))
        self.wait(1)

        # === 4. Plot Both Graphs Together ===
        cartesian_func = cartesian_axes.plot(
            lambda x: 3.5 * np.sin(3.73 * np.cos(1.78 * x)),
            x_range=[0, 10 * PI],
            color=BLUE
        )

        polar_func = polar_axes.plot_polar_graph(
            lambda theta: 3.5 * np.sin(3.73 * np.cos(1.78 * theta)),
            theta_range=[0, 10 * PI],
            color=YELLOW,
            stroke_width=2
        )

        self.play(Create(cartesian_func), Create(polar_func), run_time=8)
        self.wait(2)
