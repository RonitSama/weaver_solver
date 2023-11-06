# weaver_solver
A functional solver for the widely-played word game Weaver at https://wordwormdormdork.com/. Programmed in CPython.

src/solver.py is the main file to run. This is NOT a clone-able repository; simply download the files and change the path to your Chromedriver in solve_on_site.py.

IF NOT USING CHROMEDRIVER, no need to download Selenium package. Just input "n" to prompt ("Automate? (y/n/t):  ") in terminal.

ELSE, REQUIRES Selenium package from ([https://pypi.org/project/selenium/]([url])) as well as a Chromedriver from ([https://chromedriver.chromium.org/downloads]([url])).

Chromdriver version MUST match YOUR Chrome version, or solve_on_site.py WILL NOT WORK.

Final solution will be in solution.txt once solver.py is run. If using Chromedriver, solution will automatically begin inserting into [https://wordwormdormdork.com/](url) once found. Incorrect answers found by the solver are handled.


Please enjoy!
