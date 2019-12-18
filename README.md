# Kayaking Web Scraper

This Python programme scrapes the onePA Kayaking website to retrieve all certification course details for 1, 2 and 3 Star.
Source: https://www.onepa.sg/cat/water-sports/subcat/kayaking

How to run it on MacOS:
1) Download the executable in `dist` and run it
2) Obtain course info from terminal

How to run it on Windows:
1) Install the required Python packages in the script
2) Run `python <script file path>` in command prompt
**Will create a compatible executable soon**

Here's the directory structure for critical files
* `build` where PyInstaller puts most metadata for building the executable
* `dist` has the FINAL EXECUTABLE for distribution
* `resource` contains the chromedriver used for scraping
* `src` includes 2 scripts which prints info on command prompt or create txt file
* `venv` contains all necessary package dependencies for scraping (virtual environment)
* `scraper.py` can be opened by any code editor (similar to .ipynb)
* `scraper.spec` encodes info on how to process script (auto created by PyInstaller)
* `courses.txt` displays all retrieved course info

Instructions for future software maintenance:
1) Pull Git repository and navigate to folder on local machine
2) Edit the abs file paths in `scraper.spec` (pathex & binaries) and `src scripts`
3) Make relevant changes to source code
4) Run `source venv/bin/activate` in command line to launch virtual environment 
5) Run `pyinstaller --onefile scraper.spec` to bundle data files into an executable
