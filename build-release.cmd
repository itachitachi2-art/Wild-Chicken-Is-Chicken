@echo off
setlocal
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0build-release.ps1" -GameDir "%~1"
if errorlevel 1 (
  echo [WildChickenIsChicken] RELEASE BUILD FAILED
  pause
  exit /b 1
)
echo [WildChickenIsChicken] RELEASE ZIP OK
pause
exit /b 0
