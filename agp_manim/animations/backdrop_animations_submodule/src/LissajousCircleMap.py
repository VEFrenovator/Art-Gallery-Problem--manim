from manim import *
import numpy as np

config.frame_width = 9
config.frame_height = 16
config.pixel_width = 1080
config.pixel_height = 1920
config.frame_rate = 30

class LissajousCircleMap(Scene):
    def construct(self):
        self.camera.background_color = BLACK

        title = Text("Lissajous Circle Map", color=WHITE, weight=BOLD).scale(1.2).move_to(UP * 3.5)
        self.play(Write(title))

        circle = Circle(radius=3, color=WHITE)
        circle.move_to(DOWN * 1.5)
        self.play(Create(circle))

        n = 200
        a = 3
        b = 2
        lines = VGroup()

        for i in range(n):
            start_angle = i * TAU / n
            end_angle = ((a * i + b) % n) * TAU / n
            start = circle.point_at_angle(start_angle)
            end = circle.point_at_angle(end_angle)
            line = Line(start, end, stroke_color=YELLOW, stroke_opacity=0.3)
            lines.add(line)

        self.play(Create(lines), run_time=4)
        self.wait()
