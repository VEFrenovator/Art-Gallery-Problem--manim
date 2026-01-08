from manim import *
import math

config.frame_width = 9
config.frame_height = 16
config.pixel_width = 1080
config.pixel_height = 1920
config.frame_rate = 30

class TaylorSeriesCos(Scene):
    def construct(self):
        self.camera.background_color = BLACK
        title = Text("Taylor Series Approximation", color=WHITE, weight=BOLD).scale(0.75).move_to(UP * 3.5)
        equation = MathTex(r"f(x) = \cos(x)", color=YELLOW).scale(1.0).next_to(title, DOWN, buff=0.4)
        self.play(Write(title), Write(equation))

        axes = Axes(
            x_range=[-PI, PI], 
            y_range=[-1.5, 1.5], 
            x_length=6, 
            y_length=3,
            axis_config={"color": GRAY}, 
            tips=False
        ).move_to(DOWN * 1.0)
        self.play(Create(axes))

        graph = axes.plot(lambda x: np.cos(x), color=YELLOW)
        self.play(Create(graph))

        def taylor_cos(x, n):
            return sum(((-1)**(k//2)) * x**k / math.factorial(k) for k in range(n+1) if k % 2 == 0)

        for i, deg in enumerate([0, 2, 4, 6]):
            approx = axes.plot(lambda x: taylor_cos(x, deg), color=BLUE_D)
            label = MathTex(f"T_{{{deg}}}(x)").scale(0.6).next_to(approx.get_end(), RIGHT)
            self.play(Create(approx), FadeIn(label))
            self.wait(0.5)
        self.wait()
