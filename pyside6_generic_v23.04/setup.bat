set cPath=%cd%
set PYTHON_DIR=%cPath%\python\
set PATH=C:\WINDOWS\system32;C:\WINDOWS;%PYTHON_DIR%;%PYTHON_DIR%\Scripts;

xcopy .\source\python-3.10.11-embed-amd64-pip %PYTHON_DIR% /eY
xcopy .\source\app .\bin\ /eY

python %PYTHON_DIR%\get-pip.py
pip install --upgrade pip
pip install virtualenv
python -m virtualenv --copies .venv

call .venv\Scripts\activate.bat

pip install --upgrade pip
pip install pyside6

python .\bin\main.py
pause