FROM python:3.7.8-slim

# Instalar Nginx
RUN apt-get update && apt-get install -y nginx && rm -rf /var/lib/apt/lists/*

# Instalar dependencias de Python
RUN pip install -U pip
COPY requirements.txt app/requirements.txt
RUN pip install -r app/requirements.txt

# Copiar código de la app y configuración de Nginx
COPY . /app
WORKDIR /app
COPY nginx.conf /etc/nginx/nginx.conf

# Exponer el puerto de Nginx
EXPOSE 8080

# Configurar Streamlit para producción
ENV STREAMLIT_SERVER_HEADLESS=true
ENV STREAMLIT_SERVER_ENABLE_CORS=false
ENV STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

# Script de inicio: Streamlit en background, Nginx en foreground
CMD streamlit run app.py --server.port=8501 --server.address=0.0.0.0 & nginx -g 'daemon off;'