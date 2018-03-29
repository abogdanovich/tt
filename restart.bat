ECHO taskkill PYTHON
taskkill /IM python.exe /f
ECHO runserver PYTHON
"c:\Program Files\nginx-1.7.3\bin\RunHiddenConsole.exe" python "d:\Projects\timetracker\tt\manage.py" runserver 0.0.0.0:8000