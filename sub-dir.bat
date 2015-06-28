@echo off
python %~dp0\ShooterSubAll.py %1 %~dp0\ignore.txt avi mp4 mkv

rem pause

C:\Windows\System32\timeout.exe 10
