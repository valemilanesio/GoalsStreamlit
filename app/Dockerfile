# Imagen base oficial de Streamlit
FROM python:3.11-slim

# Evitar errores de stdin para Streamlit y no almacenar caché pip
ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# Setear el directorio de trabajo
WORKDIR .

# Copiar los archivos necesarios
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copiar el resto del contenido
COPY . .

# Exponer el puerto 8501 (por defecto en Streamlit)
EXPOSE 8501

# Comando para correr la app
CMD ["streamlit", "run", "app.py", "--server.enableCORS=false"]
