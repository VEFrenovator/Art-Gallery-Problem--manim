"""math: Базовая математическая библиотека;
manim: Основная анимационная библиотека.
    Примечание. Не обращай внимания на Wildcard предупреждение.
    Если написать import manim, то это не будет соответсвовать документации
    manim;
shapely: Продвинутая геометрии библиотека. Использую для нахождения пересечений."""

import math
from manim import *
from shapely import (
    LineString,
    Polygon as ShapelyPolygon,
    Point as ShapelyPoint,
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

    def _angle_and_dist(self, observer, point):
        """
        Возвращает пару (angle, dist2) от observer к point:
        - angle  — угол в радианах (atan2),
        - dist2  — квадрат евклидова расстояния.
        """
        dx = point[0] - observer[0]
        dy = point[1] - observer[1]
        return math.atan2(dy, dx), dx*dx + dy*dy

    def _build_edges(self, polygon):
        """Возвращает список Shapely LineString-ребер для заданного списка вершин."""
        edges = []
        n = len(polygon)
        for i in range(n):
            a = polygon[i]
            b = polygon[(i+1) % n]
            edges.append(LineString([a, b]))
        return edges

    def _cast_ray(self, observer, angle, edges, max_dist=1e6):
        """
        Стреляет лучом из observer под углом angle, 
        возвращает координаты ближайшего пересечения с edges или None.
        """
        ox, oy = observer
        dx = math.cos(angle)
        dy = math.sin(angle)
        far = (ox + dx * max_dist, oy + dy * max_dist)
        ray = LineString([observer, far])

        closest_pt = None
        min_dist2 = float('inf')
        for edge in edges:
            inter = ray.intersection(edge)
            if inter.is_empty:
                continue
            # Могут быть MultiPoint, обрабатываем все
            points = inter.geoms if hasattr(inter, 'geoms') else [inter]
            for p in points:
                d2 = (p.x - ox)**2 + (p.y - oy)**2
                if d2 < min_dist2:
                    min_dist2 = d2
                    closest_pt = (p.x, p.y)
        return closest_pt

    def compute_visibility(
            self,
            polygon: list[tuple[float, float]] | Polygon,
            observer: tuple[float, float] | Dot,
            epsilon=1e-8,
        ):
        """
        Возвращает список вершин полигона видимости из observer внутри polygon.

        epsilon  — угол отклонения для «щелей» (по умолчанию 1e-8).
        """
        # 0) Проверяем классы
        if polygon is Polygon:
            polygon = [tuple(coords[:2]) for coords in polygon.get_vertices()]
        if observer is Dot:
            observer = tuple(observer.get_center()[:2])
        
        # Проверяем, что охранник внутри галерее
        if not ShapelyPoint(observer).covered_by(ShapelyPolygon(p)):
            raise ValueError(f"Guard with coords {observer} is not in gallery")

        # 1) Собираем все уникальные углы к вершинам
        base_angles = set()
        for p in polygon:
            ang, _ = self._angle_and_dist(observer, p)
            base_angles.add(ang)

        # 2) Генерируем «расщеплённые» углы
        angles = []
        for ang in base_angles:
            angles.extend((ang - epsilon, ang, ang + epsilon))

        # 3) Строим ребра и «стреляем» всеми лучами
        edges = self._build_edges(polygon)
        hits = []
        for ang in angles:
            pt = self._cast_ray(observer, ang, edges)
            if pt is not None:
                hits.append((ang, pt))

        # 4) Дедуплицируем по углу, оставляя ближайшую точку
        nearest = {}
        for ang, pt in hits:
            _, d2 = self._angle_and_dist(observer, pt)
            if ang not in nearest or d2 < self._angle_and_dist(observer, nearest[ang])[1]:
                nearest[ang] = pt

        # 5) Сортируем по углу и возвращаем только точки
        result = [nearest[ang] for ang in sorted(nearest)]
        return result

    def construct(self):
        # ПОДТЕМА
        # global_subtheme_handler.update_subtheme(self)

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

        
        guard_view_coords = self.compute_visibility(polygon, guard)
        guard_view = Polygon(
            *[(x, y, 0) for x, y in guard_view_coords],
            stroke_opacity=0,
            fill_color=GREEN,
            fill_opacity=1,
            z_index=-1,
        )
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
