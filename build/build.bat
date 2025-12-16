@echo off
title Social Warriors Build
setlocal ENABLEEXTENSIONS

REM =========================
REM PROJECT CONFIG
REM =========================
set PROJECT_ROOT=D:\programs\socialwarriors
set BUILD_DIR=%PROJECT_ROOT%\build
set VENV_PY=%PROJECT_ROOT%\venv\Scripts\python.exe
set WORK_DIR=%BUILD_DIR%\work
set DIST_DIR=%BUILD_DIR%\dist
set NAME=social-warriors_0.03a

REM =========================
REM SAFETY CHECK
REM =========================
if not exist "%VENV_PY%" (
    echo [ERROR] Python venv not found:
    echo %VENV_PY%
    pause
    exit /b 1
)

REM =========================
REM CLEAN PREVIOUS BUILD
REM =========================
echo [+] Cleaning old build...
rmdir /S /Q "%WORK_DIR%" 2>nul
rmdir /S /Q "%DIST_DIR%" 2>nul

REM =========================
REM BUILD EXE
REM =========================
echo [+] Building EXE...

"%VENV_PY%" -m PyInstaller ^
 --onedir ^
 --console ^
 --noupx ^
 --noconfirm ^
 --hidden-import=requests ^
 --hidden-import=urllib3 ^
 --hidden-import=certifi ^
 --hidden-import=jsonpatch ^
 --hidden-import=jsonpointer ^
 --add-data "%PROJECT_ROOT%\assets;assets" ^
 --add-data "%PROJECT_ROOT%\config;config" ^
 --add-data "%PROJECT_ROOT%\stub;stub" ^
 --add-data "%PROJECT_ROOT%\templates;templates" ^
 --add-data "%PROJECT_ROOT%\villages;villages" ^
 --add-data "%PROJECT_ROOT%\mods;mods" ^
 --paths "%PROJECT_ROOT%" ^
 --workpath "%WORK_DIR%" ^
 --distpath "%DIST_DIR%" ^
 --specpath "%BUILD_DIR%" ^
 --icon="%BUILD_DIR%\icon.ico" ^
 --name %NAME% "%PROJECT_ROOT%\server.py"

if errorlevel 1 (
    echo.
    echo [ERROR] Build failed.
    pause
    exit /b 1
)

REM =========================
REM DONE
REM =========================
echo.
echo =====================================
echo  BUILD SUCCESS
echo  EXE LOCATION:
echo  %DIST_DIR%\%NAME%\%NAME%.exe
echo =====================================
pause
