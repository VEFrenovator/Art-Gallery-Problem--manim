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
Предоставление класса, отвечающего за управление выводом текущих подтем, что упрощает понимание
процесса доклада.
"""

from manim import *


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
            ["Алгоритм решения", [
                ["Триангуляция (без добавления новых вершин)", []],
                ["Окрашивание вершин в три цвета", []],
            ]],
            ["Применение на практике", []],
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
