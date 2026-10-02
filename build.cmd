@echo off
call "%~dp0WildChickenIsChicken\build.cmd" %*
exit /b %errorlevel%
