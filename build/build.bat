@echo off
title Builder

set NAME=social-warriors_0.02a

:main
call :pyInstaller
del /F /Q .\dist\%NAME%\%NAME%.exe.manifest
del /F /S /Q .\dist\%NAME%\certifi
rmdir .\dist\%NAME%\certifi
mkdir .\dist\%NAME%\bundle
echo.
echo [MANUAL] Move all files to the bundle folder (except game folders, base_library.zip and python3X.dll).
pause>NUL
exit

:pyInstaller
echo [+] Starting pyInstaller...
python -m Pyinstaller ^
 --onedir ^
 --console ^
 --noupx ^
 --noconfirm ^
 --runtime-hook=".\path_bundle.py" ^
 --add-data "..\..\assets;assets" ^
 --add-data "..\..\config;config" ^
 --add-data "..\..\stub;stub" ^
 --add-data "..\..\templates;templates" ^
 --add-data "..\..\villages;villages" ^
 --paths ..\. ^
 --workpath .\work ^
 --distpath .\dist ^
 --specpath .\bundle ^
 --icon=..\icon.ico ^
 --name %NAME% ..\server.py
REM --debug bootloader
echo [+] pyInstaller Done.
EXIT /B 0