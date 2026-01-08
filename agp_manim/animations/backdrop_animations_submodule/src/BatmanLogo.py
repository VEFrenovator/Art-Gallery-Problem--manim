from manim import *
import numpy as np

# Video render settings
config.frame_width = 9
config.frame_height = 16
config.pixel_width = 1080
config.pixel_height = 1920
config.frame_rate = 30

class BatmanLogo(Scene):
    def construct(self):
        self.camera.background_color = BLACK
        epsilon = 1e-6  # For numerical stability

        def safe_sqrt(x):
            return np.nan_to_num(np.sqrt(np.maximum(0, x)), nan=0.0, posinf=0.0, neginf=0.0)

        def clip_near(val, target, thresh=1e-2):
            return np.abs(val - target) < thresh

        y_range = [-5, 5]

        # Math equations displayed while drawing
        equations = [
            r"\left(\frac{x}{7}\right)^2 \sqrt{\frac{||x|-3|}{|x|-3}} + \left(\frac{y}{3}\right)^2 \sqrt{\frac{|y + \frac{3}{7}\sqrt{33}|}{y + \frac{3}{7}\sqrt{33}}} = 1",
            r"\left|\frac{x}{2}\right| - \left(\frac{3\sqrt{33}-7}{112}\right)x^2 + \sqrt{1 - (||x|-2| - 1)^2} = y + 3",
            r"9 \sqrt{\frac{|(|x|-1)(|x|-0.75)|}{(1-|x|)(|x|-0.75)}} - 8|x| = y",
            r"9 \sqrt{\frac{|(|x|-1)(|x|-0.75)|}{(1-|x|)(|x|-0.75)}} - 8|x| = y",
            r"3|x| + 0.75 \sqrt{\frac{(|x|-0.75)(|x|-0.5)}{(0.75-|x|)(|x|-0.5)}} = y",
            r"2.25 \sqrt{\frac{(x-0.5)(x+0.5)}{(0.5-x)(0.5+x)}} = y",
            r"\frac{6\sqrt{10}}{7} + (1.5 - 0.5|x|)\sqrt{\frac{||x|-1|}{|x|-1}} - \frac{6\sqrt{10}}{14} \sqrt{4 - (|x|-1)^2} = y",
            r"\frac{6\sqrt{10}}{7} + (1.5 - 0.5|x|)\sqrt{\frac{||x|-1|}{|x|-1}} - \frac{6\sqrt{10}}{14} \sqrt{4 - (|x|-1)^2} = y"
        ]

        # List of implicit curve definitions and their plotting bounds
        segments = [
            # Top arc of the wings
            (
                lambda x, y: ((x / 7) ** 2 * safe_sqrt(np.abs(np.abs(x) - 3) / (np.abs(x) - 3 + epsilon)) +
                              (y / 3) ** 2 * safe_sqrt(np.abs(y + 3 / 7 * np.sqrt(33)) / (y + 3 / 7 * np.sqrt(33) + epsilon)) - 1),
                [-8, 8],
                [-3 * np.sqrt(33) / 7, 6 - 4 * np.sqrt(33) / 7]
            ),
            # Upper wings
            (
                lambda x, y: (np.abs(x / 2) - ((3 * np.sqrt(33) - 7) / 112) * x ** 2 +
                              safe_sqrt(1 - (np.abs(np.abs(x) - 2) - 1) ** 2) - y - 3),
                [-4.05, 4.05],
                y_range
            ),
            # Outer lower wings (left)
            (
                lambda x, y: (
                    np.nan if clip_near(np.abs(x), 0.75) or clip_near(np.abs(x), 1) else
                    9 * safe_sqrt(np.abs((np.abs(x) - 1)*(np.abs(x) - 0.75)) /
                                  ((1 - np.abs(x))*(np.abs(x) - 0.75 + epsilon))) - 8 * np.abs(x) - y
                ),
                [-1.05, -0.7],
                y_range
            ),
            # Outer lower wings (right)
            (
                lambda x, y: (
                    np.nan if clip_near(np.abs(x), 0.75) or clip_near(np.abs(x), 1) else
                    9 * safe_sqrt(np.abs((np.abs(x) - 1)*(np.abs(x) - 0.75)) /
                                  ((1 - np.abs(x))*(np.abs(x) - 0.75 + epsilon))) - 8 * np.abs(x) - y
                ),
                [0.7, 1.05],
                y_range
            ),
            # Inner lower wings
            (
                lambda x, y: (
                    np.nan if clip_near(np.abs(x), 0.5) or clip_near(np.abs(x), 0.75) else
                    3 * np.abs(x) + 0.75 * safe_sqrt(np.abs((np.abs(x) - 0.75)*(np.abs(x) - 0.5)) /
                                                     ((0.75 - np.abs(x)) * (np.abs(x) - 0.5 + epsilon))) - y
                ),
                [-0.76, 0.76],
                [2.25, 5]
            ),
            # Central dip
            (
                lambda x, y: (
                    np.nan if clip_near(np.abs(x), 0.5) else
                    2.25 * safe_sqrt(np.abs((x - 0.5)*(x + 0.5) / ((0.5 - x)*(0.5 + x + epsilon)))) - y
                ),
                [-0.51, 0.51],
                y_range
            ),
            # Tail curve (left)
            (
                lambda x, y: (
                    np.nan if clip_near(np.abs(x), 1) else
                    6 * np.sqrt(10) / 7 + (1.5 - 0.5 * np.abs(x)) *
                    safe_sqrt(np.abs(np.abs(x) - 1) / (np.abs(x) - 1 + epsilon)) -
                    (6 * np.sqrt(10) / 14) * safe_sqrt(4 - (np.abs(x) - 1) ** 2) - y
                ),
                [-3.05, -1.0],
                y_range
            ),
            # Tail curve (right)
            (
                lambda x, y: (
                    np.nan if clip_near(np.abs(x), 1) else
                    6 * np.sqrt(10) / 7 + (1.5 - 0.5 * np.abs(x)) *
                    safe_sqrt(np.abs(np.abs(x) - 1) / (np.abs(x) - 1 + epsilon)) -
                    (6 * np.sqrt(10) / 14) * safe_sqrt(4 - (np.abs(x) - 1) ** 2) - y
                ),
                [1.0, 3.05],
                y_range
            )
        ]

        # Title display
        title = Text("Batman Logo", color=WHITE, weight=BOLD).scale(1.2)
        title.move_to(UP * 3.5)
        self.play(Write(title))

        # Create each part of the Batman shape
        curves = [
            ImplicitFunction(
                func,
                x_range=xr,
                y_range=yr,
                color=YELLOW,
                stroke_width=2,
                min_depth=4,
                max_quads=10000
            )
            for func, xr, yr in segments
        ]

        batman = VGroup(*curves).scale(0.6).move_to(DOWN * 2.0)

        # Animate each labeled curve one at a time
        labels = [
            MathTex(eq, color=YELLOW).scale(0.6).next_to(title, DOWN, buff=0.4)
            for eq in equations
        ]

        for curve, label in zip(curves, labels):
            self.play(Write(label), Create(curve), run_time=1.2)
            self.wait(0.2)
            self.play(FadeOut(label), run_time=0.5)

        self.wait(2)
