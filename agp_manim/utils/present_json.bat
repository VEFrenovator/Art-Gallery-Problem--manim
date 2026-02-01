@echo off
set /p scenes=Enter scene name(-s) to present: 
manim-slides.exe present --start-paused -F -H -S 0 --info-window-screen 1 %scenes%
