@echo off
set "SURSA=C:\Developer\repos-sala\Plan-Sala"
set "DESTINATIE=A:\Obsidian\Rag\Plan-Sala"

rem 0. Se relanseaza din %TEMP%, ca sa nu se stearga pe el insusi daca e rulat din destinatie
if not "%~1"=="--din-temp" (
    copy /y "%~f0" "%TEMP%\copiaza.cmd" >nul
    "%TEMP%\copiaza.cmd" --din-temp
    exit /b
)

rem 1. Goleste continutul destinatiei (fisiere + subfoldere, cu forta)
if exist "%DESTINATIE%" (
    del /f /s /q "%DESTINATIE%\*" >nul 2>&1
    for /d %%D in ("%DESTINATIE%\*") do rd /s /q "%%D"
) else (
    mkdir "%DESTINATIE%"
)

rem 2. Copiaza tot din sursa (inclusiv .git si acest fisier), fara folderul date\
robocopy "%SURSA%" "%DESTINATIE%" /E /XD "%SURSA%\date" /NFL /NDL /NJH /NJS /NC /NS /NP

echo Gata: "%SURSA%" -^> "%DESTINATIE%"
pause
