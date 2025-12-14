@echo off
title Builder

set NAME=social-warriors_0.02a

:main
call :pyInstaller

set TARGET=.\dist\%NAME%
set BUNDLE=%TARGET%\bundle

echo [+] Creating bundle folder...
mkdir "%BUNDLE%" 2>NUL

echo [+] Moving runtime folders into bundle...
for %%D in (
    assets
    config
    templates
    villages
    stub
) do (
    if exist "%TARGET%\%%D" (
        echo     -> %%D
        move "%TARGET%\%%D" "%BUNDLE%" >NUL
    )
)

echo [+] Build + bundling finished successfully.
pause
exit /b

:pyInstaller
echo [+] PyInstaller version:
pyinstaller --version

echo [+] Starting PyInstaller...
pyinstaller ^
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

echo [+] PyInstaller Done.
exit /b 0
