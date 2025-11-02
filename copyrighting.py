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
"""

from manim import *


class CopyrightMark(VGroup):
    def __init__(
        self,
        author: str | None = "VEFrenovator",
        year: int | None = 2025,
        license: str | None = "MIT",
        full_copyright_text: str | None = None,
        **kwargs,
    ):
        if full_copyright_text:
            self.text = Text(full_copyright_text, font="Courier New", weight=BOLD)
        elif author and license and year:
            self.text = Text(
                f"Credit by {author}. Copyright © {year} {author}. Licensed under {license}",
                font="Courier New",
                weight=BOLD,
            )
        else:
            raise ValueError(
                """
                CopyrightMark class __init__ function has not enougth arguments to form
                copyright information text. Please, provide author & year & license or 
                full_copyright_text.
                """
            )

        self.text.scale_to_fit_width(config.frame_width / 2).to_edge(DOWN)
        self.rect = SurroundingRectangle(self.text, color=WHITE, buff=MED_SMALL_BUFF)
        super().__init__(self.text, self.rect, **kwargs)


class CreateCopyrightMark(AnimationGroup):
    def __init__(self, copyright_mark: CopyrightMark, **kwargs):
        super().__init__(
            Write(copyright_mark.text),
            Create(copyright_mark.rect),
            **kwargs,
        )


class UncreateCopyrightMark(AnimationGroup):
    def __init__(self, copyright_mark: CopyrightMark, **kwargs):
        super().__init__(
            Unwrite(copyright_mark.text),
            Uncreate(copyright_mark.rect),
            **kwargs,
        )
