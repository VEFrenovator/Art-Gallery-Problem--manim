"""
manim: Основная анимационная библиотека.
    Примечание. Не обращай внимания на Wildcard предупреждение.
    Если написать import manim, то это не будет соответсвовать документации
    manim;
shapely: Продвинутая геометрии библиотека. Использую для нахождения пересечений.
"""

from typing import List
from manim import *
from shapely.geometry import (
    Polygon as ShapelyPolygon,
    Point as ShapelyPoint,
)
import solution
from subtheme_handler import SubthemeHandler


# Глобальный экземпляр SubthemeHandler
global_subtheme_handler = SubthemeHandler()


# Русский шрифт
rus_tex_template = TexTemplate(
    tex_compiler="xelatex",
    output_format=".xdv",
    preamble=r"""\usepackage{polyglossia}
\setmainlanguage{russian}
\usepackage{fontspec}
\defaultfontfeatures{Numbers = Lining}
\setmainfont{Times New Roman}[Numbers = Lining]""",
)

# Координаты многоугольника
polygon_dots_positions_list = [
    [-2.36667, -0.31515],
    [-2.31818, 0.8303],
    [-1.19091, 0.8303],
    [-2.18485, 1.60606],
    [0.09394, 1.55152],
    [0.5, 0.94545],
    [-0.0697, 0.46061],
    [2.05152, 0.44242],
    [2.19697, -2.33939],
    [-0.19697, -2.35152],
    [-0.11818, 0.09091],
    [-0.71818, 0.60606],
    [-0.70606, -0.58182],
    [-1.31818, -0.5697],
    [-1.3303, -1.0303],
    [-0.40909, -0.70909],
    [-1.25758, -2.15152],
    [-1.7, -2.15152],
    [-1.69394, -1.00606],
    [-4.16061, -0.98788],
    [-4.12424, 0.27273],
    [-3.22727, 0.53939],
    [-3.20303, 0.92121],
    [-4.11212, 1.42424],
    [-4.10606, 2.21212],
    [-2.63939, 2.19394],
    [-2.7, -0.29697],
]

# Точки на вершинах многоугольника
polygon_dots = VGroup()
for coords in polygon_dots_positions_list:
    coords.append(0)
    polygon_dots.add(Dot(coords, color=WHITE))

# Многоугольник
polygon = Polygon(*polygon_dots_positions_list, color=WHITE)

# Общая группа
comb_polygon = VGroup(polygon, polygon_dots)

# Треугольники триангуляции
triangles_ids = solution.triangulate(polygon)
triangles = VGroup()

for triangle_id in triangles_ids:
    dot1_i, dot2_i, dot3_i = triangle_id
    triangle_coords = [
        polygon_dots[dot1_i].get_center(),
        polygon_dots[dot2_i].get_center(),
        polygon_dots[dot3_i].get_center(),
    ]
    triangles.add(
        Polygon(
            *triangle_coords,
            color=GRAY,
            stroke_width=DEFAULT_STROKE_WIDTH * 0.5,
            joint_type=LineJointType.BEVEL,
        )
    )


class Greetings(Scene):
    """
    Класс отображения приветственного текста (тема и автор).
    """

    def construct(self):
        # Приветственный текст
        theme = Text(
            "Теорема о картинной галерее",
            font_size=48,
        )

        author = Text(
            "",
            font_size=28,
        )
        author.next_to(author, DOWN, buff=MED_LARGE_BUFF)

        # Вывод
        text_out_group = VGroup(theme, author)
        out_lag_ratio = 0.35

        self.wait()
        self.play(AnimationGroup(Write(text_out_group), lag_ratio=out_lag_ratio))
        self.play(
            Circumscribe(
                mobject=text_out_group,
                run_time=2,
                buff=MED_SMALL_BUFF,
            )
        )
        self.wait()
        self.play(AnimationGroup(Unwrite(text_out_group), lag_ratio=out_lag_ratio))
        self.wait()


class TableOfContents(Scene):
    """
    Класс отображения содержания (плана работы).
    """

    def _unpack(
        self, subthemes: List, depth: int = 0, prev_num_sys: str = ""
    ) -> List[str]:
        """
        Функция распаковывает подтемы (`subthemes`) в массив строк, организую это в
        многоуровневый список. Функция делает это рекурсивно, поэтому при вызове рекурсивно
        (из функции) требуется дополнительно передать:
        - `depth` - уровень в многоуровневом списке (чем больше, тем глубже).
        - `prev_num_sys` - нумерация предыдущего уровня.
        """
        plain_lines = []
        for i, subtheme in enumerate(subthemes, start=1):
            plain_lines.append(
                ("\t" * depth) + prev_num_sys + str(i) + ". " + subtheme[0]
            )
            if len(subtheme[1]) != 0:
                plain_lines.extend(
                    self._unpack(
                        subthemes=subtheme[1],
                        depth=depth + 1,
                        prev_num_sys=f"{prev_num_sys}{i}.",
                    )
                )
        return plain_lines

    def construct(self):
        title = Title("Содержание", tex_template=rus_tex_template)
        body = Paragraph(
            "\n".join(self._unpack(global_subtheme_handler.subtheme_variants))
        ).scale_to_fit_width(config.frame_width * 0.85)
        self.wait()
        self.play((Succession(Write(title), Write(body))))
        self.wait()
        self.play(LaggedStart(Unwrite(body), Unwrite(title), lag_ratio=0.3))
        self.wait()


class ProblemDescription(Scene):
    """
    Описание проблемы
    """

    def construct(self):
        global polygon
        global polygon_dots
        global comb_polygon

        # ВЫВОД
        self.wait()

        # Отрисовка многоугольника
        self.play(
            LaggedStart(
                Create(polygon_dots, rate_func=linear),
                Create(polygon, rate_func=linear),
                lag_ratio=0.1,
                run_time=3,
            )
        )
        self.wait()

        # Отрисовка охранника
        guard = Dot([-0.5, 0, 0], 0.12, color=RED, z_index=1)
        self.play(GrowFromCenter(guard))
        self.wait()
        self.play(
            Flash(
                point=guard,
                line_length=0.5,
                flash_radius=guard.radius + 0.01,
                color=guard.get_color(),
            )
        )

        # Показ того, что он смотрит на 360
        line_of_sight = Line(
            start=guard.get_center(),
            end=guard.get_center() + UP,
            stroke_color=WHITE,
            stroke_opacity=0,
        )
        line_of_sight_trace = TracedPath(
            line_of_sight.get_center,
            stroke_color=line_of_sight.get_stroke_color(),
            stroke_width=line_of_sight.get_length() * 50,
            stroke_opacity=1,
            dissipating_time=0.25,
        )

        self.play(
            Succession(
                Create(line_of_sight),
                Add(line_of_sight_trace),
                Rotate(
                    line_of_sight,
                    angle=360 * DEGREES * 2,
                    about_point=line_of_sight.get_start(),
                    run_time=3,
                ),
                Wait(line_of_sight_trace.dissipating_time),
            )
        )
        self.remove(line_of_sight, line_of_sight_trace)
        self.wait()

        # Отрисовка поля зрения
        guard_view_coords = solution.calculate_visibility(polygon, guard)
        FOV_KWARGS = {
            "stroke_opacity": 0,
            "fill_color": GREEN,
            "fill_opacity": 1,
            "z_index": -1,
        }
        guard_view = Polygon(
            *[(x, y, 0) for x, y in guard_view_coords],
            **FOV_KWARGS,
        )
        self.play(GrowFromPoint(guard_view, guard))
        self.wait()

        # Движение охранника
        updater_func = lambda mobj: mobj.set_points_as_corners(
            [(x, y, 0) for x, y in solution.calculate_visibility(polygon, guard)]
        )
        guard_view.add_updater(updater_func)
        path = VMobject(fill_opacity=0).set_points_smoothly(
            [
                guard.get_center(),
                polygon_dots[0].get_center() + DOWN * 0.5,
                polygon_dots[-8].get_center() + RIGHT * 0.5 + UP,
            ]
        )
        self.play(MoveAlongPath(guard, path, run_time=5, rate_func=smooth))
        guard_view.clear_updaters()
        self.wait()

        # Мерцание вершин
        for _ in range(2):
            self.play(
                AnimationGroup(
                    Indicate(polygon_dot, scale_factor=2, color=ORANGE, lag_ratio=0)
                    for polygon_dot in polygon_dots
                )
            )
            self.wait(0.25)
        self.wait()

        # Перемещения охранника в угол
        guard_view.add_updater(updater_func)
        self.play(
            guard.animate.move_to(
                polygon_dots[-8].get_center() + np.array([0.01, 0.01, 0])
            )
        )
        guard_view.clear_updaters()
        self.wait()

        # Создание новых охранников, которые полностью осматривают многоугольник
        # Удаление ненужного
        self.play(
            AnimationGroup(
                Uncreate(guard_view),
                Uncreate(guard),
            )
        )
        self.wait()


class Algorithm(Scene):
    """
    Показ работы алгоритма Стива Фиска
    """

    def construct(self):
        global polygon
        global polygon_dots
        global comb_polygon

        # Добавление и сдвиг многоугольника

        self.add(comb_polygon)
        self.play(
            comb_polygon.animate.scale_to_fit_width(config.frame_width / 2 * 0.85)
        )
        self.play(comb_polygon.animate.move_to(RIGHT * config.frame_width / 4))
        polygon.set_z_index(1)
        polygon_dots.set_z_index(2)
        self.wait()

        # Разделение экрана
        self.wait()
        divided_line1 = Line(ORIGIN, DOWN * config.frame_height / 2 * 0.85, color=WHITE)
        divided_line2 = divided_line1.copy().rotate(180 * DEGREES, about_point=ORIGIN)
        divided_lines = VGroup(divided_line1, divided_line2)
        titles = VGroup(
            MarkupText("<u>Шаги</u>", font_size=36)
            .to_edge(UP)
            .shift(LEFT * config.frame_width / 4),
            MarkupText("<u>Многоугольник</u>", font_size=36)
            .to_edge(UP)
            .shift(RIGHT * config.frame_width / 4),
        )
        self.play(
            AnimationGroup(
                Create(divided_lines, lag_ratio=0), Write(titles, lag_ratio=0)
            )
        )
        self.wait()

        # Создание нумерованного списка шагов
        steps_strs = [
            "Триангулировать многоугольник (без добавления новых вершин).",
            "Раскрасить вершины в три цвета так, чтобы каждый треугольник был окрашен всеми тремя цветами.",
            "Теперь весь многоугольник просматривается всеми охранниками одной группы.",
            r"Цвет с меньшим количеством вершин образует множество максимум $\lfloor n/3 \rfloor$ вершин.",
        ]
        steps = VGroup()
        for i, line in enumerate(steps_strs):
            steps.add(
                Tex(
                    f"{str(i + 1)}. {line}",
                    tex_template=rus_tex_template,
                    should_center=False,
                    width=config.frame_width / 2 * 0.9,
                    height=config.frame_height / 4 * 0.7,
                )
            )
            if len(steps) >= 2:
                steps[i].next_to(steps[i - 1], DOWN)
        steps.move_to(LEFT * config.frame_width / 4)

        # Шаг 1. Триангуляция
        self.play(
            Write(steps[0], run_time=2), Create(triangles, lag_ratio=0.2, run_time=4)
        )
        self.wait()

        # Шаг 2. Раскраска
        color_groups = solution.tricolor(
            triangles=triangles_ids,
            polygon_verts_count=len(polygon_dots_positions_list),
        )
        color_variants = (PURE_BLUE, PURE_GREEN, PURE_RED)
        animations: List[Animation] = []

        for i in range(3):
            for vert_id in color_groups[i]:
                vert = polygon_dots[vert_id]
                animations.append(vert.animate.set_color(color_variants[i]))

        polygon_dots.set_z_index(polygon.z_index + 1)
        self.play(
            LaggedStart(
                *animations,
                run_time=3,
            ),
            Write(steps[1]),
        )

        indications = []
        for dot in polygon_dots:
            indications.append(
                Indicate(
                    dot,
                    2.5,
                    dot.get_color(),
                    rate_func=there_and_back_with_pause,
                    run_time=5,
                )
            )
        self.play(AnimationGroup(*indications))
        self.wait()

        # Шаг 3. Отображение того, что вся галерея просматривается наблюдателями оной группы
        self.play(Write(steps[2]), run_time=2)
        self.play(triangles.animate.set_fill(PURE_BLUE, 0.75), run_time=2)
        self.play(triangles.animate.set_fill(PURE_GREEN, 0.75), run_time=2)
        self.play(triangles.animate.set_fill(PURE_RED, 0.75), run_time=2)
        self.play(triangles.animate.set_fill(None, 0), run_time=2)
        self.wait()

        # Шаг 4. Группировка наблюдателей в группы по цветам и показ того, что n/3 с нижним
        # округлением достаточно
        color_poly_groups = VGroup(z_index=0)  # type: VGroup[VGroup[Dot]]
        color_poly_arranged_groups = VGroup(z_index=0)  # type: VGroup[VGroup[Dot]]

        for color_group in color_groups:
            color_poly_group = VGroup()
            for vert_id in color_group:
                color_poly_group.add(polygon_dots[vert_id])
            color_poly_groups.add(color_poly_group)
            color_poly_arranged_groups.add(
                color_poly_groups[-1].copy().arrange_in_grid(rows=3)
            )

            if len(color_poly_arranged_groups) >= 2:
                color_poly_arranged_groups[-1].next_to(
                    color_poly_arranged_groups[-2], buff=MED_LARGE_BUFF
                )

        color_poly_arranged_groups.move_to(ORIGIN).to_edge(DOWN).shift(
            config.frame_width / 4 * RIGHT
        )

        self.play(
            Write(steps[3]), Transform(color_poly_groups, color_poly_arranged_groups)
        )
        self.wait()

        # Удаление
        deletions: List[Animation] = []
        for mobj in self.mobjects:
            if isinstance(mobj, SVGMobject) or isinstance(mobj, Paragraph):
                deletions.append(Unwrite(mobj))
            elif isinstance(mobj, VMobject):
                deletions.append(Uncreate(mobj))
            else:
                deletions.append(FadeOut(mobj))
        self.play(AnimationGroup(*deletions))
        self.wait()

        # Восстановление исходных точек многоугольника
        polygon = Polygon(
            *polygon_dots_positions_list, color=WHITE, z_index=1
        ).scale_to_fit_height(config.frame_height * 0.9)
        polygon_dots = VGroup(z_index=2)
        for coords in polygon.get_vertices():
            polygon_dots.add(Dot(coords, color=WHITE))


class Triangulation(Scene):
    """
    Подробное описание метода отрезания ушей.
    """

    def construct(self):
        def degenerate_triangle(triangle: Polygon, is_ear: bool) -> None:
            """
            Функция анимационно удаляет треугольник (`triangle`).
            """
            if is_ear:
                self.play(triangle.animate.set_fill(GREEN))
            else:
                self.play(triangle.animate.set_fill(RED))
            self.play(triangle.animate.set_fill(opacity=0))
            self.play(Uncreate(triangle))
            self.wait()

        global polygon
        global polygon_dots
        global comb_polygon

        # Вывод определения
        ear_defenition = Tex(
            r"Вершна $v_i$ простого многоугольника $P$ называется \underline{\textbf{ухом}}, если диагональ $v_{i-1}v_{i+1}$ полностью лежит внутри $P$ и внутри треугольника $v_{i-1}v_{i}v_{i+1}$ не лежит других вершин $P$",
            tex_template=rus_tex_template,
        ).scale_to_fit_width(config.frame_width * 0.85)

        self.wait()
        self.play(
            Succession(
                Write(ear_defenition), Circumscribe(ear_defenition, buff=MED_SMALL_BUFF)
            )
        )
        self.wait()
        self.play(Unwrite(ear_defenition))
        self.wait()

        # Добавление многоугольника
        comb_polygon.move_to(ORIGIN).scale_to_fit_height(config.frame_height * 0.9)
        self.play(
            LaggedStart(
                Create(polygon_dots, rate_func=linear),
                Create(polygon, rate_func=linear),
                run_time=3,
                lag_ratio=0.1,
            )
        )
        self.wait()

        # Создание shapely-многоугольника
        shapely_polygon = ShapelyPolygon(polygon.get_vertices())

        # Добавление треугольников
        i = 0
        for _ in range(5):

            # Shapely треугольник для геометрических вычислений
            shapely_triangle = ShapelyPolygon(
                [
                    polygon_dots[(i + bias) % len(polygon_dots)].get_center()[:2]
                    for bias in (-1, 0, 1)
                ]
            )

            # Manim треугольник для анимирования
            manim_triangle = Polygon(
                *[
                    polygon_dots[(i + bias) % len(polygon_dots)].get_center()
                    for bias in (-1, 0, 1)
                ],
                color=GRAY,
                joint_type=LineJointType.BEVEL,
                stroke_width=DEFAULT_STROKE_WIDTH * 0.5,
                z_index=-1,
            )

            # Закрашиваем вершину, которую сейчас проверяем
            polygon_dots[i].set_z_index(3)
            self.play(polygon_dots[i].animate.set_color(PURPLE_E))

            # Вывод manim треугольника
            self.play(
                Succession(
                    Create(manim_triangle),
                    manim_triangle.animate.set_fill(ORANGE, 1),
                ),
            )
            self.wait()

            # Проверка 1. Возможное ухо внутри многоугольника?
            is_ear = shapely_polygon.covers(shapely_triangle)

            # -> Если да, закрашиваем цветом, ближе к жёлтому, запускаем проверку 2
            if is_ear:
                self.play(manim_triangle.animate.set_fill(YELLOW))

                # Проверка 2. Внутри возможного уха лежит(-ат) точки многоугольника?
                has_vert_inside = False
                for vert in polygon_dots[i + 2 :] + polygon_dots[: i - 1]:
                    vert.set_color(ORANGE).scale(2)
                    # Если точка внутри, останавливаем цикл и выходим
                    if shapely_triangle.covers(ShapelyPoint(vert.get_center()[:2])):
                        self.wait()
                        has_vert_inside = True
                        break
                    # Если не внутри, идём дальше
                    else:
                        self.wait(0.15)
                        vert.set_color(WHITE).scale(0.5)

                # Если была точка внутри, удаляем треугольник и идём дальше
                if has_vert_inside:
                    vert.set_color(RED)
                    degenerate_triangle(manim_triangle, is_ear=False)
                    vert.set_color(WHITE).scale(0.5)
                    i += 1
                    continue

                # Удаляем ухо
                degenerate_triangle(manim_triangle, is_ear=True)

                # Создаюм список оставшихся точек (список вершин многоугольника
                # без уха) и новую VGroup без точки-уха
                new_coords: List[float, float, 0] = []
                new_dots = VGroup()
                for dot in polygon_dots:
                    if dot is not polygon_dots[i]:
                        new_dots.add(dot)
                        new_coords.append(dot.get_center())

                # Пересоздаём полигоны по новым точкам
                shapely_polygon = ShapelyPolygon(new_coords)  # Строгое пересоздание
                new_polygon = Polygon(*new_coords, color=WHITE)  # Пересоздадим позже

                # Удаляем линии уха, которые не являются диагональю, а также пересоздаём
                # многоугольник
                lines_to_cut = VGroup()
                for bias in (-1, 1):
                    lines_to_cut.add(
                        Line(
                            polygon_dots[i],
                            polygon_dots[(i + bias) % len(polygon_dots)],
                            color=WHITE,
                        )
                    )
                self.play(
                    Succession(
                        Transform(polygon, new_polygon),
                        Uncreate(lines_to_cut, lag_ratio=0),
                        Uncreate(polygon_dots[i]),
                    )
                )

                polygon.become(new_polygon)
                # После всех операций, присваиваем VGroup'е polygon_dots новое значение
                # без точки-уха
                polygon_dots = new_dots

            # -> Если нет, убираем треугольник и идём к следующему кандидату
            else:
                degenerate_triangle(manim_triangle, is_ear=False)
                i += 1

            # Удаляем раскраску у главной вершины
            self.play(polygon_dots.animate.set_color(WHITE))

        # Трюк: делаем плавное исчезновение, а потом результат триангуляции
        self.play(FadeOut(comb_polygon))

        # P.S. Но не забываем восстановить полигон и точки
        polygon = (
            Polygon(*polygon_dots_positions_list, color=WHITE, z_index=1)
            .move_to(ORIGIN)
            .scale_to_fit_height(config.frame_height * 0.9)
        )
        polygon_dots = VGroup(z_index=2)
        for coords in polygon.get_vertices():
            polygon_dots.add(Dot(coords, color=WHITE))
        comb_polygon = VGroup(polygon, polygon_dots)

        triangles.move_to(ORIGIN).scale_to_fit_height(polygon.height)
        self.wait()
        self.play(AnimationGroup(FadeIn(comb_polygon), FadeIn(triangles[:-1])))
        self.wait()


class Tricoloring(Scene):
    def construct(self):
        pass
