from manim import *
import numpy as np

# Vertical video configuration
config.frame_width = 9
config.frame_height = 16
config.pixel_width = 1080
config.pixel_height = 1920
config.frame_rate = 30

class RadialSinkField(Scene):
    def construct(self):
        self.camera.background_color = BLACK

        # Title and equation
        title = Text("Radial Sink Field", color=WHITE, weight=BOLD).scale(1.2).move_to(UP * 3.5)
        self.play(Write(title))

        equation = MathTex(
            r"\vec{F}(x, y) = \left(",
            r"-\frac{x}{\sqrt{x^2 + y^2}}, \quad -\frac{y}{\sqrt{x^2 + y^2}}",
            r"\right)",
            color=YELLOW
        ).scale(0.8).next_to(title, DOWN, buff=0.4)
        self.play(Write(equation))

        # Radial sink vector field
        def sink_field(pos):
            x, y = pos[:2]
            r = np.sqrt(x**2 + y**2) + 0.1  # avoid division by zero
            return np.array([-x / r, -y / r, 0])

        # Streamlines
        stream_lines = StreamLines(
            sink_field,
            x_range=[-4, 4, 0.3],
            y_range=[-4, 4, 0.3],
            stroke_width=1.2,
            max_anchors_per_line=50,
            virtual_time=4,
            dt=0.05,
            color=PURPLE,
        ).scale(0.8).move_to(DOWN * 2.0)

        self.add(stream_lines)

        # Flow animation
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
