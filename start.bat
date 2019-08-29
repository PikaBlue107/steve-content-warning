setlocal EnableDelayedExpansion
:loop
@echo on
py steveBot.py
IF EXIST "tmp.txt" ( 
	set /p bool=<tmp.txt
	del tmp.txt
	if "!bool!"=="true" goto :loop
)
pause