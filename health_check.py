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
import requests
from urllib.parse import urlparse

class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/healthz':
            # Health check simple
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'ok')
        elif self.path == '/':
            # Redirigir a Streamlit
            self.send_response(302)
            self.send_header('Location', '/')
            self.end_headers()
        else:
            # Para otras rutas, intentar redirigir a Streamlit
            try:
                # Verificar si Streamlit está respondiendo
                response = requests.get(f'http://localhost:8080{self.path}', timeout=5)
                self.send_response(response.status_code)
                for header, value in response.headers.items():
                    if header.lower() not in ['transfer-encoding', 'connection']:
                        self.send_header(header, value)
                self.end_headers()
                self.wfile.write(response.content)
            except:
                # Si Streamlit no responde, devolver 404
                self.send_response(404)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write(b'Not Found')
    
    def log_message(self, format, *args):
        # Silenciar logs del health check para evitar spam
        pass

def start_health_check_server():
    """Iniciar servidor de health check en puerto 8080"""
    try:
        port = 8080
        server = HTTPServer(('0.0.0.0', port), HealthCheckHandler)
        print(f"Health check server started on port {port}")
        server.serve_forever()
    except OSError as e:
        print(f"Could not start health check server: {e}")

if __name__ == "__main__":
    start_health_check_server() 