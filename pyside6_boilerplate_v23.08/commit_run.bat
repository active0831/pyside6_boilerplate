call set_path.bat

xcopy .\source\app .\bin\ /eY

call .venv\Scripts\activate.bat

python .\bin\main_window.py

pause