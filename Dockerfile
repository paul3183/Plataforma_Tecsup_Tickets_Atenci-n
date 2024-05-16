# Usa una imagen de Python específica
FROM python:3.12.0

# Copia los archivos de requerimientos e instala las dependencias
COPY requerimientos.txt .
RUN pip install --no-cache-dir -r requerimientos.txt
RUN pip install uwsgi

# Copia el resto de la aplicación
COPY . .

# Comando para iniciar uWSGI con la configuración
CMD ["uwsgi", "--ini", "uwsgi.ini"]
