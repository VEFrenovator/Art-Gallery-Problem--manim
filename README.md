<p align="center">
  <img src=https://github.com/VEFrenovator/Art-Gallery-Theorem--manim/blob/main/ArtGalleyTheoremLogo_ManimCE_v0.19.0.png>
  <br />
  <br />
  <i>A ManimCE animation explaining <b>Fisk's proof</b> of the solution to the <b>Art Gallery Problem</b></i>
  <br />
  <br />
  <i>by VEFrenovator</i>
</p>

---

> [!NOTE]
> This file is *translated on other languages*!
> - **ENG** English (current)
> - [**RUS** Русский](https://github.com/VEFrenovator/Art-Gallery-Problem--manim/blob/main/README-ru.md)

> [!NOTE]
> #### Versions sheet
> This `Python v3.11` project uses the following libraries:
> - `ManimCE v0.19.0`
> - `Shapely v2.1.1`
> - `Mapbox-earcut v1.0.3`
> - ***Only for `slides_animation.py`:*** `manim-slides v5.5.1`
> - *Python built-ins: `typing`, `math`*

> [!IMPORTANT]
> All comments (in code) and texts (in animation) are written in ***Russian***. The author welcomes pull requests with an English version.

# Installation
## Manim and other PyPI libraries
> [!WARNING]
> This installation method may not be universal. It is recommended to consult each module's documentation to avoid issues.

All libraries listed in the versions sheet (*excluding Python built-ins*) can be installed via `cmd` or `PowerShell` (on Windows) using the 
```cmd
pip install [...package name...]
```
command.

> [!NOTE]
> The installation process for manim-slides may differ slightly. For details, refer to the [manim-slides documentation/installation](https://manim-slides.eertmans.be/latest/installation.html#installation).

## Files installation
To install the project, run `git clone` or download the `raw` files directly. For more details, see [Cloning a repository](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository).

# Animation classes description
> [!TIP]
> The order of classes (in this document and in the code) follows their logical sequence. Use this order during presentations.

## `Greetings`
The `Greetings` class displays the project's theme and author.  
To modify the theme or author, update the `theme` or `author` variables.

## `TableOfContents`
Converts a *multi-dimensional Python list* of subthemes from `subtheme_handler.py/SubthemeHandler/subtheme_variants` into a *multi-level `VGroup` list* and animates it.

## `ProblemDescription`
Displays task conditions for the Art Gallery Problem:
- The observer has *360° visibility at all times*
- The observer must be placed *on a polygon vertex*

As of 17.07.2025 (D/M/Y), `ProblemDescription` **does not** include these Art Gallery Theorem conditions but should:
- The polygon is *simple*
- We seek the *minimum number* of observers for general cases

## `Algorithm`
The `Algorithm` class illustrates key steps of [Steve Fisk's proof](https://en.wikipedia.org/wiki/Art_gallery_problem):
1. *Triangulate* the polygon (without adding vertices)
2. *Tricolor* vertices so each triangle contains all three colors
3. Place observers at vertices of the least-used color

## `Triangulation`
Demonstrates polygon triangulation using the ear-clipping method.

## `Tricoloring`
> [!NOTE]
> This class is incomplete.

# Files descriptions and usage

> [!WARNING]
> Some texts in `animation.py` and `slides_animation.py` require LaTeX rendering. Review the full [Manim installation guide](https://docs.manim.community/en/stable/installation.html).

## `animation.py`

> [!CAUTION]
> Some animations in this module are DEPRECATED. All changes and updates are located in `slides_animation.py`.


Contains standard Manim animations. Render using the [ManimCE rendering process](https://github.com/ManimCommunity/manim?tab=readme-ov-file#usage) to output `.mp4` files.

## `slides_animation.py`
Contains animations identical to `animation.py` but with interactive pauses. See [manim-slides quickstart](https://manim-slides.eertmans.be/latest/quickstart.html).

## `solution.py`
Provides computational functions:
- `calculate_visibility` – Computes an observer's field of view within a polygon. Returns visible area coordinates.

> [!CAUTION]
> As of 17.07.2025 (D/M/Y), `calculate_visibility` **does not** work correctly when the observer is on an edge/vertex.

- `triangulate` – Performs polygon triangulation via `mapbox_earcut.triangulate_float32`. Returns triangle vertex indices (e.g., `(0, 1, 2)` = triangle from first three polygon vertices).
- `tricolor` – Assigns three colors to triangulation vertices where each triangle contains all colors. `polygon_verts_count` specifies original vertex count. Returns `tuple[set, set, set]` of color groups.

## `subtheme_handler.py`
> [!NOTE]
> This section is incomplete.

# License
Licensed under MIT. Copyright © VEFrenovator ([LICENSE.md](https://github.com/VEFrenovator/Art-Gallery-Theorem--manim/blob/main/LICENSE.md)).
