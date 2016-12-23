@echo off

REM =================================
goto :main

REM =================================
:EscapeAmpersands
set tempArgs=%*
set RET=%tempArgs:&=^&%

exit /b

:UnescapeAmpersands
set tempArg1=%*
set RET=%tempArg1:^&=&%

exit /b

:lastarg
set RET=%1

echo RET=%RET%

shift
if not [%1]==[] goto lastarg

exit /b

:StartAgain
echo :StartAgain
REM call :EscapeAmpersands %*
rem echo start /MAX cmd /c %0 %RET% max
REM pause
start /MAX cmd /c %0 %RET% max

exit /b

:Exit
pause
goto :EOF

REM =================================
:main

REM =================================
rem setlocal EnableDelayedExpansion
set app=%~dp0\ShooterSubAll.py

call :EscapeAmpersands %*
call :lastarg %RET%

echo RET=%RET%
pause

if not [%RET%] == ["max"] goto :StartAgain

if [%1]==[] goto :EOF

:loop
if [%1]==[] goto :Exit
if [%1]==[max] goto :Exit

call :UnescapeAmpersands %1
python %app% %RET%

shift
goto :loop

