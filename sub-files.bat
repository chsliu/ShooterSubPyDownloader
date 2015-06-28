rem @echo off
rem setlocal EnableDelayedExpansion
set app=%~dp0\ShooterSubAll.py

rem call :EscapeAmpersands %*
call :lastarg %RET%
if not [%RET%] == ["max"] goto :StartAgain

if [%1]==[] goto :EOF

:loop
if [%1]==[] goto :Exit
if [%1]==[max] goto :Exit

call :UnescapeAmpersands %1
python %app% %RET%

shift
goto :loop

goto :EOF

:EscapeAmpersands
set tempArgs=%*
set RET=%tempArgs:&=^&%

goto :EOF

:UnescapeAmpersands
set tempArg1=%*
set RET=%tempArg1:^&=&%

goto :EOF


:lastarg
set RET=%1
shift
if not [%1]==[] goto lastarg

goto :EOF

:StartAgain
call :EscapeAmpersands %*
rem echo start /MAX cmd /c %0 %RET% max
pause
start /MAX cmd /c %0 %RET% max

goto :EOF



:Exit
pause
