FROM python:3.7.8-slim

# remember to expose the port your app'll be exposed on.
EXPOSE 8080

RUN pip install -U pip

COPY requirements.txt app/requirements.txt
RUN pip install -r app/requirements.txt

# copy into a directory of its own (so it isn't in the toplevel dir)
COPY . /app
WORKDIR /app

# Configurar Streamlit para deshabilitar health checks en Cloud Run
ENV STREAMLIT_SERVER_HEADLESS=true
ENV STREAMLIT_SERVER_ENABLE_CORS=false
ENV STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

# Hacer ejecutable el health check
RUN chmod +x health_check.py

# Script de inicio que ejecuta ambos servicios
RUN echo '#!/bin/bash\n\
echo "Starting health check server..."\n\
python health_check.py &\n\
echo "Starting Streamlit app..."\n\
streamlit run app.py --server.port=$PORT --server.address=0.0.0.0 --server.headless=true --server.enableCORS=false\n\
' > start.sh && chmod +x start.sh

ENTRYPOINT ["./start.sh"]