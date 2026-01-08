from manim import *
from math import comb

# Reel-friendly config
config.pixel_width = 1080
config.pixel_height = 1920
config.frame_width = 9
config.frame_height = 16

class PascalTriangle(Scene):
    def construct(self):
        self.camera.background_color = BLACK

        max_rows = 6
        triangle = self.generate_triangle(max_rows)

        # Title
        title = Text("Pascal's Triangle", color=WHITE, weight=BOLD).scale(1.2).move_to(UP * 3.5)
        subtitle = Text("Each number is the sum of two above it", color=YELLOW).scale(0.5).next_to(title, DOWN, buff=0.4)
        subtitle.next_to(title, DOWN, buff=0.3)

        self.add(title, subtitle)

        triangle.move_to(DOWN * 1)

        # Animate triangle row by row
        for i, row in enumerate(triangle):
            for j, cell in enumerate(row):
                if i == 0:
                    self.play(FadeIn(cell, scale=1.2), run_time=0.5)
                    self.wait(0.3)
                    continue

                if j == 0 or j == len(row) - 1:
                    self.play(FadeIn(cell, shift=UP * 0.3, scale=1.1), run_time=0.4)
                else:
                    # Animate sum arrows from above
                    top_left = triangle[i - 1][j - 1]
                    top_right = triangle[i - 1][j]
                    arrow1 = Arrow(start=top_left.get_bottom(), end=cell.get_top(), buff=0.1, color=BLUE_B, stroke_width=2.5)
                    arrow2 = Arrow(start=top_right.get_bottom(), end=cell.get_top(), buff=0.1, color=GREEN_B, stroke_width=2.5)

                    self.play(Create(arrow1), Create(arrow2), run_time=0.25)
                    self.play(FadeIn(cell, scale=1.1), run_time=0.4)
                    self.remove(arrow1, arrow2)

            self.wait(0.25)

    def generate_triangle(self, num_rows):
        triangle = VGroup()
        for row in range(num_rows):
            row_group = VGroup()
            for col in range(row + 1):
                val = comb(row, col)
                color = WHITE if val == 1 else YELLOW_B
                text = MathTex(str(val), color=color).scale(0.85)
                text.move_to(RIGHT * (col - row / 2) * 0.9 + DOWN * row * 0.9)
                row_group.add(text)
            triangle.add(row_group)
        return triangle