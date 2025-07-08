FROM python:3.7.8-slim

# Install Nginx
RUN apt-get update && apt-get install -y nginx && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install -U pip
COPY requirements.txt app/requirements.txt
RUN pip install -r app/requirements.txt

# Copy app code and Nginx configuration
COPY . /app
WORKDIR /app
COPY nginx.conf /etc/nginx/nginx.conf

# Expose Nginx port
EXPOSE 8080

# Configure Streamlit for production (these can be overridden with environment variables)
ENV STREAMLIT_SERVER_HEADLESS=true
ENV STREAMLIT_SERVER_ENABLE_CORS=false
ENV STREAMLIT_BROWSER_GATHER_USAGE_STATS=false
ENV STREAMLIT_LOGGER_LEVEL=error
ENV STREAMLIT_SERVER_ENABLE_STATIC_SERVING=true
ENV STREAMLIT_SERVER_ENABLE_XSRF_PROTECTION=false
ENV STREAMLIT_SERVER_ENABLE_WEBSOCKET_COMPRESSION=false

# Startup script: Streamlit in background, Nginx in foreground
CMD streamlit run app.py --server.port=8501 --server.address=0.0.0.0 --logger.level=error & nginx -g 'daemon off;'