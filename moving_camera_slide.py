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

This module provides a custom class combines Manim MovingCameraScene and Slide from manim_slides.
"""

from manim import MovingCameraScene
from manim_slides import Slide

class MovingCameraSlide(MovingCameraScene, Slide):  # pylint: disable=inherit-non-class
    """A class that combines MovingCameraScene and Slide functionality.
    If there are any conflicts between the two parent classes, redefine this class as follows:
    ```
    class MovingCameraSlide(MovingCameraScene, Slide):
        pass
    ```
    """
    def __init__(self, **kwargs):
        # Ensure Slide initializes first so it does not override the MovingCamera later.
        Slide.__init__(self, **kwargs)
        MovingCameraScene.__init__(self, **kwargs)
