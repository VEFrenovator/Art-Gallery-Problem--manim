"""math: Базовая математическая библиотека;
manim: Основная анимационная библиотека.
    Примечание. Не обращай внимания на Wildcard предупреждение.
    Если написать import manim, то это не будет соответсвовать документации
    manim;
shapely: Продвинутая геометрии библиотека. Использую для нахождения пересечений."""

import math
from manim import *
from shapely.geometry import (
    Polygon as ShapelyPolygon,
    Point as ShapelyPoint,
    LineString,
)


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
            ["Введение", [
                ["Формулировка", []],
                ["Некоторые очевидные выводы", []]
            ]],
            ["Решение Стива Фиска", [
                ["Триангуляция", [
                    ["Жадный алгоритм", []],
                    ["Триангуляция выпуклого многоугольника", []],
                    ["Метод отрезания ушей", [
                        ["Некоторые определения", []],
                        ["Некоторые теоремы", [
                            ["Триангуляционная теорема", []],
                            ["Теорема о двух ушах", []]
                        ]],
                        ["Алгоритм нахождения уха и оценка вычислительной сложности", []],
                        ["Алгоритм триангуляции и оценка вычислительной сложности", []],
                        ["Вывод о методе триангуляции путём отрезания ушей", []]
                    ]]
                ]],
                ["Раскраска вершин", []],
                ["Остатки от деления", []],
                ["Вывод о решении Стива Фикса", []]
            ]],
            ["Заключение и напутствие", []]
        ]

        # Дерево subtheme_variants, но развёрнутое в список путей (pre-order)
        self.flat_paths = [] # Список путей в кортежах (путь, название)
        self._unpack(self.subtheme_variants, [])
        self.sequence = -1  # Номер подтемы в flat_path

        self.current_out_texts: dict[int, Text] = {} # {приоритет: текст}
        self.current_out_lines: dict[int, Line] = {} # {приоритет: линия}. Примечание: линии
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
                new.animate.shift(LEFT * 2).set_opacity(1)
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
            top = scene.camera.frame_center[1] + scene.camera.frame_height / 2  # Смещение
            new_out_text.move_to([0, top, 0] + UP * (1. - 0.125))
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
                stroke_width=DEFAULT_STROKE_WIDTH * 0.5
            ).next_to(
                prev_out_text, DOWN, buff=buff_between_out_texts / 2
            )   # manim класс

            scene.play(Create(out_line))    # Вывод
            self.current_out_lines[new_priority] = out_line # Обновление переменной

            # Подготовка
            new_out_text.move_to(prev_out_text)
            # Вывод
            scene.play(
                new_out_text.animate.next_to(
                    prev_out_text,
                    DOWN,
                    buff=buff_between_out_texts
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
            for priority in sorted(
                self.current_out_texts.keys(),
                reverse=True
            )[:prev_priority]:
                if priority > new_priority:
                    line = self.current_out_lines.get(priority)
                    text = self.current_out_texts.get(priority)
                    scene.play(
                        FadeOut(line),
                        text.animate.move_to(target_text).set_opacity(0)
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

# Русский шрифт
rus_text_template = TexTemplate(
    tex_compiler="xelatex",
    output_format=".xdv",
    preamble=r"""\usepackage{polyglossia}
\setmainlanguage{russian}
\usepackage{fontspec}
\setmainfont{Times New Roman}"""
)

class Greetings(Scene):
    """
    Класс отображения приветственного текста (тема и автор).
    """

    def construct(self):
        # Приветственный текст
        theme = Text(
            "Теорема о картинной галереи",
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


class TableOfContents(Scene):
    def construct(self):
        out_lines = []
        line = Tex("Table of Content", tex_template = rus_text_template)
        for i, (path, name) in enumerate(global_subtheme_handler.flat_paths):
            num_str = ".".join(str(i+1) for i in path)
            out_lines.append(num_str)
        self.play(Write(VGroup(Text(line for line in out_lines))))
        self.wait()
        self.play(Write())

class ProblemDescription(Scene):
    """
    Класс отрисовки картинной галереи, отображения поля видимости.
    В течении действия рассказываю о сути проблемы.
    """

    def len_of_two_dim_list(self, list: list) -> int:
        ans = 0
        for row in list:
            ans += len(row)
        return ans

    # ОХРАННИК
    def is_segment_inside_polygon(self, segment: Line, polygon: Polygon) -> bool:
        """
        Функция определяет, лежит ли отрезок внутри многоугольника (даже если
        отрезок касается вершин многоугольника).
        """

        # Преобразуем manim Polygon в список координат
        poly_coords = [tuple(p)[:2] for p in polygon.get_vertices()]
        shapely_poly = ShapelyPolygon(poly_coords)

        # Преобразуем manim Line в shapely LineString
        seg_coords = [tuple(segment.get_start())[:2], tuple(segment.get_end())[:2]]
        shapely_line = LineString(seg_coords)

        # Проверим, лежит ли отрезок строго внутри полигона (без касания границы)
        # contains проверяет, что вся геометрия строго внутри без касаний границы
        return shapely_poly.contains(shapely_line)

    def create_guard_view(self, guard: Dot, gallery: Polygon) -> Polygon:
        """
        Функция, рассчитывающая поле зрения охранника внутри галереи и возвращающая
        это поле зрения в качестве многоугольника.
        ПРИМЕЧАНИЕ. Не анимирует многоугольник.
        """

        view_points_coords = [] # Массив координат видимых точек
        gallery_corners = gallery.get_vertices()    # Массив вершин галереи
        incoherent_view_points = []

        # Создаём shapely-классы
        shapely_guard = ShapelyPoint(*guard.get_center()[:2])
        shapely_gallery = ShapelyPolygon([tuple(p)[:2] for p in gallery_corners])

        # Проверяем, внутри ли галереи охранник. Если нет, возвращаем ошибку
        if not shapely_gallery.covers(shapely_guard):
            raise ValueError(f"Guard (coords = {guard.get_center()}) not in gallery")

        # Проверяем, видит ли охранник вершину галереи. Для этого перебираем все вершины
        view_points_stop_i = len(gallery_corners)
        wall_angle_i = -1
        while wall_angle_i < view_points_stop_i:
            wall_angle_i += 1
            wall_angle_i %= len(gallery_corners)
            wall_angle = gallery_corners[wall_angle_i]
            # Если линия (help_line) от охранника до вершины внутри многоугольника, значит
            # вершина видна
            help_line = Line(guard.get_center(), wall_angle)
            if self.is_segment_inside_polygon(help_line, gallery):

                # Если вершина видна, сначала добавляем её в локальный массив. Мы не
                # добавляем её сразу в view_points_coords потому, что за ней
                # может быть ещё одна видимая точка и тогда нужно правильно указать
                # порядок обхода, вычисления которого нужно производить после
                # нахождение этой самой второй точки.
                incoherent_view_points = [wall_angle]

                # Следующие шаги посвещены нахождению точки "за углом"
                # Шаг 1. Продлеваем help_line на расстояние диагонали bounding box
                # Шаг 1.1. Находим координаты bounding box с помощью метода bounds (bbox_coords)
                bbox_coord = shapely_gallery.bounds
                # и его диагонать (max_calc_dist) по Теореме пифагора
                bb_dx = bbox_coord[2] - bbox_coord[0]
                bb_dy = bbox_coord[3] - bbox_coord[1]
                max_calc_dist = math.sqrt(
                    bb_dx**2 + bb_dy**2
                )

                # Шаг 1.2. Продлеваем help_line
                start = help_line.get_start()
                end = help_line.get_end()
                direct = end - start
                new_end = start + abs(max_calc_dist) * direct
                # +создаём shapely-класс
                shapely_help_line = LineString([start, new_end])

                # Шаг 2. Ищем пересечения с многоугольником
                intersection = shapely_gallery.boundary.intersection(shapely_help_line)

                # Шаг 3. Трансформируем все найденные точки пересечения в массив (ips)
                if not intersection.is_empty:
                    match intersection.geom_type:
                        case "Point":
                            ips = [intersection]
                        case "MultiPoint":
                            ips = list(intersection.geoms)
                        case _:
                            ips = []
                    # Шаг 4. Обрабатываем каждую точку пересечения (иными словами проверяем,
                    # видит ли её охранник)
                    for ip in ips:
                        x, y = ip.coords[0][:2]
                        possible = [x, y, 0]
                        if self.is_segment_inside_polygon(
                            Line(guard.get_center(), possible), gallery
                        ):
                            incoherent_view_points.append(possible)

            # Теперь обрабатываем incoherent_view_points

            if self.len_of_two_dim_list:
                # Если видна 1 вершина или ни одна - просто добавляем, потом отчищаем.
                # В этом случае порядок обхода не имеет значения
                view_points_coords.append(incoherent_view_points)
                incoherent_view_points.clear()
                print("Hello!")
                print()
            
            elif len(incoherent_view_points) == 2 and self.len_of_two_dim_list(view_points_coords) > 0:
                # Если созданы две вершины, тогда:
                pa = LineString([view_points_coords[-1], incoherent_view_points[1]])
                both_vg = [
                    LineString(
                        [
                            incoherent_view_points[0],
                            gallery_corners[wall_angle_i - 1],
                        ]
                    ),
                    LineString(
                        [
                            incoherent_view_points[0],
                            gallery_corners[wall_angle_i + 1],
                        ]
                    ),
                ]
                # Если отрезок PA *не* пересекает один из отрезков VG порядок обхода A->V
                if pa.intersection(both_vg[0]).is_empty or pa.intersection(both_vg[1]):
                    view_points_coords.append(incoherent_view_points[-1])
                    incoherent_view_points.clear()

                # Если отрезок PA пересекает один из отрезков VG, порядок обхода V->A
                else:
                    view_points_coords.append(incoherent_view_points)
                    incoherent_view_points.clear()

                # Примачание:
                # P (Previous visible) - последний элемент view_points_coords
                # V (polygon's Visible) - видимая точка, являющаяся вершиной галереи
                # A (polygon's Additive) - новая поставленная точка
                # [Пара точек] G (gallery) - две вершины галереи, имеющие свясь с точкой V
            else:
                incoherent_view_points.clear()
                view_points_stop_i += 1

        # Возврат
        if len(view_points_coords) < 3:
            raise ValueError(
                f"Need at least 3 coords to create a Polygon, has {len(view_points_coords)}."
            )
        return Polygon(*view_points_coords)

    def construct(self):
        # ПОДТЕМА
        global_subtheme_handler.update_subtheme(self)

        # МНОГОУГОЛЬНИК
        # Множители маштаба
        coord_multipliers = [1.5, 1.5, 0]

        # Координаты
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
        comb_polygon = VGroup(polygon, polygon_dots_list)
        comb_polygon.move_to(ORIGIN)

        # ВЫВОД
        self.wait()

        # Отрисовка многоугольника
        self.play(
            AnimationGroup(
                Create(polygon, run_time=3),
                Create(polygon_dots_list, run_time=3),
                lag_ratio=1,
            )
        )
        self.wait()

        # Мерцание вершин
        for _ in range(2):
            self.play(AnimationGroup(Indicate(polygon_dot, scale_factor=2, lag_ratio=0) for polygon_dot in polygon_dots_list))
            self.wait(0.25)

        # Отрисовка охранника
        guard = Dot([-0.5, 0, 0], 0.12, color=RED)
        self.play(Create(guard))
        self.wait()

        # Отрисовка поля зрения
        guard_view = self.create_guard_view(guard, polygon).set_z_index(-1).set_fill(GREEN, 0.75)
        self.play(GrowFromPoint(guard_view, guard))
        self.wait()


#                 for i, v in enumerate(list(shapely_gallery.exterior.coords[:-1])):  # Перебор всех сторон многоугольник
#                     wall_start = v
#                     wall_end = gallery_corners[i % len(gallery_corners)]
#                     if wall_start != wall_angle and wall_end != wall_angle:
#                         wall = LineString([wall_start, wall_end])
                        
#                         common_point = wall.intersection(guard_view_shapely_line)
#                         if not common_point.is_empty and:   # Точка пересечение - нужная точка

#                             view_points_coords.append(common_point)
#                             break   # Точка персечения единственна, птому останавливаем цикл

                
#                 guard_view_shapely_line = LineString(
#                     [
#                         shapely_guard.coords[0],
#                         shapely_scale(
#                             geom=shapely_guard,
#                             xfact=max_calc_dist,
#                             yfact=max_calc_dist,
#                             origin=shapely_guard.coords[0],
#                         ).coords[0],
#                     ]
#                 )

# from shapely.affinity import scale as shapely_scale
