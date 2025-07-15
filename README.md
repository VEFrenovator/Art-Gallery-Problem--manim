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
> #### Versions sheet
> This `Python v3.11` project use follow libraries:
> - `ManimCE v0.19.0`
> - `Shapely v2.1.1`
> - `Mapbox-earcut v1.0.3`
> - ***Only for `slides_animation.py`:*** `manim-slides v5.5.1`
> - *Python built-ins: `typing`, `math`*

> [!IMPORTANT]
> All comments and texts are written in ***Russian***. The author welcomes creating a pull request with an English version.

# Installation
## Manim and other PyPl libraries
> [!WARNING]
> This installation method may not be universal. It is recommended to consult each module's documentation to avoid issues.

All libraries listed in the versions sheet (*excluding python built-ins*) are installed via `cmd` or `PowerShell` (on Windows) using 
```cmd
pip install [...package name...]
```
command.
> [!NOTE]
> The installation process for manim-slides may differ slightly. For details, refer to the [manim-slides documentation/installation](https://manim-slides.eertmans.be/latest/installation.html#installation).

## Files installation
To install the project, run `git clone` or download the `raw` file directly. For more details, see [Clonning a repository](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository).

# Files descriptions and usage
## `animation.py`
The `animation.py` file contains standart manim animations. Rendering follows the standard [ManimCE rendering process](https://github.com/ManimCommunity/manim?tab=readme-ov-file#usage) and outputs an `.mp4` file.
> [!WARNING]
> Some texts in `animation.py` and `slides_animation.py` requers LaTeX rendering. Please, read the full [manim installation process](https://docs.manim.community/en/stable/installation.html#installation).

## `slides_animation.py`
The animations in `slides_animation.py` are identical to those in `animation.py` but include pauses at key points. Learn more about manim-slides at [manim-slides documentation/quickstart](https://manim-slides.eertmans.be/latest/quickstart.html#quickstart).

## `solution.py`
There are no animations in this file because this module contains some functions which are:
- `calculate visibility` - Computes an observer's field of view within a polygon. Returns the visible area as a list of coordinates.
- `tirangulate` - Performs polygon triangulation using the mapbox_earcut method. Returns a list of triangle vertex indices relative to the original polygon vertices. For example, (0, 1, 2) indicates a triangle formed by the first three vertices of the polygon.
- `tricolor` – Assigns three colors to triangulation vertices such that each triangle contains all three colors. The polygon_verts_count parameter specifies the original polygon's vertex count. Returns a tuple of three sets, each containing vertices for a specific color group.

## `subtheme_handler.py`
> [!IMPORTANT]
> This section is incomplete.

# License
The project is licensed under the MIT license, with copyright held by VEFrenovator (see [LICENSE.md](https://github.com/VEFrenovator/Art-Gallery-Theorem--manim/blob/main/LICENSE.md)).
