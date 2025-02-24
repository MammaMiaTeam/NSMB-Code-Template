@echo off
setlocal

rem Possible python aliases
set INTERPRETERS=py "py -3" python py3 python3

set SCRIPT=convert_sdk.py

for %%I in (%INTERPRETERS%) do (
    where %%I >nul 2>nul
    if not errorlevel 1 (
        echo Running with: %%I
        %%I %SCRIPT%
	pause
        exit /b
    )
)

echo Error: Python is not installed.
pause
exit /b 1
