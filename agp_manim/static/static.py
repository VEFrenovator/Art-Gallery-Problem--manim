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

---

# Общее назначение
Рендер статических изображений для вставки в реферат.
"""

from typing import Callable, Dict
import os
from manim import *
import shapely
from PIL import Image, ImageOps
import shapely.plotting
import matplotlib.pyplot as plt
from agp_manim.utils import solution


# Прозрачный фон
config.format = "png"
config.transparent = True

# Стили
POLY_STYLE = {
    "fill_opacity": 0,
    "stroke_color": BLACK,
    "stroke_width": DEFAULT_STROKE_WIDTH * 1.75,
    "joint_type": LineJointType.BEVEL,
}

VERTS_STYLE = {
    "radius": DEFAULT_DOT_RADIUS * 5,
    "color": BLACK,
}

TRIANGLE_STYLE = {
    "stroke_color": GRAY,
    "stroke_width": POLY_STYLE["stroke_width"] * 0.8,
    "z_index": -1,
    "joint_type": LineJointType.BEVEL,
}

BORDER_SIZE = 100


def trim_transparent(func: Scene.construct) -> Callable:
    """Обрезка прозрачных полос на изображении"""

    def wrapper(self: Scene, *args, **kwargs):

        # Вызов основной функции
        original_result = func(self, *args, **kwargs)

        # Загрузка изображения
        fp = "media/images/static/"
        img_name = f"{self.__class__.__name__}_ManimCE_v0.19.1.png"

        if os.path.exists(fp + img_name):
            print("File exists, trimming...")
            with Image.open(fp + img_name) as img:
                # Обрезка прозрачных полос
                trimmed = img.crop(img.getbbox())

                # Сохранение результата
                trimmed.save(fp + "trimmed/" + img_name)
        else:
            print(f"File {fp + img_name} does not exist.")

        return original_result

    return wrapper


def add_border(border: int = BORDER_SIZE) -> Callable:
    """Добавление прозрачных полей"""

    def decorator(func: Scene.construct) -> Callable:
        def wrapper(self: Scene, *args, **kwargs):

            # Вызов основной функции
            original_result = func(self, *args, **kwargs)

            # Загрузка изображения
            fp = "media/images/static/"
            img_name = f"{self.__class__.__name__}_ManimCE_v0.19.1.png"
            if os.path.exists(fp + "trimmed/" + img_name):
                print("File exists, adding border...")
                with Image.open(fp + "trimmed/" + img_name) as img:
                    # Добавление полей
                    padded = ImageOps.expand(
                        img,
                        border=border,
                        fill=(
                            0,
                            0,
                            0,
                            0,
                        ),
                    )

                    # Сохранение результата
                    padded.save(fp + "padded/" + img_name)
            else:
                print(f"File {fp + img_name} does not exist.")

            return original_result

        return wrapper

    return decorator


def vectorize_polygon_verts(polygon: Polygon, verts_style: Dict = VERTS_STYLE):
    verts = VGroup()
    for coords in polygon.get_vertices():
        verts.add(Dot(coords, **verts_style))
    return verts


def vectorize_triangles(
    triangles_ids, polygon: Polygon, triangle_style: Dict = TRIANGLE_STYLE
):
    triangles = VGroup()
    for triangle_ids in triangles_ids:
        coords = []
        for i in triangle_ids:
            coords.append(polygon.get_vertices()[i])
        triangles.add(Polygon(*coords, **triangle_style))
    return triangles


def emulate_three_d(coords_2d):
    """Convert an iterable of 2D coordinates to 3D by adding z=0.

    Example: [[x,y], ...] -> [[x,y,0], ...]
    """
    return [[x, y, 0] for x, y in coords_2d]


class SomeObviousConclusions(Scene):

    @add_border()
    @trim_transparent
    def construct(self):
        LOC_VERT_STYLE = VERTS_STYLE.copy()
        LOC_VERT_STYLE["radius"] = DEFAULT_DOT_RADIUS * 3

        # n = 3 (треугольник)
        trigon = Polygon(
            *emulate_three_d(
                [
                    [1.36249, 2.27082],
                    [3.0777, -1.23984],
                    [-2.92052, -1.24987],
                ]
            ),
            **POLY_STYLE,
        )
        trigon_group = VGroup(trigon, vectorize_polygon_verts(trigon, LOC_VERT_STYLE))

        # n = 4
        tetragon = Polygon(
            *emulate_three_d(
                [
                    [-0.70379, 2],
                    [0.86097, -1.70124],
                    [-2.92052, -1.2498],
                    [-1.09497, -0.5878],
                ]
            ),
            **POLY_STYLE,
        )
        tetragon_group = VGroup(
            tetragon, vectorize_polygon_verts(tetragon, LOC_VERT_STYLE)
        )

        # n = 5
        pentagon = Polygon(
            *emulate_three_d(
                [
                    [0, 0],
                    [-1.2354, -0.88877],
                    [0.18893, 2.2307],
                    [1.01142, 0.51549],
                    [2.88712, -0.6681],
                ]
            ),
            **POLY_STYLE,
        )
        pentagon_group = VGroup(
            pentagon, vectorize_polygon_verts(pentagon, LOC_VERT_STYLE)
        )

        # Вывод
        out = VGroup(
            trigon_group,
            tetragon_group,
            pentagon_group,
        ).arrange()
        out.scale_to_fit_width(config.frame_width)
        self.add(out)


class SteveFiskAlgorithm(Scene):

    @add_border()
    @trim_transparent
    def construct(self):
        # Вершины
        poly_coords = [
            [-1.75269, 1.64231],
            [1.6772, 0.45203],
            [4.88783, 3.44339],
            [7.4867, -2.3881],
            [2.70498, -4.29285],
            [-0.64817, -0.95954],
            [-4.08069, -1.57461],
        ]
        # Полигон без обозначений
        poly = Polygon(*emulate_three_d(poly_coords), **POLY_STYLE)

        # Вершины
        verts = vectorize_polygon_verts(poly)

        # Триангулированный
        triangles_ids = solution.triangulate(poly)
        triangulated_poly = poly.copy()
        triangulated_verts = verts.copy()
        triangles = vectorize_triangles(triangles_ids, poly)
        triangulated_group = VGroup(triangulated_poly, triangles)

        # Трираскрашенный
        tricolor_poly = poly.copy()
        tricolor_verts = verts.copy()
        groups = solution.tricolor(triangles_ids, len(tricolor_poly.get_vertices()))

        for group, color in zip(groups, (PURE_RED, PURE_BLUE, PURE_GREEN)):
            for vert_i in group:
                tricolor_verts[vert_i].set_color(color)

        # Вывод
        out = VGroup(
            VGroup(poly, verts),
            VGroup(triangulated_group, triangulated_verts),
            VGroup(tricolor_poly, tricolor_verts, triangles.copy()),
        ).arrange()

        out.scale_to_fit_width(config.frame_width)

        self.add(out)


class OptimalTriangulation(Scene):

    @add_border()
    @trim_transparent
    def construct(self):
        LOC_VERTS_STYLE = VERTS_STYLE.copy()
        LOC_VERTS_STYLE["radius"] = DEFAULT_DOT_RADIUS * 3
        LOC_POLY_STYLE = POLY_STYLE.copy()
        LOC_POLY_STYLE["stroke_width"] *= 3
        LOC_TRIANGLE_STYLE = TRIANGLE_STYLE.copy()
        LOC_TRIANGLE_STYLE["stroke_width"] *= 0.5
        # Вершины
        poly_coords = [
            [-2, -2],
            [-2, 2],
            [-1, 0],
            [2, 2],
            [2, -2],
            [1, 0],
        ]
        poly = Polygon(*emulate_three_d(poly_coords), **LOC_POLY_STYLE)
        verts = vectorize_polygon_verts(poly, LOC_VERTS_STYLE)

        # Неоптимальная триангуляция (ручная)
        non_opt_triangles_ids = [[0, 1, 2], [0, 2, 3], [0, 3, 5]]
        non_opt_triangles = vectorize_triangles(
            non_opt_triangles_ids, poly, LOC_TRIANGLE_STYLE
        )

        # Оптимальная триангуляция (ручная)
        opt_triangles_ids = [
            [0, 1, 2],
            [2, 3, 5],
            [3, 4, 5],
        ]
        opt_triangles = vectorize_triangles(opt_triangles_ids, poly, LOC_TRIANGLE_STYLE)

        # Вывод
        out = VGroup(
            VGroup(poly, verts, non_opt_triangles),
            VGroup(poly.copy(), verts.copy(), opt_triangles),
        ).arrange()
        out.scale_to_fit_width(config.frame_width)
        self.add(out)


class Earcut(Scene):

    @add_border()
    @trim_transparent
    def construct(self):
        LOC_POLY_STYLE = POLY_STYLE.copy()
        LOC_POLY_STYLE["stroke_width"] *= 3
        LOC_VERTS_STYLE = VERTS_STYLE.copy()
        LOC_VERTS_STYLE["radius"] = DEFAULT_DOT_RADIUS * 3

        # Вершины
        poly_coords = [
            [-2, -2],
            [-2, 2],
            [-1, 0],
            [2, 2],
            [2, -2],
            [1, 0],
        ]
        poly = Polygon(*emulate_three_d(poly_coords), **LOC_POLY_STYLE)
        verts = vectorize_polygon_verts(poly, LOC_VERTS_STYLE)

        # Показ главной вершины с диагональю внутри и снаружи
        DOT_SCALING = 1.45
        triangle_inside = Polygon(
            poly.get_vertices()[0],
            poly.get_vertices()[1],
            poly.get_vertices()[2],
            color=GREEN,
            stroke_width=LOC_POLY_STYLE["stroke_width"],
            stroke_color=GREEN_E,
            fill_opacity=1,
            z_index=-1,
        )
        verts[1].set_color(PURPLE).scale(DOT_SCALING)

        triangle_outside = Polygon(
            poly.get_vertices()[0],
            poly.get_vertices()[4],
            poly.get_vertices()[5],
            color=RED,
            stroke_width=LOC_POLY_STYLE["stroke_width"],
            stroke_color=RED_E,
            fill_opacity=1,
            z_index=-1,
        )
        verts[5].set_color(ORANGE).scale(DOT_SCALING)

        # Вывод
        out = VGroup(poly, verts, triangle_inside, triangle_outside)
        out.scale_to_fit_height(config.frame_height)
        self.add(out)


class TriangulationTheorem(Scene):

    @add_border()
    @trim_transparent
    def construct(self):
        LOC_VERTS_STYLE = VERTS_STYLE.copy()
        LOC_VERTS_STYLE["radius"] /= 5
        LOC_POLY_STYLE = POLY_STYLE.copy()
        DASH_LEN = DEFAULT_DASH_LENGTH * 4
        DASHED_RATIO=0.75
        # Вершины
        poly_coords = [
            [0, -2],
            [2, 0],
            [6, 2],
            [0, 2],
            [0.5, -0.5],
            [0, -1],
            [-1, 2],
            [-2, 0],
        ]
        poly = Polygon(*emulate_three_d(poly_coords), **LOC_POLY_STYLE)
        verts = vectorize_polygon_verts(poly, LOC_VERTS_STYLE)

        # Неправильная диагональ
        wrong_diagonal = DashedLine(
            poly.get_vertices()[1],
            poly.get_vertices()[7],
            stroke_color=RED,
            stroke_width=LOC_POLY_STYLE["stroke_width"],
            dash_length=DASH_LEN,
            dashed_ratio=DASHED_RATIO,
            z_index=-1
        )

        # Правильная диагональ
        right_diagonal = DashedLine(
            poly.get_vertices()[0],
            poly.get_vertices()[5],
            stroke_color=GREEN,
            stroke_width=LOC_POLY_STYLE["stroke_width"],
            dash_length=DASH_LEN,
            dashed_ratio=DASHED_RATIO,
            z_index=-1
        )

        # Параллельная прямая
        parallel = (
            Line(
                wrong_diagonal.get_start(),
                wrong_diagonal.get_end(),
                stroke_width=LOC_POLY_STYLE["stroke_width"],
                z_index=-1
            )
            .shift(DOWN)
            .stretch_to_fit_width(config.frame_width)
            .set_color(YELLOW_E)
        )

        # Поиск точек пересечения отрезков и параллельной прямой
        intersection = shapely.intersection(
            shapely.Polygon(poly_coords),
            shapely.LineString([parallel.get_start()[:2], parallel.get_end()[:2]]),
        )
        intersection_dots = VGroup()
        for part in intersection.geoms:
            for coords in part.coords:
                dot = Dot(
                    list(coords) + [0],
                    radius=LOC_VERTS_STYLE["radius"],
                    color=parallel.get_color(),
                )
                intersection_dots.add(dot)

        # Группировка и вывод
        out = VGroup(
            poly, verts, wrong_diagonal, right_diagonal, parallel, intersection_dots
        ).scale_to_fit_height(config.frame_height)
        self.add(out)


class Tricoloring(Scene):
    
    @add_border()
    @trim_transparent
    def construct(self):
        LOC_POLY_STYLE = POLY_STYLE.copy()
        LOC_POLY_STYLE["stroke_width"] *= 3
        tri1 = Polygon(*emulate_three_d([
            [-1,-1],
            [2,-1],
            [1,2],
        ]), **LOC_POLY_STYLE)
        tri1_verts = vectorize_polygon_verts(tri1, { "radius": VERTS_STYLE["radius"] / 1.25 })
        tri1_verts[0].set_color(PURE_RED)
        tri1_verts[1].set_color(PURE_GREEN)
        tri1_verts[2].set_color(PURE_BLUE)

        tri2 = Polygon(*emulate_three_d([
            [2, -1],
            [4,1],
            [1,2],
        ]), **LOC_POLY_STYLE)
        tri2_verts = Dot(tri2.get_vertices()[1], VERTS_STYLE["radius"] / 1.25, fill_color=WHITE, stroke_width=15,  stroke_color=PURE_RED)

        out = VGroup(tri1, tri2, tri1_verts, tri2_verts).move_to(ORIGIN).scale_to_fit_height(config.frame_height * 0.95)
        self.add(out)
