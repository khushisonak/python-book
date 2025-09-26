@echo off
REM Get the local IPv4 address (excluding loopback and virtual adapters)
for /f "tokens=2 delims=:" %%f in ('ipconfig ^| findstr /R /C:"IPv4.*"') do (
    set ip=%%f
)
REM Remove leading space
set ip=%ip:~1%
echo Serving HTTP on %ip% port 50500 (http://%ip%:50500/)
python -m http.server 50500
pause