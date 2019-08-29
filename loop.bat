:loop
@echo on
py steveBot.py
@echo off
IF EXIST "tmp.txt" ( 
	set /p texte=< tmp.txt
	del tmp.txt
	if "%texte%"==true goto :loop
)
pause