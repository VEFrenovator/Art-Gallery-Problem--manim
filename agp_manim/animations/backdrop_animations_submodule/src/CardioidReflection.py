from manim import *
import numpy as np

config.frame_width = 9
config.frame_height = 16
config.pixel_width = 1080
config.pixel_height = 1920
config.frame_rate = 30

class CardioidReflection(Scene):
    def construct(self):
        self.camera.background_color = BLACK
        title = Text("Cardioid Reflection", color=WHITE, weight=BOLD).scale(1.2).move_to(UP * 3.5)
        self.play(Write(title))

        
        circle = Circle(radius=3, color=WHITE)
        circle.move_to(DOWN * 1.5)
        self.play(Create(circle))

        n = 120
        lines = VGroup()
        for i in range(1, n + 1):
            start_angle = i * TAU / n
            end_angle = (2 * i) % n * TAU / n
            start = circle.point_at_angle(start_angle)
            end = circle.point_at_angle(end_angle)
            line = Line(start, end, stroke_color=YELLOW, stroke_opacity=0.4)
            lines.add(line)

        self.play(Create(lines), run_time=3)
        self.wait()
