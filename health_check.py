#!/usr/bin/env python3
"""
Health check endpoint para Streamlit en Cloud Run
Este archivo se ejecuta en paralelo con la aplicación principal
"""

import os
import time
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
import socket

class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/healthz':
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'ok')
        elif self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'Streamlit App is running')
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'Not Found')
    
    def log_message(self, format, *args):
        # Silenciar logs del health check
        pass

def start_health_check_server():
    """Iniciar servidor de health check en puerto 8081"""
    try:
        # Intentar puerto 8081 primero
        port = 8081
        server = HTTPServer(('0.0.0.0', port), HealthCheckHandler)
        print(f"Health check server started on port {port}")
        server.serve_forever()
    except OSError:
        # Si 8081 está ocupado, intentar 8082
        try:
            port = 8082
            server = HTTPServer(('0.0.0.0', port), HealthCheckHandler)
            print(f"Health check server started on port {port}")
            server.serve_forever()
        except OSError:
            print("Could not start health check server")

if __name__ == "__main__":
    start_health_check_server() 