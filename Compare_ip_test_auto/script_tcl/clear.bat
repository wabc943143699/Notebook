@echo off
setlocal

REM 使用PowerShell来删除目录及其内容
powershell -Command "Remove-Item -Recurse .\.Xil -Force"
powershell -Command "Remove-Item -Recurse ./my_project_dir -Force"

REM 使用PowerShell来删除文件
powershell -Command "Remove-Item -Force ./vivado.jou"
powershell -Command "Remove-Item -Force ./vivado.log"

endlocal
pause