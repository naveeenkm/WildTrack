@echo off
@REM setlocal

@REM :: Set the path to your XAMPP installation
@REM set "xamppPath=C:\xampp1"

@REM :: Stop WAMP stack services if they are running
@REM echo Stopping WAMP services...
@REM net stop wampstackapache >nul 2>&1
@REM net stop wampstackmariadb >nul 2>&1

@REM :: Start Apache and MySQL from XAMPP
@REM cd /d "%xamppPath%"
@REM echo Starting Apache and MySQL...
@REM start /B apache_start.bat
@REM start /B mysql_start.bat

@REM :: Wait for a few seconds to ensure services start
@REM timeout /t 5

:: Change to the Scripts folder and activate the virtual environment
cd /d "C:\Users\Naveen K M\Documents\Project\iot\env\Scripts"
call activate

:: Change to the Django project directory
cd /d "C:\Users\Naveen K M\Documents\Project\iot\iot_tracker"

:: Start the Django server and redirect output



