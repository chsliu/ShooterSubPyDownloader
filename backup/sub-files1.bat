rem @echo off
setlocal EnableDelayedExpansion
set app=%~dp0\ShooterSubAll.py

rem echo all:  %*
rem pause

call :lastarg %*
rem echo all:  %*
rem echo last: %ARG_LAST%
rem pause

if not [%ARG_LAST%] == ["max"] goto :StartAgain
rem pause

if [%1]==[] goto :EOF

:loop
if [%1]==[] goto :Exit
if [%1]==[max] goto :Exit

rem echo python %~dp0\ShooterSubAll.py %1
rem pause
python %app% %1

shift
goto :loop

goto :EOF

:lastarg
set ARG_LAST="%~1"
shift
if not [%~1]==[] goto lastarg

goto :EOF

:StartAgain
echo :StartAgain
REM pause
set tempArgs=%*
set tempArgsEscaped=%tempArgs:&=^&%
echo start /MAX cmd /c %0 %tempArgsEscaped% max
pause
start /MAX cmd /c %0 %tempArgsEscaped% max
goto :EOF

:Exit
pause
