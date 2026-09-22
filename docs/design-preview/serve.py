#!/usr/bin/env python3
"""本地预览服务：发送 no-store 头，避免静态资源被浏览器缓存。"""
import http.server
import socketserver

PORT = 8788


class NoCacheHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Cache-Control", "no-store, must-revalidate")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        super().end_headers()


if __name__ == "__main__":
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), NoCacheHandler) as httpd:
        print(f"serving on http://localhost:{PORT} (no-store)")
        httpd.serve_forever()
