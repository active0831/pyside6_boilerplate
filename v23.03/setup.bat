rem mkdir %userprofile%\Desktop\Django_server_template
rem cd %userprofile%\Desktop\Django_server_template
python -m venv venv
.\venv\Scripts\python.exe -m pip install --upgrade pip
.\venv\Scripts\python.exe -m pip install pyside6

xcopy .\source /e .\bin\
.\venv\Scripts\python.exe .\bin\main.py
pause