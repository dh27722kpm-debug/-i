#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐱 生活记录台 · 一键启动

用法（解压后在此文件夹运行）：
    python3 start-server.py         # 或双击 启动服务.command / start-server.bat

效果：
    1. 在本机启动一个小服务器，把这个应用暴露到局域网
    2. 自动生成二维码图片 start-qrcode.png
    3. 终端打印手机可访问的网址
    4. 手机扫码 → 打开页面 → 「添加到主屏幕」即可像 App 一样用

注意：电脑关机或退出本程序后，手机上的图标仍可打开（页面已缓存），
      但要重新联网加载数据需再次运行本程序。要长期使用请看「部署指南.md」。
"""
import http.server
import socket
import os
import sys
import threading
import webbrowser
import time

PORT = 8848
ROOT = os.path.dirname(os.path.abspath(__file__))
QR_FILE = os.path.join(ROOT, "start-qrcode.png")


def get_lan_ip():
    """取本机在局域网中的 IP（手机能访问的那个）"""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]
    except Exception:
        try:
            return socket.gethostbyname(socket.gethostname())
        except Exception:
            return "127.0.0.1"
    finally:
        s.close()


def make_qr(url):
    """生成二维码图片"""
    try:
        import qrcode
        img = qrcode.make(url, box_size=10, border=2)
        img.save(QR_FILE)
        return True
    except Exception as e:
        print("  （二维码生成失败：%s，可手动复制上面的网址）" % e)
        return False


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **kw):
        super().__init__(*a, directory=ROOT, **kw)

    def log_message(self, fmt, *args):
        pass  # 静默日志，保持终端干净

    def end_headers(self):
        # 禁用缓存，保证改完代码刷新就能看到最新版本
        self.send_header("Cache-Control", "no-store, no-cache, must-revalidate")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        super().end_headers()

    def do_GET(self):
        # install.html 里注入真实的局域网地址，手机打开就显示正确网址
        if self.path.split("?")[0].endswith("/install.html"):
            try:
                with open(os.path.join(ROOT, "install.html"), "r", encoding="utf-8") as f:
                    html = f.read()
                ip = get_lan_ip()
                url = f"http://{ip}:{PORT}/index.html"
                html = html.replace("__APP_URL__", url)
                html = html.replace(
                    "qr.src = 'start-qrcode.png';",
                    "qr.src = 'start-qrcode.png?v=' + Date.now();"
                )
                data = html.encode("utf-8")
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", str(len(data)))
                self.end_headers()
                self.wfile.write(data)
                return
            except Exception:
                pass
        return super().do_GET()


def main():
    if not os.path.exists(os.path.join(ROOT, "index.html")):
        print("❌ 没找到 index.html，请先解压 zip 再运行本程序。")
        sys.exit(1)

    ip = get_lan_ip()
    url = f"http://{ip}:{PORT}/index.html"

    print("=" * 56)
    print("  🐱 生活记录台 · 已启动")
    print("=" * 56)
    print(f"  本机访问：  http://localhost:{PORT}/index.html")
    print(f"  手机访问：  {url}")
    print()
    print("  📱 手机操作：")
    print("     1. 手机和电脑连同一个 WiFi")
    print("     2. 扫下方二维码，或手动输入上面的网址")
    print("     3. iPhone：Safari 打开 → 底部「分享」→「添加到主屏幕」")
    print("     4. 安卓：Chrome 打开 → 右上角「⋮」→「添加到主屏幕」")
    print()
    print("  ⚠️  保持本窗口开着；按 Ctrl+C 退出")
    print("=" * 56, flush=True)

    if make_qr(url):
        print(f"  🖼  二维码已保存：{QR_FILE}")
        # 在终端里用字符画个简易二维码，方便没图片时扫
        try:
            import qrcode
            qr = qrcode.QRCode(border=1)
            qr.add_data(url)
            qr.make(fit=True)
            print()
            for line in qr.get_string().splitlines():
                print("     " + line)
            print()
        except Exception:
            pass

    srv = http.server.ThreadingHTTPServer(("0.0.0.0", PORT), Handler)
    try:
        # 打开本机浏览器（服务器/无图形环境会失败，静默忽略）
        def _open():
            try:
                if not os.environ.get("DISPLAY") and os.name != "nt":
                    return          # 无图形界面就跳过
                webbrowser.open(f"http://localhost:{PORT}/index.html")
            except Exception:
                pass
        threading.Timer(1.2, _open).start()
        srv.serve_forever()
    except KeyboardInterrupt:
        print("\n  👋 已停止服务")
    finally:
        srv.server_close()


if __name__ == "__main__":
    main()
