from manim import *
import numpy as np

# Vertical video config
config.frame_width = 9
config.frame_height = 16
config.pixel_width = 1080
config.pixel_height = 1920
config.frame_rate = 30

class MobiusShape(Scene):
    def construct(self):
        self.camera.background_color = BLACK

        # Title
        title = Text("Möbius Bloom", color=WHITE, weight=BOLD).scale(1.2)
        title.move_to(UP * 3.5)
        equation = MathTex(r"f(z) = \frac{z^2 - 1}{z^2 + 1}", color=YELLOW).scale(0.8).next_to(title, DOWN, buff=0.3)
        equation.next_to(title, DOWN, buff=0.4)
        self.play(Write(title), Write(equation))

        # Complex plane
        plane = ComplexPlane(
            x_range=[-2, 2],
            y_range=[-2, 2],
            x_length=6, 
            y_length=6,
            axis_config={"color": GRAY},
            tips=False
        ).move_to(DOWN * 2)
        self.play(Create(plane))

        # Grid of points with color gradient
        dots = VGroup()
        grid = np.linspace(-2, 2, 24)
        total = len(grid) ** 2
        for i, x in enumerate(grid):
            for j, y in enumerate(grid):
                z = complex(x, y)
                if abs(z) < 0.05:
                    continue
                color = interpolate_color(BLUE, RED, (i * len(grid) + j) / total)
                dot = Dot(plane.c2p(x, y), radius=0.035)
                dot.z_complex = z
                dots.add(dot)

        self.add(dots)

        # Mapping function: Möbius transformation
        def f(z):
            return (z**2 - 1) / (z**2 + 1)

        self.play(
            *[
                dot.animate.move_to(
                    plane.c2p(np.real(f(dot.z_complex)), np.imag(f(dot.z_complex)))
                )
                for dot in dots
            ],
            run_time=6,
            rate_func=smooth
        )
        self.wait(2)