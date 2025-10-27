def tricolor(triangles, polygon_verts_count):
    def find_third_non_colored(triangle):
        """
        Некоторая функция, которая возвращает третью не закрашенную
        вершыну треугольника И целевой цвет этой вершины.

        Если же в треугольнике количество уже закрашенных вершин
        не равно 2, возвращает None
        """

    # Объявляем группы цветов
    list color_a
    list color_b
    list color_c

    # Окрашиваем все вершины первого треугольника, чтобы группы не
    # были пустыми
    add v1 of triangle1 into color_a
    add v2 of triangle1 into color_b
    add v3 of triangle1 into color_c

    # Окрашиваем остальные вершины
    while length(color_a) + length(color_b) + length(color_c) < polygon_verts_count:
        for triangle in triangles:
            non_colored = find_third_non_colored(triangle)
            if non_colored is not None:
                get target_color, vertex from non_colored
                add vertex of triangle into target_color
    
    return color_a, color_b, color_c
