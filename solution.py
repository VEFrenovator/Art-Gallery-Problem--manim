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

*Общее назначение*\n
Решение поставленной задачи. Именно теоретическое решение, а не вывод анимации.

Методы
------
`calculate_visibility` - расчет поля зрения. \n
`triangulate` - триангуляция. \n
`tricolor` - раскраска в три цвета. \n
"""

import math
from typing import Iterable, List, Tuple, Set, Optional
from manim import Polygon, Dot
from shapely.geometry import (
    Polygon as ShapelyPolygon,
    Point as ShapelyPoint,
    LineString,
)
import numpy as np
import mapbox_earcut as earcut


def calculate_visibility(
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
        if math.isclose(vx, ox, abs_tol=1e-8) and math.isclose(vy, oy, abs_tol=1e-8):
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
                        directions.add((edge_dir_x / edge_dist, edge_dir_y / edge_dist))

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
                points = [ShapelyPoint(p) for p in intersection.coords]
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
            visibility_points.append((closest_intersection.x, closest_intersection.y))

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
    polygon: List[Tuple[float, float]] | Polygon | ShapelyPolygon,
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
        polygon = np.array([coords[:2] for coords in polygon.get_vertices()]).reshape(
            -1, 2
        )
    elif isinstance(polygon, ShapelyPolygon):
        polygon = np.array([coords[:2] for coords in polygon.exterior.coords]).reshape(
            -1, 2
        )

    rings_end_i = np.array([len(polygon)])

    result = earcut.triangulate_float32(polygon, rings_end_i).tolist()
    return [tuple(result[i : i + 3]) for i in range(0, len(result), 3)]


def tricolor(
    triangles: List[Tuple[int, int, int]], polygon_verts_count: int
) -> Tuple[Set, Set, Set]:
    """
    Раскрашивает вершины треугольников (`triangles`) в три цвета так, чтобы
    в любом треугольнике было все три цвета. \n
    `polygon_verts_count` - количество вершин исходного многоугольника. Другими словами,
    длина списка `polygon_dots`. \n
    Возвращает кортеж из трёх множеств. Каждое множество отражает вершины
    треугольников, которые должны быть окрашены цветом этой группы.
    """

    group_a, group_b, group_c = set(), set(), set()
    group_a.add(triangles[0][0])
    group_b.add(triangles[0][1])
    group_c.add(triangles[0][2])

    while len(group_a) + len(group_b) + len(group_c) < polygon_verts_count:
        for triangle in triangles:
            non_colored = third_non_colored(triangle, [group_a, group_b, group_c])
            if non_colored is not None:
                index, group = non_colored
                group.add(index)
    return group_a, group_b, group_c


def third_non_colored(triangle: Tuple, groups: List) -> Optional[Tuple[int, Set]]:
    """
    Принимает один треугольник триангуляции (`triangle`) и
    группы цветов (`groups`)\n
    *Если две вершины этого треугольника уже окрашены*, возвращает
    вершину, которую нужно окрасить и множество, цветом которого
    эту вершину нужно окрасить. \n
    *Если в этом треугольнике окрашены 0, 1 или 3 вершины*, возвращает `None`.
    """
    indexes = list(triangle)

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
