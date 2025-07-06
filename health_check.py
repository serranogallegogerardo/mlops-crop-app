#!/usr/bin/env python3
"""
Health check endpoint for Streamlit on Cloud Run
This file runs in parallel with the main application
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
            # Simple health check
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'ok')
        elif self.path == '/':
            # Redirect to Streamlit
            self.send_response(302)
            self.send_header('Location', '/')
            self.end_headers()
        else:
            # For other routes, try to redirect to Streamlit
            try:
                # Check if Streamlit is responding
                response = requests.get(f'http://localhost:8080{self.path}', timeout=5)
                self.send_response(response.status_code)
                for header, value in response.headers.items():
                    if header.lower() not in ['transfer-encoding', 'connection']:
                        self.send_header(header, value)
                self.end_headers()
                self.wfile.write(response.content)
            except:
                # If Streamlit doesn't respond, return 404
                self.send_response(404)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write(b'Not Found')
    
    def log_message(self, format, *args):
        # Silence health check logs to avoid spam
        pass

def start_health_check_server():
    """Start health check server on port 8080"""
    try:
        port = 8080
        server = HTTPServer(('0.0.0.0', port), HealthCheckHandler)
        print(f"Health check server started on port {port}")
        server.serve_forever()
    except OSError as e:
        print(f"Could not start health check server: {e}")

if __name__ == "__main__":
    start_health_check_server() 