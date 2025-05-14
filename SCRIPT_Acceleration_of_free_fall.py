import math
from manim import *


GRAVITY = 9.80665
# Русский шрифт
rus_text_template = TexTemplate()
rus_text_template.add_to_preamble(
    r"""
    \usepackage{polyglossia}
    \setmainlanguage{russian}
    \usepackage{fontspec}
    \setmainfont{Times New Roman}    
"""
)
rus_text_template.tex_compiler = "xelatex"
rus_text_template.output_format = ".xdv"
# Стандартный шрифт
standart_tex_template = TexTemplate()
standart_tex_template.tex_compiler = "xelatex"
standart_tex_template.output_format = ".xdv"


class TennisBall(VMobject):
    def __init__(
        self,
        radius: float = 1.0,
        fill_color: ParsableManimColor | None = None,
        stroke_width: float = 8.0,
        **kwargs
    ):
        super().__init__(**kwargs)

        # Создание мяча
        self.body = Circle(radius=radius, color=WHITE, stroke_width=stroke_width)

        if fill_color is not None:
            self.body.set_fill(fill_color, opacity=1)

        # Создание полос
        arc1 = Arc(
            radius=radius,
            angle=PI / 2,
            start_angle=PI / 4,
            stroke_color=WHITE,
            stroke_width=stroke_width / 2,
        ).flip(RIGHT)
        arc1.shift(arc1.radius * (1 - math.cos(arc1.angle / 2)) * DOWN)

        arc2 = Arc(
            radius=radius,
            angle=PI / 2,
            start_angle=PI / 4 + PI,
            stroke_color=WHITE,
            stroke_width=stroke_width / 2,
        ).flip(RIGHT)
        arc2.shift(arc2.radius * (1 - math.cos(arc2.angle / 2)) * UP)

        self.arcs = VGroup([arc1, arc2]).rotate(PI / 2)
        self.add(self.body, self.arcs)


class Greetings(Scene):
    """
    Класс отображения приветственного текста (тема и автор).
    """

    def construct(self):
        # Приветственный текст
        theme = Text(
            "Ускорение свободного падения",
            font_size=48,
        )

        author = Text(
            "Подготовил Емельяненко Владимир",
            font_size=28,
        )
        author.move_to(theme.get_bottom() + DOWN * 0.2)

        # Вывод
        text_out_group = VGroup(theme, author)
        out_lag_ratio = 1.5

        self.wait()
        self.play(AnimationGroup(Write(text_out_group), lag_ratio=out_lag_ratio))
        self.wait()
        self.play(AnimationGroup(Unwrite(text_out_group), lag_ratio=out_lag_ratio))
        self.wait()


class AccelerationOfFreeFall(Scene):
    def construct(self):
        def animate_free_fall(
            scene: Scene = self,
            falling_mobject: TennisBall = None,
            duration: float = 2.0,
            cam_zoom: float = 1.0,
            return_into_pos: Vector | None = None,
            parallel_anim_mobjects: VGroup | Mobject | None = None,
        ) -> None:
            # Отслеживающие/системные переменные
            time = ValueTracker()
            start_coords = falling_mobject.body.get_center()

            # Трасер
            trace = TracedPath(
                traced_point_func=falling_mobject.body.get_center,
                stroke_width=100 * cam_zoom,
                stroke_color=RED,
                stroke_opacity=[0.65, 0],
                dissipating_time=0.35,
            )
            trace.set_z_index(-1)
            scene.add(trace)

            # Обработчик падения
            falling_mobject.add_updater(
                update_function=lambda mob: mob.move_to(
                    start_coords
                    + DOWN * (time.get_value() ** 2) * GRAVITY * cam_zoom * 0.5
                )
            )

            # Парралельно обрабатываемые объекты
            if parallel_anim_mobjects is None:
                scene.play(
                    time.animate.set_value(duration),
                    rate_func=linear,
                    run_time=duration,
                )
            else:
                scene.play(
                    Create(parallel_anim_mobjects, lag_ratio=0),
                    time.animate.set_value(duration),
                    rate_func=linear,
                    run_time=duration,
                )
            # Падение

            scene.wait()
            # Удаление обработчика, трасера
            falling_mobject.clear_updaters()
            scene.remove(trace)
            # Возврат
            if return_into_pos is None:
                return_pos = start_coords
            else:
                return_pos = return_into_pos
            scene.play(falling_mobject.animate.move_to(return_pos), run_time=1.5)
            scene.wait()

        # Мяч
        tennis_ball = TennisBall(radius=0.45, fill_color=RED, stroke_width=6.0)

        self.wait()
        self.play(GrowFromCenter(tennis_ball), run_time=2)
        self.wait()
        self.play(tennis_ball.animate.shift(UP * 3))
        self.wait()

        # Свободное падение No. 1
        duration = 2
        animate_free_fall(
            falling_mobject=tennis_ball, duration=duration, return_into_pos=ORIGIN
        )

        # Свободное падение No. 2
        duration = 5
        # График скорости
        range_dist = ([0, duration, 0.6], [0, duration * GRAVITY, 6])
        length_dist = (config.frame_width / 2, config.frame_height - 2)
        speed_axes = Axes(
            x_range=range_dist[0],
            y_range=range_dist[1],
            x_length=length_dist[0],
            y_length=length_dist[1],
            axis_config={
                "include_numbers": True,
                "color": WHITE,
                "tip_width": 0.15,
                "tip_height": 0.15,
            },
        )
        labels = speed_axes.get_axis_labels(
            x_label=Text("Время, c").scale(0.5),
        )[0].shift(LEFT)
        y_label=VGroup(
                Text("Скорость, м/с", color=YELLOW).shift(UP * 0.45),
                Text("Расстояние, м", color=RED_B).shift(DOWN * 0.25),
            ).scale(0.4).move_to(speed_axes.axis_labels[1].get_center()).shift(UP * 0.15)

        speed_axes_help_grid = NumberPlane(
            x_range=range_dist[0],
            y_range=range_dist[1],
            x_length=length_dist[0],
            y_length=length_dist[1],
            background_line_style={
                "stroke_color": ORANGE,
                "stroke_width": 1,
                "stroke_opacity": 0.5,
            },
        )
        speed_graphic = VGroup(speed_axes, speed_axes_help_grid, labels, y_label)

        free_fall_speed_func_plot = speed_axes.plot(
            lambda time: time * GRAVITY, use_vectorized=True, color=YELLOW
        )
        free_fall_dist_func_plot = speed_axes.plot(
            lambda time: time**2 * GRAVITY * 0.5, use_vectorized=True, color=RED_B
        )
        func_plots = VGroup(free_fall_speed_func_plot, free_fall_dist_func_plot)

        VGroup(speed_graphic, func_plots).shift(RIGHT * 2.5)

        # Вывод
        # Сдвиг/маштабирование мяча
        self.play(tennis_ball.animate.shift(UP * 3 + LEFT * 5))
        self.play(tennis_ball.animate.scale(0.4))
        self.wait()
        # График скорости
        self.play(Create(speed_graphic, lag_ratio=0.5), run_time=4)
        self.wait()
        # Падение
        animate_free_fall(
            falling_mobject=tennis_ball,
            duration=duration,
            cam_zoom=0.4,
            parallel_anim_mobjects=func_plots,
        )
        # Очистка
        self.play(Uncreate(VGroup(*[func_plots, tennis_ball, speed_graphic]), lag_ration=0), run_time=4)
        self.wait()


class Equation(Scene):
    def construct(self):
        font_size = 80
        gravity_text = Tex(r"$g=9.8\frac{m}{s^2}$", font_size=font_size, tex_template = standart_tex_template)
        speed_text = Tex(r"$v=g*t$", font_size=font_size, tex_template = standart_tex_template)
        dist_text = Tex(r"$s=g*t^{2}*0.5$", font_size=font_size, tex_template=standart_tex_template)
        self.play(Write(gravity_text))
        self.wait()
        self.play(gravity_text.animate.shift(UP * 2), Write(speed_text))
        self.wait()
        self.play(Write(dist_text.shift(DOWN * 2)))
        self.wait()
        self.play(Unwrite(VGroup(gravity_text, speed_text, dist_text)))
        self.wait()


class NonGravity(Scene):
    def construct(self):
        # Земля
        planet = Circle(radius=config.frame_height / 2 - 2, color=GREEN, fill_color=GREEN, fill_opacity=0.25)
        self.play(Create(planet))
        self.wait()
        self.play(planet.animate.scale(10).shift(DOWN * (planet.radius * 10 + 3)))
        self.wait()
        # Мяч
        tennis_ball = TennisBall(radius=0.2, fill_color=RED, stroke_width=5).shift(UP * 2)
        self.play(Create(tennis_ball))
        self.wait()
