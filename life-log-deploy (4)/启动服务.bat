@echo off
chcp 65001 >nul
title 生活记录台 - 局域网服务器
cd /d "%~dp0"

echo ========================================================
echo   🐱 生活记录台 · 一键启动
echo ========================================================
echo.

where python >nul 2>nul
if %errorlevel%==0 (
    python start-server.py
    goto :end
)
where py >nul 2>nul
if %errorlevel%==0 (
    py -3 start-server.py
    goto :end
)
where python3 >nul 2>nul
if %errorlevel%==0 (
    python3 start-server.py
    goto :end
)

echo ❌ 没有检测到 Python。
echo.
echo 请先安装 Python：
echo    1. 打开 https://www.python.org/downloads/
echo    2. 下载安装，勾选 "Add Python to PATH"
echo    3. 装完后再双击本文件
echo.
echo 或者你也可以不用本工具：
echo    · 把整个文件夹拖到 https://app.netlify.com/drop 即可获得永久网址
echo.
pause
exit /b 1

:end
echo.
pause
