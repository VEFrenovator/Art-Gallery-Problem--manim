def triangulate(polygon):
    # Объявляем переменную триангулированного многоугольника
    triangulated_polygram = Polygram()

    # Пока многоугольник не стал треугольником
    while polygon is not Triangle:
        # ...проверяем все вершины
        for vertex in polygon.get_vertexes():
            possible_ear = Triangle(prev_vertex, vertex, next_vertex)
            # проверяем, является ли ухом
            if (
                vertex is Convex and
                not polygon.get_vertexes() not inside possible_ear
            ):
                # если да, отрезаем и добавляем в триангуляцию
                polygon.degenerate(possible_ear)
                triangulated_polygram.add(possible_ear)
    
    return triangulated_polygram