"""
MIT License

Copyright © 2025 VEFrenovator

Permission is hereby granted, free of charge, to any person obtaining a copy of this software
and associated documentation files (the "Software"), to deal in the Software without restriction,
including without limitation the rights to use, copy, modify, merge, publish, distribute,
sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or
substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING
BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

---

*Общее назначение*\n
`slides_animation` - главный модуль анимации. Сюда вносятся все авторские правки и нововведения.

---

*Описание (план) модуля (по классам)*:

- `{main}`: импорт библиотек, объявление TexTemplate для русского шрифта, объявление многоугольника
(галереи), а также треугольников триангуляции.\n
- `Greetings`: заставка (тема и автор).\n
- `TableOfContents`: план (содержание) выступления.\n
- `ProblemDescription`: описания теоремы, постановка проблемы.\n
- `Algorithm`: описание алгоритма решения Стива Фиска.\n
- `Triangulation`: описание алгоритма триангуляции методом отрезания ушей.\n
- `Tricoloring`: описание алгоритма жадной трираскраски.\n
- `Examples`: примеры работы алгоритма при решении реальных задач расстановки камер
видеонаблюдения.\n
- `Conclusion`: заключение, бегущая строка, содержащая код анимации.\n
- `ClosingRemarks`: заставка заключения (спасибо за внимание).\n
"""

# Импорт библиотек и модулей
import os
import json
from typing import List, Set
from manim import *
from manim_slides import Slide
from shapely.geometry import (
    Polygon as ShapelyPolygon,
    Point as ShapelyPoint,
)
import solution
from subtheme_handler import SubthemeHandler
from moving_camera_slide import MovingCameraSlide

# Установка background стиля
config.background_color = ManimColor([1/255, 1/255,30/255,0/255])

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
VMobject()
# Общая группа
comb_polygon = (
    VGroup(polygon, polygon_dots)
    .scale_to_fit_height(config.frame_height * 0.9)
    .move_to(ORIGIN)
)

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


class Greetings(Slide):  # pylint: disable=inherit-non-class
    """
    Класс отображения приветственного текста (тема и автор).
    """

    def construct(self):  # pylint: disable=missing-function-docstring
        self.wait()

        # Приветственный текст
        theme = Text(
            "Теорема о картинной галерее",
            font_size=48,
        )

        author = Text(
            "Подготовил Емельяненко Владимир",
            font_size=28,
        )
        author.next_to(author, DOWN, buff=MED_LARGE_BUFF)

        # Вывод
        text_out_group = VGroup(theme, author)
        out_lag_ratio = 0.35

        self.play(AnimationGroup(Write(text_out_group), lag_ratio=out_lag_ratio))

        self.wait()
        self.next_slide(loop=True)
        self.wait()

        self.play(
            Circumscribe(
                mobject=text_out_group,
                buff=MED_SMALL_BUFF,
            ),
            Wait(),
        )

        self.wait()
        self.next_slide()
        self.wait()

        self.play(AnimationGroup(Unwrite(text_out_group), lag_ratio=out_lag_ratio))


class TableOfContents(Slide):  # pylint: disable=inherit-non-class
    """
    Класс отображения содержания (плана работы).
    """

    def get_table_of_contents(
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
                    self.get_table_of_contents(
                        subthemes=subtheme[1],
                        depth=depth + 1,
                        prev_num_sys=f"{prev_num_sys}{i}.",
                    )
                )
        return plain_lines

    def construct(self):  # pylint: disable=missing-function-docstring
        self.next_slide()
        self.wait()

        title = Title("Содержание", tex_template=rus_tex_template)
        body = Paragraph(
            "\n".join(
                self.get_table_of_contents(global_subtheme_handler.subtheme_variants)
            )
        ).scale_to_fit_width(config.frame_width * 0.85)

        self.play((Succession(Write(title), Write(body))))

        self.wait()
        self.next_slide()
        self.wait()

        self.play(LaggedStart(Unwrite(body), Unwrite(title), lag_ratio=0.3))


class ProblemDescription(Slide):  # pylint: disable=inherit-non-class
    """
    Описание проблемы
    """

    def construct(self):  # pylint: disable=missing-function-docstring
        self.next_slide()
        self.wait()

        global polygon
        global polygon_dots
        global comb_polygon

        # ВЫВОД

        # Отрисовка многоугольника
        self.play(
            LaggedStart(
                Create(polygon_dots, rate_func=linear),
                Create(polygon, rate_func=linear),
                lag_ratio=0.1,
                run_time=3,
            )
        )

        # Отрисовка охранника
        guard = Dot([-0.5, 0, 0], 0.12, color=RED, z_index=1)

        self.wait()
        self.next_slide()
        self.wait()

        self.play(GrowFromCenter(guard))

        self.play(
            Flash(
                point=guard,
                line_length=0.5,
                flash_radius=guard.radius + 0.01,
                color=guard.get_color(),
            ),
            Wait(),
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

        self.wait()
        self.next_slide()
        self.wait()

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

        # Отрисовка поля зрения
        guard_view_coords = solution.calculate_visibility(polygon, guard)
        FOV_KWARGS = {  # pylint: disable=invalid-name
            "stroke_opacity": 0,
            "fill_color": GREEN,
            "fill_opacity": 1,
            "z_index": -1,
        }
        guard_view = Polygon(
            *[(x, y, 0) for x, y in guard_view_coords],
            **FOV_KWARGS,
        )

        self.wait()
        self.next_slide()
        self.wait()

        self.play(GrowFromPoint(guard_view, guard))

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

        self.wait()
        self.next_slide()
        self.wait()

        self.play(MoveAlongPath(guard, path, run_time=5, rate_func=smooth))
        guard_view.clear_updaters()

        # Мерцание вершин
        self.wait()
        self.next_slide()
        self.wait()

        for _ in range(2):
            self.play(
                AnimationGroup(
                    Indicate(polygon_dot, scale_factor=2, color=ORANGE, lag_ratio=0)
                    for polygon_dot in polygon_dots
                )
            )
            self.wait(0.25)

        # Перемещения охранника в угол
        guard_view.add_updater(updater_func)

        self.play(
            guard.animate.move_to(
                polygon_dots[-8].get_center() + np.array([0.01, 0.01, 0])
            )
        )
        guard_view.clear_updaters()

        # Создание новых охранников, которые полностью осматривают многоугольник
        # Удаление ненужного
        self.wait()
        self.next_slide()
        self.wait()

        self.play(
            AnimationGroup(
                FadeOut(guard_view.set_z_index(-1)),
                Uncreate(guard),
            )
        )
        self.remove(guard_view)


class Algorithm(Slide):  # pylint: disable=inherit-non-class
    """
    Показ работы алгоритма Стива Фиска
    """

    def construct(self):  # pylint: disable=missing-function-docstring
        self.next_slide()
        self.wait()

        global polygon
        global polygon_dots
        global comb_polygon

        # Добавление и сдвиг многоугольника
        self.add(comb_polygon)
        self.play(
            (
                comb_polygon.animate.scale_to_fit_width(
                    config.frame_width / 2 * 0.85
                ).move_to(RIGHT * config.frame_width / 4)
            ),
            lag_ratio=0,
        )
        polygon.set_z_index(1)
        polygon_dots.set_z_index(2)
        self.wait()

        # Разделение экрана
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

        # Создание нумерованного списка шагов
        steps_strs = [
            r"Триангулировать многоугольник\\(без добавления новых вершин).",
            r"Раскрасить вершины в три цвета\\так, чтобы каждый треугольник\\был окрашен всеми тремя цветами.",
            r"Теперь весь многоугольник\\просматривается всеми охранниками\\одной группы.",
            r"Цвет с меньшим количеством\\вершин образует множество максимум\\$\lfloor n/3 \rfloor$ вершин.",
        ]
        steps = VGroup()
        for i, line in enumerate(steps_strs):
            steps.add(
                Tex(
                    f"{str(i + 1)}. {line}",
                    tex_template=rus_tex_template,
                )
            )
            if len(steps) >= 2:
                steps[i].next_to(
                    steps[i - 1], DOWN, buff=DEFAULT_MOBJECT_TO_MOBJECT_BUFFER * 1.5
                )
        steps.move_to(ORIGIN).shift(LEFT * config.frame_width / 4).scale_to_fit_width(
            config.frame_width / 2 * 0.9
        )

        # Шаг 1. Триангуляция
        self.wait()
        self.next_slide()
        self.wait()

        triangles.move_to(polygon).scale_to_fit_width(polygon.width)
        self.play(
            Write(steps[0], run_time=2), Create(triangles, lag_ratio=0.2, run_time=4)
        )

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

        self.wait()
        self.next_slide()
        self.wait()

        self.play(
            LaggedStart(
                *animations,
                run_time=3,
            ),
            Write(steps[1]),
        )

        self.wait()
        self.next_slide()
        self.wait()

        indications = []
        for dot in polygon_dots:
            indications.append(
                Indicate(
                    dot,
                    2.5,
                    dot.get_color(),
                    rate_func=there_and_back_with_pause,
                    run_time=3,
                )
            )
        self.play(AnimationGroup(*indications))

        # Шаг 3. Отображение того, что вся галерея просматривается наблюдателями оной группы
        self.wait()
        self.next_slide()
        self.wait()

        self.play(Write(steps[2]), run_time=2)
        self.play(triangles.animate.set_fill(PURE_BLUE, 0.75), run_time=2)
        self.play(triangles.animate.set_fill(PURE_GREEN, 0.75), run_time=2)
        self.play(triangles.animate.set_fill(PURE_RED, 0.75), run_time=2)
        self.play(triangles.animate.set_fill(None, 0), run_time=2)

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

        self.wait()
        self.next_slide()
        self.wait()

        self.play(
            Write(steps[3]), Transform(color_poly_groups, color_poly_arranged_groups)
        )

        # Удаление
        deletions: List[Animation] = []
        for mobj in self.mobjects:
            if isinstance(mobj, SVGMobject) or isinstance(mobj, Paragraph):
                deletions.append(Unwrite(mobj))
            elif isinstance(mobj, VMobject):
                deletions.append(Uncreate(mobj))
            else:
                deletions.append(FadeOut(mobj))

        self.wait()
        self.next_slide()
        self.wait()

        self.play(AnimationGroup(*deletions))

        # Восстановление исходных точек многоугольника
        polygon = (
            Polygon(*polygon_dots_positions_list, color=WHITE, z_index=1)
            .scale_to_fit_height(config.frame_height * 0.9)
            .move_to(ORIGIN)
        )
        polygon_dots = VGroup(z_index=2)
        for coords in polygon.get_vertices():
            polygon_dots.add(Dot(coords, color=WHITE))


class Triangulation(Slide):  # pylint: disable=inherit-non-class
    """
    Подробное описание метода отрезания ушей.
    """

    def construct(self):  # pylint: disable=missing-function-docstring
        def degenerate_triangle(triangle: Polygon, is_ear: bool) -> None:
            """
            Функция анимационно удаляет треугольник (`triangle`), в случае, если это ухо
            (`is_ear==True`), оставляет его "фантом" (полупрозрачную копию).
            """
            if is_ear:
                self.play(triangle.animate.set_fill(GREEN), run_time=0.5)
                fantom = (
                    triangle.copy()
                    .set_stroke(BLUE_C, DEFAULT_STROKE_WIDTH / 2, 0.7)
                    .set_fill(opacity=0)
                    .set_z_index(-2)
                )
                self.add(fantom)
                fantoms.add(fantom)
            else:
                self.play(triangle.animate.set_fill(RED), run_time=0.5)
            self.play(triangle.animate.set_fill(opacity=0), run_time=0.5)
            self.play(Uncreate(triangle), run_time=1)

        self.next_slide()
        self.wait()

        global polygon
        global polygon_dots
        global comb_polygon

        # Определение
        ear_defenition = Tex(
            r"Вершна $v_i$ простого многоугольника $P$ называется \underline{\textbf{ухом}}, если диагональ $v_{i-1}v_{i+1}$ полностью лежит внутри $P$ и внутри треугольника $v_{i-1}v_{i}v_{i+1}$ не лежит других вершин $P$",
            tex_template=rus_tex_template,
        ).scale_to_fit_width(config.frame_width * 0.85)

        self.play(Write(ear_defenition))

        self.wait()
        self.next_slide(loop=True)
        self.wait()

        self.play(Circumscribe(ear_defenition, buff=MED_SMALL_BUFF))

        self.next_slide()
        self.wait()

        self.play(Unwrite(ear_defenition))
        self.wait()

        # Добавление блок-схемы
        block_diagram = (
            ImageMobject(r"Visual_charts\Triangulation\tiangulation_block_diagram.png")
            .scale_to_fit_height(config.frame_height - SMALL_BUFF * 4)
            .shift(UP * 2)
        )

        self.next_slide()
        self.play(
            AnimationGroup(FadeIn(block_diagram), block_diagram.animate.shift(DOWN * 2))
        )
        self.wait()

        # Добавление псевдокода
        pseudocode = (
            Code(
                r"Visual_charts\Triangulation\triangulation_pseudocode.py",
                formatter_style="dracula",
                language="python",
                background="window",
            )
            .next_to(config.right_side, RIGHT)
            .scale_to_fit_width(config.frame_width / 5 * 4 * 0.95)
        )
        self.add(pseudocode)

        self.next_slide()
        self.play(
            AnimationGroup(
                block_diagram.animate.scale(0.75 * 0.95).next_to(
                    config.left_side, RIGHT, buff=SMALL_BUFF
                ),
                pseudocode.animate.next_to(config.right_side, LEFT, buff=SMALL_BUFF),
            )
        )
        self.wait()

        # Отчистка экрана
        self.next_slide()
        self.play(
            AnimationGroup(
                block_diagram.animate.next_to(config.left_side, LEFT).scale(0.8),
                pseudocode.animate.next_to(config.right_side, RIGHT).scale(0.8),
            )
        )
        self.remove(block_diagram, pseudocode)

        # Добавление многоугольника
        self.next_slide()
        self.wait()

        self.play(
            LaggedStart(
                Create(polygon_dots, rate_func=linear),
                Create(polygon, rate_func=linear),
                run_time=3,
                lag_ratio=0.1,
            )
        )

        # Создание shapely-многоугольника
        shapely_polygon = ShapelyPolygon(polygon.get_vertices())

        # Добавление треугольников
        self.next_slide()
        self.wait()

        i = 0
        fantoms = (
            VGroup()
        )  # Группа треугольников, создаваемых в процессе анимации. Подробнее
        # см. функцию degenerate_triangle

        while len(polygon_dots) > 3:
            i %= len(polygon_dots)

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
            self.play(
                AnimationGroup(
                    polygon_dots[i].animate.set_color(PURPLE_E),
                    Indicate(polygon_dots[i], color=PURPLE_E),
                ),
                run_time=0.5,
            )

            # Вывод manim треугольника
            self.play(
                Succession(
                    Create(manim_triangle),
                    manim_triangle.animate.set_fill(ORANGE, 1),
                ),
                run_time=1,
            )

            # Проверка 1. Возможное ухо внутри многоугольника?
            is_ear = shapely_polygon.covers(shapely_triangle)

            # -> Если да, закрашиваем цветом, ближе к жёлтому, запускаем проверку 2
            if is_ear:
                self.play(manim_triangle.animate.set_fill(YELLOW), run_time=0.5)

                # Проверка 2. Внутри возможного уха лежит(-ат) точки многоугольника?
                has_vert_inside = False
                for vert in polygon_dots[i + 2 :] + polygon_dots[: i - 1]:
                    vert.set_color(ORANGE).scale(2)
                    # Если точка внутри, останавливаем цикл и выходим
                    if shapely_triangle.covers(ShapelyPoint(vert.get_center()[:2])):
                        has_vert_inside = True
                        break
                    # Если не внутри, идём дальше
                    else:
                        self.wait(0.1)
                        vert.set_color(WHITE).scale(0.5)

                # Если была точка внутри, удаляем треугольник и идём дальше
                if has_vert_inside:
                    vert.set_color(RED)
                    self.wait(0.5)
                    vert.set_color(WHITE).scale(0.5)
                    degenerate_triangle(manim_triangle, is_ear=False)
                    i += 1
                    continue

                # Удаляем ухо (именно как ухо. Т.е. закрашиваем предварительно зеленым)
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
                    LaggedStart(
                        Transform(polygon, new_polygon),
                        Uncreate(lines_to_cut, lag_ratio=0),
                        ShrinkToCenter(polygon_dots[i]),
                        lag_ratio=0.5,
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
            self.play(polygon_dots.animate.set_color(WHITE), run_time=0.4)

        # Итог: на экране только фантомы и треугольник-полигон (белый)
        # Делаем полигон фантомом
        self.next_slide()
        self.wait()
        self.next_slide()  # Двойной next_slide, чтобы сделать паузу
        self.play(
            AnimationGroup(
                ShrinkToCenter(polygon_dots[0]),
                ShrinkToCenter(polygon_dots[1]),
                ShrinkToCenter(polygon_dots[2]),
                polygon.animate.set_stroke(BLUE_C, DEFAULT_STROKE_WIDTH / 2, 0.7),
            )
        )
        fantoms.add(polygon)

        # Отчистка экрана
        self.next_slide()
        self.play(LaggedStart(*[Uncreate(fantom) for fantom in fantoms]))


class Tricoloring(Slide):  # pylint: disable=inherit-non-class
    """
    Подробное описание метода трираскраски полигона.
    """

    def construct(self):  # pylint: disable=missing-function-docstring
        # Блок схема
        block_diagram = (
            ImageMobject(r"Visual_charts\Tricoloring\tricoloring_block_diagram.png")
            .scale_to_fit_height(config.frame_height * 0.95)
            .shift(UP * 2)
        )

        self.next_slide()
        self.wait()
        self.play(
            AnimationGroup(
                FadeIn(block_diagram), block_diagram.animate.shift(DOWN * 2)
            ),
        )
        self.wait()
        self.next_slide()

        # Псевдокод
        pseudocode = (
            Code(
                r"Visual_charts\Tricoloring\tricoloring_pseudocode.py",
                formatter_style="dracula",
                language="python",
                background="window",
            )
            .next_to(config.right_side, RIGHT)
            .scale_to_fit_height((config.frame_height - SMALL_BUFF * 4) * 0.85)
        )
        self.add(pseudocode)

        self.wait()
        self.play(
            AnimationGroup(
                block_diagram.animate.next_to(config.left_side, RIGHT, buff=SMALL_BUFF),
                pseudocode.animate.next_to(config.right_side, LEFT, buff=SMALL_BUFF),
            )
        )
        self.wait()
        self.next_slide()
        self.wait()
        self.play(
            AnimationGroup(
                block_diagram.animate.next_to(config.left_side, LEFT).scale(0.8),
                pseudocode.animate.next_to(config.right_side, RIGHT).scale(0.8),
            )
        )
        self.remove(block_diagram, pseudocode)
        self.next_slide()

        # Отрисовка многоугольника И диагоналей триангуляции
        self.wait()
        self.play(
            LaggedStart(
                Create(polygon_dots.set_z_index(2), rate_func=linear),
                Create(
                    polygon.set_z_index(1).set_stroke(
                        width=DEFAULT_STROKE_WIDTH / 2, opacity=0.5
                    ),
                    rate_func=linear,
                ),
                LaggedStart(
                    [Create(triangle.set_z_index(0)) for triangle in triangles[::-1]]
                ),
                run_time=3,
                lag_ratio=0.1,
            )
        )
        self.next_slide()

        # Нативный показ работы работы алгоритма трираскраски
        def get_color_of_group(group: Set) -> ManimColor:
            """
            Функция, возвращающая `ManimColor` в соответствии с
            именем переменной группы (`group`)
            """
            if group is color_a:
                return PURE_RED
            if group is color_b:
                return PURE_GREEN
            if group is color_c:
                return PURE_BLUE

        color_a, color_b, color_c = set(), set(), set()
        color_a.add(triangles_ids[0][0])
        color_b.add(triangles_ids[0][1])
        color_c.add(triangles_ids[0][2])

        self.wait()
        self.play(
            Succession(
                triangles[0]
                .animate.set_color(YELLOW)
                .set_stroke(width=DEFAULT_STROKE_WIDTH * 1.5),
                polygon_dots[triangles_ids[0][0]].animate.set_color(PURE_RED),
                polygon_dots[triangles_ids[0][1]].animate.set_color(PURE_GREEN),
                polygon_dots[triangles_ids[0][2]].animate.set_color(PURE_BLUE),
                run_time=1,
            )
        )
        self.play(
            triangles[0]
            .animate.set_color(GRAY)
            .set_stroke(width=DEFAULT_STROKE_WIDTH * 0.5),
            run_time=1 / 4,
        )
        self.wait()
        self.next_slide()

        while len(color_a) + len(color_b) + len(color_c) < len(
            polygon_dots_positions_list
        ):
            for triangle_id, triangle in zip(triangles_ids, triangles):
                non_colored = solution.third_non_colored(
                    triangle_id, [color_a, color_b, color_c]
                )

                if non_colored is not None:
                    index, group = non_colored
                    group.add(index)

                    self.play(
                        Succession(
                            triangle.animate.set_color(YELLOW).set_stroke(
                                width=DEFAULT_STROKE_WIDTH * 1.5
                            ),
                            polygon_dots[index].animate.set_color(
                                get_color_of_group(group)
                            ),
                            run_time=1,
                        )
                    )
                    self.play(
                        triangle.animate.set_color(GRAY).set_stroke(
                            width=DEFAULT_STROKE_WIDTH * 0.5
                        ),
                        run_time=1 / 4,
                    )
        self.wait()
        self.next_slide()
        self.wait()
        self.next_slide()

        # Отчистка экрана
        self.play(
            LaggedStart(
                Uncreate(polygon_dots, rate_func=linear),
                Uncreate(polygon, rate_func=linear),
                LaggedStart(
                    [Uncreate(triangle.set_z_index(0)) for triangle in triangles]
                ),
                run_time=3,
                lag_ratio=0.1,
            )
        )
        self.wait()


class Examples(MovingCameraSlide):  # pylint: disable=inherit-non-class
    def construct(self):  # pylint: disable=missing-function-docstring
        # Слайд-шоу для перспектив
        perspectives = Group()

        for path in os.listdir("Visual_charts/Examples/Perspectives"):
            perspective = ImageMobject(
                f"Visual_charts/Examples/Perspectives/{path}"
            ).scale_to_fit_width(config.frame_width - SMALL_BUFF * 2)
            perspectives.add(perspective)

        perspectives.arrange(buff=SMALL_BUFF * 2)
        perspectives.next_to(config.right_side, RIGHT, buff=SMALL_BUFF)
        self.add(perspectives)

        for _ in range(len(perspectives)):
            self.play(perspectives.animate.shift(LEFT * config.frame_width))
            self.wait(3)
        self.next_slide()

        # Слайд-шоу для планировок
        # Показ цветной планировки
        plan = (
            ImageMobject(r"Visual_charts\Examples\Plans\Plan.png")
            .scale_to_fit_width(config.frame_width - SMALL_BUFF * 2)
            .next_to(config.right_side, RIGHT, buff=SMALL_BUFF)
        )
        self.add(plan)

        self.play(
            AnimationGroup(
                perspectives.animate.shift(LEFT * config.frame_width),
                plan.animate.move_to(ORIGIN),
            )
        )
        self.wait()
        self.remove(perspectives)
        self.next_slide()

        # Смена на контрастную
        plan_contrasted = (
            ImageMobject(r"Visual_charts\Examples\Plans\Plan_contrasted.png")
            .scale_to_fit_width(config.frame_width - SMALL_BUFF * 2)
            .next_to(config.top, UP, buff=SMALL_BUFF)
        )
        self.add(plan_contrasted)

        self.play(
            AnimationGroup(
                plan.animate.shift(DOWN * config.frame_height),
                plan_contrasted.animate.shift(DOWN * config.frame_height),
            )
        )
        self.wait()
        self.remove(plan)
        self.next_slide()

        # Смена на контрастную без обозначений
        plan_contrasted_nonotations = (
            ImageMobject(r"Visual_charts\Examples\Plans\Plan_contrasted_nonotations.png")
            .scale_to_fit_width(config.frame_width - SMALL_BUFF * 2)
            .next_to(config.bottom, DOWN, buff=SMALL_BUFF)
        )
        self.add(plan_contrasted_nonotations)

        self.play(
            AnimationGroup(
                plan_contrasted.animate.shift(UP * config.frame_height),
                plan_contrasted_nonotations.animate.shift(UP * config.frame_height),
            )
        )
        self.wait()
        self.remove(plan_contrasted)
        self.next_slide()

        # Исчезновение контрастной планировки без обозначений и появление триангулированной
        triangulated_plan = (
            ImageMobject(r"Visual_charts\Examples\Plans\Plan_triangulated.png")
            .scale_to_fit_width(config.frame_width - SMALL_BUFF * 2)
            .move_to(ORIGIN)
        )
        self.add(triangulated_plan)
        self.play(
            plan_contrasted_nonotations.animate.set_opacity(0),
        )
        self.wait()
        self.remove(plan_contrasted_nonotations)
        self.next_slide()

        # Анимация движения камеры
        self.camera.frame.save_state()
        point_1 = triangulated_plan.get_bottom() + UP * 0.5
        point_2 = triangulated_plan.get_top() + DOWN * 0.5

        self.play(
            self.camera.frame.animate.move_to(point_1).set_width(
                triangulated_plan.width * 0.5
            ),
        )
        self.play(
            self.camera.frame.animate.move_to(point_2).set_width(
                triangulated_plan.width * 0.5
            ),
            run_time=8,
            rate_func=double_smooth,
        )
        self.play(Restore(self.camera.frame))

        self.wait()
        self.next_slide()

        # Удаление триангулированной планировки
        self.play(
            triangulated_plan.animate.set_opacity(0),
        )
        self.remove(triangulated_plan)
        self.wait()
