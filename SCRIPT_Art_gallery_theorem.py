"""
math: Базовая математическая библиотека;
manim: Основная анимационная библиотека.
    Примечание. Не обращай внимания на Wildcard предупреждение.
    Если написать import manim, то это не будет соответсвовать документации
    manim;
shapely: Продвинутая геометрии библиотека. Использую для нахождения пересечений.
"""

import math
from typing import Iterable, Tuple, List, Set, Optional
from manim import *
from shapely.geometry import (
    Polygon as ShapelyPolygon,
    Point as ShapelyPoint,
    LineString,
)
import mapbox_earcut as earcut


class Solution:
    """
    Решение поставленной задачи. Именно теоретическое решение, а не вывод анимации.

    Методы
    ------
    `calculate_visibility` - расчет поля зрения. \n
    `triangulate` - триангуляция. \n
    `tricolor` - раскраска в три цвета. \n
    """

    def calculate_visibility(
        self,
        polygon: Iterable[Iterable[float]] | Polygon | ShapelyPolygon,
        observer: Iterable[float] | Dot | ShapelyPoint,
    ) -> List[Tuple[float]]:
        """
        **ПРЕДУПРЕЖДЕНИЕ:** На момент 14.07.2025 не работает, если наблюдатель точно на границе. \n
        Расчитывает поле зрения наблюдателя (`observer`) в многоугольнике (`polygon`). \n
        Возвращает поле зрения в виде списка координат.

        Исключения
        ----------
        `ValueError`, если наблюдатель не в многоугольнике (учитывая границы).
        """

        # Convert input to Shapely objects
        if isinstance(polygon, Polygon):
            polygon = ShapelyPolygon(polygon.get_vertices())
        elif isinstance(polygon, Iterable):
            polygon = ShapelyPolygon(polygon)

        if isinstance(observer, Dot):
            observer = ShapelyPoint(observer.get_center())
        elif isinstance(observer, Iterable):
            observer = ShapelyPoint(observer)

        # Extract observer coordinates
        ox, oy = observer.coords[0][:2]

        # Check if observer is in the polygon (including boundary)
        if not polygon.covers(observer):
            raise ValueError("Observer is not in the polygon")

        # Get polygon vertices
        vertices = list(polygon.exterior.coords)

        # Check if observer is exactly at a vertex
        is_vertex = False
        for v in vertices:
            if math.isclose(ox, v[0], abs_tol=1e-8) and math.isclose(
                oy, v[1], abs_tol=1e-8
            ):
                is_vertex = True
                break

        # Create new polygon with observer as vertex if on edge
        new_vertices = []
        if not is_vertex and polygon.touches(observer):
            for i in range(len(vertices) - 1):
                p1, p2 = vertices[i], vertices[i + 1]
                edge = LineString([p1, p2])
                if edge.distance(observer) < 1e-8:
                    new_vertices.append(p1)
                    new_vertices.append((ox, oy))
                    is_vertex = True
                else:
                    new_vertices.append(p1)
            new_vertices.append(vertices[-1])
            vertices = new_vertices
            polygon = Polygon(vertices)

        # Create edges (excluding zero-length edges)
        edges = []
        for i in range(len(vertices) - 1):
            p1, p2 = vertices[i], vertices[i + 1]
            if math.isclose(p1[0], p2[0], abs_tol=1e-8) and math.isclose(
                p1[1], p2[1], abs_tol=1e-8
            ):
                continue
            edges.append(LineString([p1, p2]))

        # Get critical directions (vertices and edge-aligned directions)
        directions = set()
        epsilon = 1e-7  # Small angular offset

        for v in vertices:
            vx, vy = v[:2]
            if math.isclose(vx, ox, abs_tol=1e-8) and math.isclose(
                vy, oy, abs_tol=1e-8
            ):
                continue

            dx = vx - ox
            dy = vy - oy
            dist = math.hypot(dx, dy)
            directions.add((dx / dist, dy / dist))

            # Add edge-aligned directions for adjacent edges
            if is_vertex:
                # Find adjacent vertices
                prev_idx = (vertices.index(v) - 1) % (len(vertices)) - 1
                next_idx = (vertices.index(v) + 1) % (len(vertices)) - 1

                for adj in [vertices[prev_idx], vertices[next_idx]]:
                    if math.isclose(adj[0], ox, abs_tol=1e-8) and math.isclose(
                        adj[1], oy, abs_tol=1e-8
                    ):
                        # Direction along the edge
                        edge_dir_x = vx - ox
                        edge_dir_y = vy - oy
                        edge_dist = math.hypot(edge_dir_x, edge_dir_y)
                        if edge_dist > 1e-8:
                            directions.add(
                                (edge_dir_x / edge_dist, edge_dir_y / edge_dist)
                            )

        # Add epsilon-offset rays for all critical directions
        all_directions = []
        for dx, dy in directions:
            all_directions.append((dx, dy))

            # Add clockwise offset
            all_directions.append(
                (
                    dx * math.cos(epsilon) - dy * math.sin(epsilon),
                    dx * math.sin(epsilon) + dy * math.cos(epsilon),
                )
            )

            # Add counter-clockwise offset
            all_directions.append(
                (
                    dx * math.cos(epsilon) + dy * math.sin(epsilon),
                    -dx * math.sin(epsilon) + dy * math.cos(epsilon),
                )
            )

        # Calculate max ray distance
        max_dist = 2 * max(math.hypot(v[0] - ox, v[1] - oy) for v in vertices)

        # Find closest intersections
        visibility_points = []
        for dx, dy in all_directions:
            ray_end = (ox + dx * max_dist, oy + dy * max_dist)
            ray = LineString([(ox, oy), ray_end])

            closest_intersection = None
            min_dist_sq = float("inf")

            for edge in edges:
                # Skip edges containing observer
                if edge.distance(observer) < 1e-8:
                    continue

                # Handle potential floating-point issues
                try:
                    intersection = ray.intersection(edge)
                except:
                    continue

                if intersection.is_empty:
                    continue

                # Process different intersection types
                if intersection.geom_type == "Point":
                    points = [intersection]
                elif intersection.geom_type == "MultiPoint":
                    points = intersection.geoms
                elif intersection.geom_type == "LineString":
                    points = [Point(p) for p in intersection.coords]
                else:
                    continue

                for p in points:
                    px, py = p.x, p.y
                    if math.isclose(px, ox, abs_tol=1e-8) and math.isclose(
                        py, oy, abs_tol=1e-8
                    ):
                        continue

                    # Calculate squared distance
                    dist_sq = (px - ox) ** 2 + (py - oy) ** 2
                    if dist_sq < min_dist_sq:
                        min_dist_sq = dist_sq
                        closest_intersection = p

            if closest_intersection:
                visibility_points.append(
                    (closest_intersection.x, closest_intersection.y)
                )

        # Remove duplicates
        unique_points = []
        for p in visibility_points:
            if not any(
                math.isclose(p[0], up[0], abs_tol=1e-8)
                and math.isclose(p[1], up[1], abs_tol=1e-8)
                for up in unique_points
            ):
                unique_points.append(p)

        # Sort by angle
        def angle_from_observer(p):
            return math.atan2(p[1] - oy, p[0] - ox)

        unique_points.sort(key=angle_from_observer)

        return unique_points

    def triangulate(
        self, polygon: List[Tuple[float, float]] | Polygon | ShapelyPolygon
    ) -> List[Tuple[int, int, int]]:
        """
        Триангулирует многоугольник (`polygon`) с помощью метода отрезания ушей. \n
        Использует библиотеку `mapbox_earcut`. \n
        Возвращает треугольники триангуляции в виде списка ***индексов вершин треугольников**
        в списке изначальных вершин многоугольника*. Например, треугольник
        (0, 1, 2) означает, что вершины исходного многоугольника под индексами (0, 1, 2)
        образуют треугольник триангуляции.
        """
        if isinstance(polygon, Polygon):
            polygon = np.array(
                [coords[:2] for coords in polygon.get_vertices()]
            ).reshape(-1, 2)
        elif isinstance(polygon, ShapelyPolygon):
            polygon = np.array(
                [coords[:2] for coords in polygon.exterior.coords]
            ).reshape(-1, 2)

        rings_end_i = np.array([len(polygon)])

        result = earcut.triangulate_float32(polygon, rings_end_i).tolist()
        return [tuple(result[i : i + 3]) for i in range(0, len(result), 3)]

    def tricolor(
        self, triangles: List[Tuple[int, int, int]], polygon_verts_count: int
    ) -> Tuple[Set, Set, Set]:
        """
        Раскрашивает вершины треугольников (`triangles`) в три цвета так, чтобы
        в любом треугольнике было все три цвета. \n
        `polygon_verts_count` - количество вершин исходного многоугольника. Другими словами,
        длина списка `polygon_dots`. \n
        Возвращает кортеж из трёх множеств. Каждое множество отражает вершины
        треугольников, которые должны быть окрашены цветом этой группы.
        """

        def third_non_colored(triangle: Tuple) -> Optional[Tuple[int, Set]]:
            """
            Принимает один треугольник триангуляции (`triangle`) \n
            *Если две вершины этого треугольника уже окрашены*, возвращает
            вершину, которую нужно окрасить и множество, цветом которого
            эту вершину нужно окрасить. \n
            *Если в этом треугольнике окрашены 0, 1 или 3 вершины*, возвращает `None`.
            """
            indexes = list(triangle)
            groups = [group_a, group_b, group_c]

            i, j = 0, 0
            while i < len(indexes):
                while j < len(groups):
                    if indexes[i] in groups[j]:
                        del indexes[i]
                        del groups[j]
                        break
                    j += 1
                else:
                    i += 1
                j = 0

            if len(indexes) == 1:
                return indexes[0], groups[0]

        group_a, group_b, group_c = set(), set(), set()
        group_a.add(triangles[0][0])
        group_b.add(triangles[0][1])
        group_c.add(triangles[0][2])

        while len(group_a) + len(group_b) + len(group_c) < polygon_verts_count:
            for triangle in triangles:
                non_colored = third_non_colored(triangle)
                if non_colored is not None:
                    index, group = non_colored
                    group.add(index)
        return group_a, group_b, group_c


class SubthemeHandler:
    """
    Класс для анимационной смены подтем.
    Просьба запускать update_subtheme в соответствующем названию подтемы подклассе Scene.
    """

    def __init__(self):
        # Многомерный массив (дерево) вариантов подтем в формате ["название", [подтемы более
        # низкого уровня]].
        # Примечание: если подтем более низкого уровня нет, массив объявляется пустым.

        self.subtheme_variants = [
            ["Введение", []],
            ["Описание проблемы", []],
            ["Алгоритм Стива Фиска", []],
            [
                "Триангуляция многоугольника (без добавления новых вершин)",
                [
                    ["Некоторые определения", []],
                    ["Жадный алгоритм", []],
                    [
                        "Метод отрезания ушей",
                        [
                            ["Некоторые теоремы", []],
                            ["Алгоритм", []],
                        ],
                    ],
                ],
            ],
            ["Раскраска вершин", []],
            ["Остатки от деления", []],
            ["Заключение", []],
        ]

        # Дерево subtheme_variants, но развёрнутое в список путей (pre-order)
        self.flat_paths = []  # Список путей в кортежах (путь, название)
        self._unpack(self.subtheme_variants, [])
        self.sequence = -1  # Номер подтемы в flat_path

        self.current_out_texts: dict[int, Text] = {}  # {приоритет: текст}
        self.current_out_lines: dict[int, Line] = (
            {}
        )  # {приоритет: линия}. Примечание: линии
        # нет над 1-ым уровнем

    def _unpack(self, subtree: list, path) -> None:
        """
        Рекурсивный обход дерева для формирования списка путей.
        Каждый путь - это масив индексов до текущей подтемы в subtree. Например, чтобы дойти
        до подтемы "Жадный алгорим" нужно использовать путь [1, 0, 0].
        При этом на одной итерации мы зацикливаемся в самом себе.
        """
        for i, (name, children) in enumerate(subtree):
            new_path = path + [i]

            self.flat_paths.append((new_path, name))
            if children:
                self._unpack(children, new_path)

    def init_subtheme(self, scene: Scene) -> None:
        """
        Функция добавляет нужную подтему на экран мгновенно. Нужно запускать при инициализации
        класса чтобы подтема не пропадала при окончании предыдущего и не появлялась при
        включении нового.
        """
        if len(self.current_out_texts) == 0:
            self.update_subtheme(scene)

        scene.add(*[*self.current_out_texts.values(), *self.current_out_lines.values()])

    def update_subtheme(self, scene: Scene) -> None:
        """
        Функция анимационно сменяет подтему. Требует Scene класс для отображения анимации.
        """

        def change_same_priorities(prev: Text, new: Text) -> None:
            """
            Анимационный поврот в заданом уровня старой подтемы на новою. Как в барабане.
            Сюда приходят два случая: когда нужно вывести такого же уровня и более высокого уровня.
            """
            # Подготовка
            new.move_to(prev).shift(RIGHT * 2)
            # Вывод
            scene.play(
                prev.animate.shift(LEFT * 2).set_opacity(0),
                new.animate.shift(LEFT * 2).set_opacity(1),
            )
            # Изменение переменных
            self.sequence += 1
            self.current_out_texts[new_priority] = new_out_text

        new_index = self.sequence + 1

        # Если вышли за границы массива
        if new_index >= len(self.flat_paths):
            raise IndexError("Достигли конца массива. Вывод подтемы невозможен.")

        # new_index, new_path, new_priority, new_name - это то, что должно быть выведено по итогу
        new_path, new_name = self.flat_paths[new_index]
        new_priority = len(new_path)

        # Текст класса manim для вывода
        new_out_text = Text(new_name, font_size=15, fill_opacity=0)
        scene.add(new_out_text)

        # Если это первый вывод
        if self.sequence == -1:
            # Подготовка
            top = (
                scene.camera.frame_center[1] + scene.camera.frame_height / 2
            )  # Смещение
            new_out_text.move_to([0, top, 0] + UP * (1.0 - 0.125))
            # Вывод
            scene.play(new_out_text.animate.shift(DOWN).set_opacity(1))
            # Перезапсь переменных
            self.current_out_texts[new_priority] = new_out_text
            self.sequence += 1
            # Остановка функции
            return

        # Если это уже не первый вывод
        # Переменные о прошлой подтеме
        prev_path, _ = self.flat_paths[self.sequence]
        prev_priority = len(prev_path)
        prev_out_text = self.current_out_texts.get(prev_priority)

        # Если нужно вывести тему более низкого уровня
        if new_priority > prev_priority:
            buff_between_out_texts = 0.15
            # Создаём линию
            out_line = Line(
                start=RIGHT * (buff_between_out_texts + 0.5),
                end=LEFT * (buff_between_out_texts + 0.5),
                stroke_width=DEFAULT_STROKE_WIDTH * 0.5,
            ).next_to(
                prev_out_text, DOWN, buff=buff_between_out_texts / 2
            )  # manim класс

            scene.play(Create(out_line))  # Вывод
            self.current_out_lines[new_priority] = out_line  # Обновление переменной

            # Подготовка
            new_out_text.move_to(prev_out_text)
            # Вывод
            scene.play(
                new_out_text.animate.next_to(
                    prev_out_text, DOWN, buff=buff_between_out_texts
                ).set_opacity(1)
            )
            # Обновление переменных
            self.sequence += 1
            self.current_out_texts[new_priority] = new_out_text
            return

        # Если нужно вывести тему такого-же уровня
        if new_priority == prev_priority:
            # Прокрутка
            change_same_priorities(prev_out_text, new_out_text)
            # Остановка функции
            return

        # Если требуется вывести подтему более высокго уровня
        if new_priority < prev_priority:
            target_text = self.current_out_texts[new_priority]
            # Втягивание всех подтем более низкого уровня
            for priority in sorted(self.current_out_texts.keys(), reverse=True)[
                :prev_priority
            ]:
                if priority > new_priority:
                    line = self.current_out_lines.get(priority)
                    text = self.current_out_texts.get(priority)
                    scene.play(
                        FadeOut(line), text.animate.move_to(target_text).set_opacity(0)
                    )
                    if line:
                        del self.current_out_lines[priority]
                    if text:
                        del self.current_out_texts[priority]

            # Проворот
            change_same_priorities(target_text, new_out_text)
            # Остановка функции
            return

        # Если никакой из if не сработал, значит есть ошибка проверки
        raise RuntimeError("update_subtheme func didn't decide IF-block to make return")


# Глобальный экземпляр SubthemeHandler
global_subtheme_handler = SubthemeHandler()

# Глобальный экземпляр Solution
global_solution = Solution()

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
        # ПОДТЕМА
        global_subtheme_handler.update_subtheme(self)

        # МНОГОУГОЛЬНИК
        # Множители маштаба
        coord_multipliers = [1.5, 1.5, 0]

        # Добавление видимых точек многоугольника
        polygon_dots_list = VGroup()

        for polygon_dot_position in polygon_dots_positions_list:
            polygon_dot_position.append(0)
            for i in range(3):
                polygon_dot_position[i] = polygon_dot_position[i] * coord_multipliers[i]

            polygon_dots_list.add(
                Dot(
                    point=polygon_dot_position,
                    color=WHITE,
                )
            )

        # Создание общей группы
        polygon = Polygon(*polygon_dots_positions_list, color=WHITE)

        # Смещение в центр
        global comb_polygon
        comb_polygon = VGroup(polygon, polygon_dots_list)
        comb_polygon.move_to(ORIGIN)

        # ВЫВОД
        self.wait()

        # Отрисовка многоугольника
        self.play(
            LaggedStart(
                Create(polygon_dots_list, rate_func=linear),
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
        guard_view_coords = global_solution.calculate_visibility(polygon, guard)
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
            [(x, y, 0) for x, y in global_solution.calculate_visibility(polygon, guard)]
        )
        guard_view.add_updater(updater_func)
        path = VMobject(fill_opacity=0).set_points_smoothly(
            [
                guard.get_center(),
                polygon_dots_list[0].get_center() + DOWN * 0.5,
                polygon_dots_list[-8].get_center() + RIGHT * 0.5 + UP,
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
                    for polygon_dot in polygon_dots_list
                )
            )
            self.wait(0.25)
        self.wait()

        # Перемещения охранника в угол
        guard_view.add_updater(updater_func)
        self.play(guard.animate.move_to(polygon_dots_list[-8].get_center()))
        guard_view.clear_updaters()
        self.wait()

        # Создание новых охранников, которые полностью осматривают многоугольник

        # Удаление
        self.play(
            AnimationGroup(
                Uncreate(guard_view),
                Uncreate(guard),
                LaggedStart(
                    Create(polygon_dots_list, rate_func=lambda a: 1 - linear(a)),
                    Create(polygon, rate_func=lambda a: 1 - linear(a)),
                    lag_ratio=0.1,
                ),
                run_time=5,
            )
        )
        self.wait()


class Algorithm(Scene):
    """
    Показ работы алгоритма Стива Фиска
    """

    def construct(self):

        # Обновление подтемы
        # global_subtheme_handler.init_subtheme(self)
        # global_subtheme_handler.update_subtheme(self)

        # Добавление и сдвиг многоугольника
        self.add(comb_polygon)
        self.play(
            AnimationGroup(
                comb_polygon.animate.shift(RIGHT * config.frame_width / 4),
                comb_polygon.animate.scale_to_fit_width(config.frame_width / 2 * 0.85),
            )
        )
        comb_polygon[0].set_z_index(1)
        comb_polygon[1].set_z_index(2)
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
        global triangles
        triangles_ids = global_solution.triangulate(comb_polygon[0])
        triangles = VGroup()

        for triangle_id in triangles_ids:
            dot1_i, dot2_i, dot3_i = triangle_id
            triangle_coords = [
                comb_polygon[1][dot1_i].get_center(),
                comb_polygon[1][dot2_i].get_center(),
                comb_polygon[1][dot3_i].get_center(),
            ]
            triangles.add(
                Polygon(
                    *triangle_coords,
                    color=GRAY,
                    stroke_width=DEFAULT_STROKE_WIDTH * 0.5,
                    joint_type=LineJointType.BEVEL,
                )
            )
        self.play(
            Write(steps[0], run_time=2), Create(triangles, lag_ratio=0.2, run_time=4)
        )
        self.wait()

        # Шаг 2. Раскраска
        color_groups = global_solution.tricolor(
            triangles=triangles_ids,
            polygon_verts_count=len(polygon_dots_positions_list),
        )
        color_variants = (PURE_BLUE, PURE_GREEN, PURE_RED)
        animations: List[Animation] = []

        for i in range(3):
            for vert_id in color_groups[i]:
                vert = comb_polygon[1][vert_id]
                animations.append(vert.animate.set_color(color_variants[i]))

        comb_polygon[1].set_z_index(comb_polygon[0].z_index + 1)
        self.play(
            LaggedStart(
                *animations,
                run_time=3,
            ),
            Write(steps[1]),
        )

        indications = []
        for dot in comb_polygon[1]:
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
        color_poly_groups: VGroup[VGroup[Dot]] = VGroup()
        color_poly_arranged_groups: VGroup[VGroup[Dot]] = VGroup()
        for color_group in color_groups:
            color_poly_group = VGroup()
            for vert_id in color_group:
                color_poly_group.add(comb_polygon[1][vert_id])
            color_poly_groups.add(color_poly_group)
            color_poly_arranged_groups.add(
                color_poly_groups[-1].copy().arrange_in_grid(cols=3)
            )

        for i in color_poly_arranged_groups[1:]:
            color_poly_arranged_groups[i].next_to(
                color_poly_arranged_groups[i - 1], buff=MED_LARGE_BUFF
            )
        color_poly_arranged_groups.move_to(ORIGIN).to_edge(DOWN).shift(
            config.frame_width / 4
        )

        self.play(
            Write(steps[3]), Transform(color_poly_groups, color_poly_arranged_groups)
        )
        self.wait()

        # Удаление
        deletions: List[Animation] = []
        for mobj in self.mobjects:
            if mobj is comb_polygon:
                continue
            if isinstance(mobj, SVGMobject):
                deletions.append(Unwrite(mobj))
            elif isinstance(mobj, VMobject):
                deletions.append(Uncreate(mobj))
            else:
                deletions.append(FadeOut(mobj))
        self.play(AnimationGroup(*deletions))
        self.wait()


class Triangulation(Scene):
    """
    Подробное описание метода отрезания ушей.
    """

    def construct(self):
        def degenerate_triangle(triangle: Polygon) -> None:
            """
            Функция анимационно удаляет треугольник (`triangle`). \n
            Запускать, если построенный треугольник не подходит под определене уха
            """
            self.play(
                Succession(triangle.animate.set_fill(RED), Uncreate(triangle)),
            )
            self.wait()

        # Создание shapely-многоугольника
        shapely_polygon = ShapelyPolygon(comb_polygon[0])

        # Вывод определения
        ear_defenition = Tex(
            r"Вершна $v_i$ простого многоугольника $P$ называется \underline{\textbf{ухом}}, если диагональ $v_{i-1}v_{i+1}$ полностью лежит внутри $P$ и внутри $\triangleupv_{i-1}v_{i}v_{i+1}$ не лежит других вершин $P$"
        )
        self.play(Write(ear_defenition))
        self.wait()
        self.play(Unwrite(ear_defenition))
        self.wait()

        # Добавление и сдвиг многоугольника
        self.add(comb_polygon)
        self.play(
            AnimationGroup(
                comb_polygon.animate.move_to(ORIGIN),
                comb_polygon.animate.scale_to_fit_height(config.frame_height * 0.9),
            ),
        )
        self.wait()

        # Добавление треугольников
        for i in range(3):
            shapely_triangle = ShapelyPolygon(
                [comb_polygon[1][i + bias].get_center()[:2] for bias in (-1, 0, 1)]
            )
            manim_triangle = Polygon(
                *[comb_polygon[1][i + bias].get_center() for bias in (-1, 0, 1)],
                color=GRAY,
                joint_type=LineJointType.BEVEL,
            )
            self.play(
                Succession(
                    Create(manim_triangle),
                    manim_triangle.animate.set_fill(ORANGE, 0.35),
                ),
            )
            self.wait()
            is_ear = shapely_polygon.covers(shapely_triangle)
            if is_ear:
                self.play(manim_triangle.animate.set_fill(GREEN_E.darker(0.35)))
                for vert in comb_polygon[1][i + 2 : i - 1]:
                    vert.set_color(YELLOW)
                    if shapely_triangle.covers(ShapelyPoint(vert.get_center()[:2])):
                        self.wait()
                        vert.set_color(RED)
                        self.wait()
                        degenerate_triangle(manim_triangle)
                        vert.set_color(WHITE)
                        break
                    else:
                        self.wait()
                self.play(
                    Succession(
                        manim_triangle.animate.set_fill(GREEN),
                        manim_triangle.animate.set_fill(opacity=0),
                    )
                )
                cut_lines = VGroup(
                    *[
                        Line(
                            comb_polygon[1][i].get_center(),
                            comb_polygon[1][i + bias].get_center(),
                        )
                        for bias in (-1, 1)
                    ]
                )
                cut_lines.add(comb_polygon[1][i].copy())
                del comb_polygon[1][i]
                self.play(Uncreate(cut_lines))
                self.wait()

            else:
                degenerate_triangle(manim_triangle)

        self.play(FadeOut(comb_polygon))

        self.play(FadeIn(triangles[-1]))
        self.wait()
        self.play(AnimationGroup(FadeIn(comb_polygon), FadeIn(triangles)))
        self.wait()


class Tricoloring(Scene):
    def construct(self):
        pass
