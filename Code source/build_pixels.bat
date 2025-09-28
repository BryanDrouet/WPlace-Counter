@echo off
REM === Compilation de l'application en .exe avec PyInstaller ===
python -m PyInstaller --noconsole --onefile --icon=icon.ico pixels_gui.py

echo.
echo ✅ Compilation terminee !
echo Ton .exe se trouve dans le dossier "dist"
pause
