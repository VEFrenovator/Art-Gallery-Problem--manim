from manim import *
from shapely.geometry import (
    Polygon as ShapelyPolygon,
    Point as ShapelyPoint,
    LineString,
)
from shapely.affinity import scale as shapely_scale
import math


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


class IntroText(Scene):
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
        out_lag_ratio = 0.8

        self.wait()
        self.play(AnimationGroup(Write(text_out_group), lag_ratio=out_lag_ratio))
        self.wait()
        self.play(AnimationGroup(Unwrite(text_out_group), lag_ratio=out_lag_ratio))
        self.wait()


class SubthemeHandler(Scene):
    def __init__(self):
        self.sequence = 0
        self.subthemes = [
            "Проблема",
            "Решение Стива Фиска",
            "Триангуляция",
            "Раскраска",
            "Остатки",
            "Заключение"
        ]

    def set_subtheme(self, subtheme_name: str | None) -> None:
        if subtheme_name not in self.subthemes:
            raise ValueError(f"Given subtheme '{subtheme_name}' doesn't exist in the list of subthemes")

        if subtheme_name is not None:
            self 


class ProblemDescription(Scene):
    # ОХРАННИК
    def is_segment_inside_polygon(self, segment: Line, polygon: Polygon) -> bool:

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
        view_points_coords = []
        gallery_corners = gallery.get_vertices()

        # Проверяем, внутри ли галереи охранник
        shapely_guard = ShapelyPoint(*guard.get_center()[:2])
        shapely_gallery = ShapelyPolygon([tuple(p)[:2] for p in gallery_corners])

        if not shapely_gallery.covers(shapely_guard):
            raise ValueError(f"Guard (coords = {guard.get_center()}) not in gallery")

        # Проверяем, видит ли точку охранник
        for wall_angle in gallery_corners:
            help_line = Line(guard.get_center(), wall_angle)

            # Проверяем, видит ли охранник точку
            if self.is_segment_inside_polygon(help_line, gallery):
                view_points_coords.append(wall_angle)

                # Проверяем, видит ли охранник точку за углом (проверяем для всех углов, даже меньше 180)
                bbox_coord = shapely_gallery.bounds
                bb_dx = bbox_coord[2] - bbox_coord[0]
                bb_dy = bbox_coord[3] - bbox_coord[1]
                max_calc_dist = math.sqrt(
                    bb_dx**2 + bb_dy**2
                )  # Диагональ ограничевающего прямоугольника для галереи

                # Продлеваем отрезок зрения охраника
                start = help_line.get_start()
                end = help_line.get_end()
                direct = end - start
                new_end = start + abs(max_calc_dist) * direct
                #help_lines.add(Line(start, new_end))

                shapely_help_line = LineString([start, new_end])

                intersection = shapely_gallery.boundary.intersection(
                    shapely_help_line
                )

                if not intersection.is_empty:
                    match intersection.geom_type:
                        case "Point":
                            ips = [intersection]
                        case "MultiPoint":
                            ips = list(intersection.geoms)
                        case _:
                            ips = []
                
                    for ip in ips:
                        x, y = ip.coords[0][:2]
                        possible = [x, y, 0]
                        if self.is_segment_inside_polygon(
                            Line(guard.get_center(), possible),
                            gallery
                        ):
                            view_points_coords.append(possible)
                            
        if len(view_points_coords) < 3:
            raise ValueError(f"Need at least 3 coords to create a Polygon, has {len(view_points_coords)}.")
        return Polygon(*view_points_coords)
        #return help_lines


    def construct(self):
        # ЛОКАЛИЗАЦИЯ (выключено)
        # global rus_text_template

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
            self.play(
                AnimationGroup(
                    *[
                        dot.animate.set_color(YELLOW_E).scale(2.5)
                        for dot in polygon_dots_list
                    ],
                    run_time=1,
                )
            )

            self.play(
                AnimationGroup(
                    *[
                        dot.animate.set_color(WHITE).scale(1 / 2.5)
                        for dot in polygon_dots_list
                    ],
                    run_time=1,
                )
            )

            self.wait(0.25)

        # Отрисовка охранника
        guard = Dot([-0.5, 0, 0], 0.12, color=PURE_RED)
        self.play(Create(guard))

        self.wait()

        self.add(self.create_guard_view(guard, polygon).set_fill(GREEN, 0.75))

        self.wait()


"""
                for i, v in enumerate(list(shapely_gallery.exterior.coords[:-1])):  # Перебор всех сторон многоугольник
                    wall_start = v
                    wall_end = gallery_corners[i % len(gallery_corners)]
                    if wall_start != wall_angle and wall_end != wall_angle:
                        wall = LineString([wall_start, wall_end])
                        
                        common_point = wall.intersection(guard_view_shapely_line)
                        if not common_point.is_empty and:   # Точка пересечение - нужная точка

                            view_points_coords.append(common_point)
                            break   # Точка персечения единственна, птому останавливаем цикл
"""
"""
                
                guard_view_shapely_line = LineString(
                    [
                        shapely_guard.coords[0],
                        shapely_scale(
                            geom=shapely_guard,
                            xfact=max_calc_dist,
                            yfact=max_calc_dist,
                            origin=shapely_guard.coords[0],
                        ).coords[0],
                    ]
                )
"""
