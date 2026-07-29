<p align="center">
  <img src=./Readme_illustrations/ArtGalleyTheoremLogo_ManimCE_v0.19.0.png>
  <br />
  <br />
  <i>A project with a <a href="https://github.com/VEFrenovator/Art-Gallery-Problem--manim/tree/main/media/videos/slides_animation/2160p60">ManimCE animation</a>, a <a href="https://github.com/VEFrenovator/Art-Gallery-Problem--manim/blob/main/slides/conv/full_touchscreen.html">presentation</a> and a <a href="https://github.com/VEFrenovator/Art-Gallery-Problem--manim/blob/main/documents/SiS_EXP_%D0%97%D0%B0%D0%B4%D0%B0%D1%87%D0%B0%20%D0%BE%20%D0%BA%D0%B0%D1%80%D1%82%D0%B8%D0%BD%D0%BD%D0%BE%D0%B9%20%D0%B3%D0%B5%D0%BB%D0%B5%D1%80%D0%B5%D0%B5%20%D0%A2%D1%80%D0%B8%D0%B0%D0%BD%D0%B3%D1%83%D0%BB%D1%8F%D1%86%D0%B8%D1%8F.pdf">report</a> explaining <b><a href="https://en.wikipedia.org/wiki/Art_gallery_problem#Fisk's_short_proof">Fisk's solution</a></b> to the <b><a href="https://en.wikipedia.org/wiki/Art_gallery_problem">Art Gallery Problem</a>.</b></i>
  <br />
  <i>by VEFrenovator</i>
  <br />
  <br />
  <b><i>From author:</i></b> I'm now only entering the github community and I'll be happy for <i>any</i> your response. Suggestions, tips, pieces of advice — write me anything you want or consider necessary. You can use the <a href="https://github.com/VEFrenovator/Art-Gallery-Problem--manim/discussions">Discussions page</a> or my <a href="mailto:vladimir_e11@outlook.com"> email</a>.
</p>

---

# What is this project about?

This repository was created while working on my individual final project. The main issue comes from a visibility problem in computational geometry — the [Art Gallery Problem](https://en.wikipedia.org/wiki/Art_gallery_problem). Inspired by [3blue1brown](https://www.youtube.com/c/3blue1brown) channel, I created an animation covering the key aspects of the problem statement, the [Fisk's solution](https://en.wikipedia.org/wiki/Art_gallery_problem#Fisk's_short_proof) and the real-world application of the solution.

> [!IMPORTANT]
> 
> **Non-full English support**
> 
> The main language of the project is Russian. This is actually not a big problem, because the animation does not contains a lot of text, but you clearly have to translate them, what requeues working with code, if you are going to take a speech with it. Also, comments in code are mostly Russian.
>
> **I really welcome pull requests with an English version, or even asking issues — please, contact me and I will try to set aside my time to make changes and rerender the animations in English.** For now, there is only readme translated.

# Before start: how it was ^_~. Gallery

Some scenes from the animation, charts from the report and the presentation itself :)

<table width="100%" border="0" cellpadding="5">
  <tr>
    <td><video src="./media/videos/slides_animation/2160p60/ProblemDescription.mp4#t=0:00:02" controls width="100%"></video></td>
    <td><video src="./media/videos/slides_animation/2160p60/Triangulation.mp4#t=20,40" controls width="100%"></video></td>
  </tr>
</table>

<details>
  <summary>Expand to see more from the Gallery! (ps. x = cos x and x - (cos x) = 0 just kind of got into the frame on my presentation).</summary>

  <table width="100%" border="0" cellpadding="5">
    <tr>
      <td><video src="./media/videos/slides_animation/2160p60/Algorithm.mp4#t=0:00:01" controls width="100%"></video></td>
      <td><video src="./media/videos/slides_animation/2160p60/Greetings.mp4#t=0:00:01" controls width="100%"></video></td>
    </tr>
    <tr>
      <td><video src="./media/videos/slides_animation/2160p60/Tricoloring.mp4#t=0:00:04" controls width="100%"></video></td>
      <td><video src="./media/videos/slides_animation/2160p60/Examples.mp4#t=0:00:04" controls width="100%"></video></td>
    <tr>
      <td style="text-align: center;"><img src="./media/images/static/trimmed/Earcut_ManimCE_v0.19.1.png" alt="Earcut triangulation process chart" width="25%"></td>
      <td><img src="./media/images/static/trimmed/SteveFiskAlgorithm_ManimCE_v0.19.1.png" alt="Steve Fisk algorithm chart"></td>
    </tr>
    <tr>
      <td style="text-align: center;"><img src="./Readme_illustrations/presentation_1_blurred.png" alt="Presentation photo 1" width="50%"></td>
      <td style="text-align: center;"><img src="./Readme_illustrations/presentation_2_blurred.png" alt="Presentation photo 2" width="90%"></td>
    </tr>
  </table>
</details>

---

# Installation

> [!TIP]
> 
> **Before installing anything**, decide if you really need it. It is possible to see the animations and the presentation without installing anything. See more in the [Quick User Guide, or FAQ](#quick-user-guide-or-faq) section.

## Standard install

<!-- The following installation process 
To simplify the work, a python package called **`agp-manim`** (shortened from the name of the repo). Unfortunately, it is not on github releases or PyPi (for now). The easiest way is to

1) Clone the repo
2) Install the package using a `./pyproject.toml` script via pip. -->
Execute the following commands:

```bash
git clone --recurse-submodules https://github.com/VEFrenovator/Art-Gallery-Problem--manim
cd Art-Gallery-Problem--manim
pip install -e .
```

After executing, the `agp-manim` python lib will be available in your current python environment, and you will be able to 

```python
import agp-manim
```

in your python files.

<!-- > [!NOTE]
> **Edibility (`-e` flag)**
> 
> If you clearly are **not** going to make changes in the source code, you can drop the `-e` flag (aka "editable package"), but everything will still work with it, too. -->

> [!IMPORTANT]
> 
> **Limited functionality**
> 
> The agp-manim itself **does not** provide important libs and has limited functionality. The installation process above provides only the "Base package", as stated in the Custom install table. See more in the [Custom install](#custom-install) section below.


## Custom install

In this table, you can see the abilities of different installation preferences. The table is sorted by the increasing number of installed packages and abilities. You can choose the best that fits your needs.

<!-- 
Name | Command(s) | Packages installed | Abilities
:--: | :--------: | :----------------: | :-------:
Repo | `git clone --recurse-submodules https://github.com/VEFrenovator/Art-Gallery-Problem--manim` | — (repo files only) | To open files locally, including 4k `.mp4` rendered media; Run `.html` presentation using your installed browser.
Base package | (See [Standard install section](#standard-install) above) | _Everything from Repo_ + `agp-manim, setuptools, requests, importlib-metadata` | _Everything from Repo_ + To import the `agp-manim` lib and its submodules in your python files
`manim-slides-present` package | _All commands from Base_ + `pip install -e .[manim-slides-present]` | _Everything from Base_ + `manim-slides[full], PyQt6, PySide6` | _Everything from Base_ + To run the presentation using `.json` manim-slides files
`dev` package | _All commands from Base_ + `pip install -e .[dev]` | _Everything from `manim-slides-present`_ + `numpy, shapely, mapbox-earcut, pillow, manim` | _Everything from `manim-slides-present`_ + To run and render any `.py` file in the repo, and to lead the development of the project (e.g., to add new features, fix bugs, etc.)
`full` package **(alias for `dev`)** | _All commands from Base_ + `pip install -e .[full]` | _Everything from `dev`_ | _Everything from `dev`_ 
-->


Name | Command(s) | Packages installed | Abilities
:--: | :--------: | :----------------: | :-------:
Repo | `git clone --recurse-submodules https://github.com/VEFrenovator/Art-Gallery-Problem--manim` | — (repo files only) | To open files locally, including 4k `.mp4` rendered media; Run `.html` presentation using your browser.
Base package | <u><i>All commands from [Standard install section](#standard-install) above</i></u> | <u><i>Everything from Repo</i></u> + `agp-manim, setuptools, requests, importlib-metadata` | <u><i>Everything from Repo</i></u> + To import the `agp-manim` lib and its submodules, classes and functions in your python files
`manim-slides-present` package | <u><i>All commands from Base</i></u> + `pip install -e .[manim-slides-present]` | <u><i>Everything from Base</i></u> + `manim-slides[full], PyQt6, PySide6` | <u><i>Everything from Base</i></u> + To run the presentation using `.json` manim-slides files
`dev` package | <u><i>All commands from Base</i></u> + `pip install -e .[dev]` | <u><i>Everything from <code>manim-slides-present</code></i></u> + `numpy, shapely, mapbox-earcut, pillow, manim` | <u><i>Everything from <code>manim-slides-present</code></i></u> + To run and render any `.py` file in the repo, and to lead the development of the project (e.g., to add new features, fix bugs, etc.)
`full` package **(alias for `dev`)** | <u><i>All commands from Base</i></u> + `pip install -e .[full]` | <u><i>Everything from <code>dev</code></i></u> | <u><i>Everything from <code>dev</code></i></u>


# Quick User Guide, or FAQ

This section is a shorted version of the full user guide. For better compression, subsections' titles are like questions, and the answers are inside.

<details>
  <summary>I want to see the animation and/or presentation, but I don't want to install anything. Can I do so?</summary>

  **Yes, almost.**

  You can find the rendered 4k animation's scenes in the [`./media/videos/slides_animation/2160p60`](https://github.com/VEFrenovator/Art-Gallery-Problem--manim/tree/main/media/videos/slides_animation/2160p60) folder and download them separately. Similarly, the presentation is available in the [`./slides/conv`](https://github.com/VEFrenovator/Art-Gallery-Problem--manim/tree/main/slides/conv) folder. There are many `.html` presentation files, but the main is [`full_touchscreen.html`](https://github.com/VEFrenovator/Art-Gallery-Problem--manim/tree/main/slides/conv/full_touchscreen.html). For more information about others, see

</details>

<!-- <details>
  <summary></summary>
</details> -->

# How to contribute

There are a huge field of freedom in helping this project! For guidlines, ideas and more, see [CONTRIBUTING.md](https://github.com/VEFrenovator/Art-Gallery-Theorem--manim/blob/main/LICENSE.md).

# License

Licensed under MIT. Copyright © 2025 VEFrenovator. For license text, see [LICENSE.md](https://github.com/VEFrenovator/Art-Gallery-Theorem--manim/blob/main/LICENSE.md).
