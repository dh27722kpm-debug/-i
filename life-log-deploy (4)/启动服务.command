#!/bin/bash
cd "$(dirname "$0")" || exit 1

# 如果是双击打开的，给个提示
clear
echo "========================================================"
echo "  🐱 生活记录台 · 一键启动"
echo "========================================================"
echo

if command -v python3 >/dev/null 2>&1; then
  python3 start-server.py
elif command -v python >/dev/null 2>&1; then
  python start-server.py
else
  echo "❌ 没有检测到 Python。"
  echo
  echo "请先安装 Python（brew install python 或 python.org 下载）："
  echo "  https://www.python.org/downloads/"
  echo
  echo "或者不用本工具：把整个文件夹拖到 https://app.netlify.com/drop"
  echo
  read -r -p "按回车键退出…" _
  exit 1
fi

echo
read -r -p "按回车键退出…" _
