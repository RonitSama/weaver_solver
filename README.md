# weaver_solver
A functional solver for the widely-played word game Weaver at https://wordwormdormdork.com/. Programmed in CPython.

The simplest analogy for Weaver is a word ladder. The starting and ending words are given, and the task is to come up with words to connect them. The trick is that each succeeding word may only have a one-letter difference. For example, a valid word to follow "same" is "fame", and an invalid word would be "fume". To get to "fume", you would need to have "same" -> "fame" -> "fume".

/src/solver.py is the main file to run. Make sure to change the path to your Chromedriver in /src/solve_on_site.py.

IF NOT USING CHROMEDRIVER (therefore not letting the program open Chrome and solve the day's challenge), there is no need to download the Selenium package. Just input "n" to the prompt ("Automate? (y/n/t):  ") in terminal.

ELSE, Selenium package is REQUIRED from (https://pypi.org/project/selenium/) as well as a Chromedriver from (https://chromedriver.chromium.org/downloads). The Chromdriver version MUST match YOUR Chrome version, or /src/solve_on_site.py WILL NOT WORK. Also make sure to change the path to your Chromedriver in /src/solve_on_site.py.

Final solution will be in /src/solution.txt once /src/solver.py is run. If not, make sure the terminal directory is whatever directory all the code is in and run it again. If using Chromedriver, the solution will automatically begin inserting into https://wordwormdormdork.com/ once found. Incorrect answers are possible because Weaver's word bank is not public so this program uses nearly every 4-letter word in the English language. If encountered, the solver handles it (removes the incorrect word from the word bank and re-solves) if and only if Chromedriver and Selenium are being used. The incorrect word will never be considered again, as it is permanently removed from /src/word_bank.py.

PLEASE do not click off of Chrome while the program is running; the website may open an ad that the program cannot deal with and the program will crash unhandled. These ads are outside of Selenium's capabilities to deal with, so there is no clear workaround other than: don't click off.

Note: if today's challenge uses 5-letter words, this solver will not function. As mentioned previously, it is hard-coded with 4-letter words (/src/words.py) so the solver won't be able to test any 5-letter words for the solution.


Please enjoy!
