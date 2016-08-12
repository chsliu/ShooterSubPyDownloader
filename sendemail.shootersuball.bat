@echo off
set path=%path%;%~dp0\..\bin

REM =================================
set MyDate=
for /f "skip=1" %%x in ('wmic os get localdatetime') do if not defined MyDate set MyDate=%%x
set TODAY=%MyDate:~0,4%-%MyDate:~4,2%-%MyDate:~6,2%
set MONTH=%MyDate:~0,4%-%MyDate:~4,2%
REM =================================
set T=%1
set T=%T::=%
set T=%T:\\=%
set T=%T:\=-%

set LOG1=%temp%\%~n0-%T%-%TODAY%-summary.txt
set LOG2=%temp%\%~n0-%T%-%TODAY%.txt
set TXT1=%temp%\%~n0.txt

REM =================================
python %~dp0\ShooterSubAll.py %1 %~dp0\ignore.txt avi mp4 mkv >>%LOG2%

rem pause

REM =================================
echo List of newly download subtitles:	 >%LOG1%
findstr /C:".zh" %LOG2%				>>%LOG1%
rem findstr /C:"Writing:" %LOG2%		>>%LOG1%
rem findstr /C:"Found for:" %LOG2%		>>%LOG1%
rem findstr /C:"NONE:" %LOG2%			>>%LOG1%

REM =================================
copy %0 %TXT1% >nul

for /f %%a in ('type "%LOG1%"^|find "" /v /c') do set /a cnt=%%a
rem for /f %%a in ('type "%LOG1%"^|find "Found for:" /c') do set /a cnt=%%a

if %cnt% gtr 1 (
  rem echo %LOG1% has %cnt% lines
  echo %1 sending report...
  sendemail -s msa.hinet.net -f egreta.su@msa.hinet.net -t chsliu@gmail.com -u [FileBot] %~n0 %1 -m %0 %1 -a %LOG1% %LOG2% %TXT1%
) else (
  rem echo %LOG1% only has %cnt% lines
  echo %1 has no report.
)

del %LOG1% %LOG2% %TXT1%
