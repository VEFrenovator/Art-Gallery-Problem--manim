from manim import *
import numpy as np

# Vertical video configuration
config.frame_width = 9
config.frame_height = 16
config.pixel_width = 1080
config.pixel_height = 1920
config.frame_rate = 30

class CircularSwirlField(Scene):
    def construct(self):
        self.camera.background_color = BLACK

        # Title and equation
        title = Text("Circular Swirl Field", color=WHITE, weight=BOLD).scale(1.2).move_to(UP * 3.5)
        equation = MathTex(r"\vec{F}(x, y) = (-y, x)", color=YELLOW).scale(0.8).next_to(title, DOWN, buff=0.4)
        self.play(Write(title), Write(equation))

        # Define the swirl vector field
        def swirl_field(pos):
            x, y = pos[:2]
            return np.array([-y, x, 0])

        # Streamlines visualization
        stream_lines = StreamLines(
            swirl_field,
            x_range=[-4, 4, 0.4],
            y_range=[-4, 4, 0.4],
            stroke_width=1.2,
            max_anchors_per_line=50,
            virtual_time=4,
            dt=0.05,
            color=PURPLE,
        ).scale(0.6).move_to(DOWN * 2.0)

        # Add streamlines
        self.add(stream_lines)

        # Animate streamlines
        stream_lines.start_animation(
            flow_speed=1.0,
            time_width=1.2,
        )

        self.wait(6)

        # Remove all elements
        self.play(
            AnimationGroup(
                Unwrite(title),
                Unwrite(equation),
                stream_lines.end_animation(),
            )
        )
