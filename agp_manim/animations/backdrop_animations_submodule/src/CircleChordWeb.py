from manim import *
import numpy as np

config.frame_width = 9
config.frame_height = 16
config.pixel_width = 1080
config.pixel_height = 1920
config.frame_rate = 30

class CircleChordWeb(Scene):
    def construct(self):
        self.camera.background_color = BLACK
        title = Text("Circle Chord Web", color=WHITE, weight=BOLD).scale(1.2).move_to(UP * 3.5)
        self.play(Write(title))

        circle = Circle(radius=3, color=WHITE).move_to(DOWN * 1.5)
        self.play(Create(circle))

        n = 50
        points = [circle.point_at_angle(i * TAU / n) for i in range(n)]
        lines = VGroup()

        for i in range(n):
            for j in range(i + 1, n):
                line = Line(points[i], points[j], stroke_color=YELLOW, stroke_opacity=0.08)
                lines.add(line)

        self.play(Create(lines), run_time=5)
        self.wait()
