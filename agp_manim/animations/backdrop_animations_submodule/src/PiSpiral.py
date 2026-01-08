from manim import *
import numpy as np

DIGIT_COLORS = {
    "0": BLUE_E, "1": ORANGE, "2": TEAL_B, "3": YELLOW_E, "4": RED_E,
    "5": GOLD_E, "6": GREEN_C, "7": PURPLE_B, "8": "#ADD8E6", "9": PINK, ".": WHITE
}

config.frame_width = 9
config.frame_height = 16
config.pixel_width = 1080
config.pixel_height = 1920
config.frame_rate = 30

class PiSpiral(Scene):
    def construct(self):
        self.camera.background_color = BLACK

        pi_digits = "3.14159265358979323846264338327950288419716939937510"

        shadow = MathTex(r"\pi", color=DARK_GRAY).scale(5).shift(0.07 * DOWN + 0.07 * RIGHT)
        main = MathTex(r"\pi", color=WHITE).scale(5)
        highlight = MathTex(r"\pi", color=BLUE_E).scale(5).set_opacity(0.2).shift(0.05 * UP + 0.05 * LEFT)
        symbol = VGroup(shadow, main, highlight)
        self.play(FadeIn(symbol))

        a, b = 1.75, 0.1
        spiral = VGroup()
        for i, d in enumerate(pi_digits):
            angle = i * 0.35
            r = a + b * angle
            pos = [r * np.cos(angle), r * np.sin(angle), 0]
            digit = Text(d, font="Monospace", color=DIGIT_COLORS.get(d, WHITE)).scale(0.5)
            digit.move_to(pos)
            digit.rotate(angle + PI / 2)
            spiral.add(digit)

        self.play(LaggedStartMap(FadeIn, spiral, lag_ratio=0.03), run_time=4)
        self.wait(2)
