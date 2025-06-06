# @REM @echo off

# @REM :: Change to the Scripts folder and activate the virtual environment
# @REM cd /d "C:\Users\Naveen K M\Documents\Project\iot\env\Scripts"
# @REM call activate

# @REM :: Change to the Django project directory
# @REM cd /d "C:\Users\Naveen K M\Documents\Project\iot\iot_tracker"
# Change to the Scripts folder and activate the virtual environment
Set-Location "C:\Users\Naveen K M\Documents\Project\iot\env\Scripts"

# Activate the virtual environment
.\Activate.ps1

# Change to the Django project directory
Set-Location "C:\Users\Naveen K M\Documents\Project\iot\iot_tracker"
python manage.py runserver
