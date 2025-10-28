<p align="center">
  <img src=https://github.com/VEFrenovator/Art-Gallery-Theorem--manim/blob/main/ArtGalleyTheoremLogo_ManimCE_v0.19.0.png>
  <br />
  <br />
  <i>Компьютерная анимация на ManimCE, объясняющая <b>решение Стива Фиска</b> для <b>задачи о картинной галерее</b></i>
  <br />
  <br />
  <i>создана VEFrenovator'ом</i>
</p>

---

> [!NOTE]
> Текст этого файла *доступен на других языках!*
> - [**ENG** English](https://github.com/VEFrenovator/Art-Gallery-Theorem--manim/blob/main/README.md)
> - **RUS** Русский (текущий)


> [!NOTE]
> #### Список версий использованных библиотек
> Этот проект на `Python v3.11` использует следующие библиотеки:
> - `ManimCE v0.19.0`
> - `Shapely v2.1.1`
> - `Mapbox-earcut v1.0.3`
> - ***Только для `slides_animation.py`:*** `manim-slides v5.5.1`
> - *Встроенные в Python: `typing`, `math`*

> [!IMPORTANT]
> Все комментарии (в коде) и тексты (в анимации) написаны на ***Русском***. Автор приветствует создания Pull Request с английской версией.

# Установка
## Manim и другие PyPI библиотеки 
> [!WARNING]
> Описанный метод установки может быть неточным. Рекомендуется прочесть инструкцию по установке каждой отдельной библиотеки во избежание проблем.

Все библиотеки, перечисленные в списке использованных библиотек (*не включая встроенные в Python*), могут быть установлены через `cmd` или `PowerShell` (в Windows), используя комманду
```cmd
pip install [...package name...]
```

> [!NOTE]
> Установка manim-slides может немного отличаться. Для уточнения деталей, прочитайте [manim-slides documentation/installation](https://manim-slides.eertmans.be/latest/installation.html#installation).

## Установка файлов проекта
Для установки всего проекта, запустите `git clone` или установите `raw`-файлы по отдельности. Для уточнения деталей, прочитайте [Cloning a repository](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository).

# Описание классов анимации в `slides_animation.py`
> [!TIP]
> Порядок классов здесь и в коде таков же, как и их смысловой порядок. Используйте приведённый порядок при своём выступлении.

## `Greetings`
Класс `Greetings` показывает тему и автора проекта.  
Чтобы изменить тему или автора проекта, измените одноименные переменные.

## `TableOfContents`
Конвертирует *многомерный массив* из `subtheme_handler.py/SubthemeHandler/subtheme_variants` в *многоуровневый отображаемый список, заключенный в одну `VGroup`* и анимирует её.

## `ProblemDescription`
Отоброжает ключевые условия задачи о картинной галерее, а именно:
- Наблюдатель смотрит *на 360° в каждый момент времени*
- Наблюдатель должен быть расположен *на вершине многоугольника*

На момент 17.07.2025 (Д/М/Г), `ProblemDescription` **не** отображает сдедующих условий задачи, но должен:
- Многоугольник *простой*.
- Мы ищем *верхнюю границу* для количества наблюдателей в общем случае.

## `Algorithm`
Класс `Algorithm` иллюстрирует ключевые шаги [Доказательства Стива Фиска](https://en.wikipedia.org/wiki/Art_gallery_problem):
1. *Триангулировать* многоугольник (без добавления новых вершин).
2. *Расскрасть все вершины многоугольника* так, чтобы в каждом треугольнике триангуляции были вершины всех трёх цветов.
3. Разместить наблюдателей в вершинах цвктовой группы с меньшим числом вершин.

## `Triangulation`
Демонстрирует триангуляцию многоугольника методом отрезания ушей.

## `Tricoloring`
> [!NOTE]
> Работа над этим классом всё ещё ведется.

# Описание файлов и их использование

> [!WARNING]
> Некоторые тксты в `animation.py` и `slides_animation.py` требуют LaTeX рендера. Прчитайте весь [Manim installation guide](https://docs.manim.community/en/stable/installation.html).

## `animation.py`

> [!CAUTION]
> Некоторые анимации в этом файле УСТАРЕЛИ. Все новые анимации и авторские обновления помещаются в `slides_animation.py`.

Содержит стандартные анимации manim, описанные выше. Рендер в соответствии с [ManimCE rendering process](https://github.com/ManimCommunity/manim?tab=readme-ov-file#usage) выдаст`.mp4` файл.

## `slides_animation.py`
Содержит анимации, идентичные `animation.py` но с интерактивными паузами. Для уточнения деталей, читайте [manim-slides quickstart](https://manim-slides.eertmans.be/latest/quickstart.html).

## `solution.py`
Содержит некоторые функции для геометрических вычеслений, а именно:
- `calculate_visibility` – Расчитывает поля зрения охранника в многоугольнике. Возвращает поле зрение как список координат.

> [!CAUTION]
> На момент 17.07.2025 (Д/М/Г), `calculate_visibility` **не** работает коректно в случае, когда наблюдатель находится точно на ребре или вершине.

- `triangulate` – Триангулирует многоугольник, используя `mapbox_earcut.triangulate_float32`. Возвращает индексы из массива точек многоугольника, формирующие тругольники триангуляции (т.е., `(0, 1, 2)` = треугольник из первых трёх точек многоугольника).
- `tricolor` – Возвращает трираскраску точек многоугольника, в которой каждый треугольник триангуляции раскрашен в 3 цвета. Параметр `polygon_verts_count` принимает количество точек в многоугольнике. Возвращает `tuple[set, set, set]`, отображающий три группы разных цветов.

## `subtheme_handler.py`
> [!NOTE]
> Работа над этим разделом всё ещё ведется.

# License
Лицензированно под MIT. Copyright © VEFrenovator ([LICENSE.md](https://github.com/VEFrenovator/Art-Gallery-Theorem--manim/blob/main/LICENSE.md)).
