@echo off

set ROOT=%~dp0

:main
if [%1]==[] goto :EOF

start call %ROOT%\sub-file.bat "%1" ^&^& exit

sleep 1

shift

goto :main
