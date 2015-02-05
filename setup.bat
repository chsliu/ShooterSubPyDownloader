@echo off

echo ============== p2sendfile ============== 
python setup.py py2exe

del *.pyc
del *.bak

REM pause
