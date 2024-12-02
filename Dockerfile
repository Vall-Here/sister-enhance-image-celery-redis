# # Menggunakan Python sebagai base image
# FROM python:3.9-slim

# # Menentukan working directory
# WORKDIR /app

# RUN apt-get update && apt-get install -y libgl1 libglib2.0-0 libsm6 libxrender1 libxext6
# # Menyalin requirements.txt dan menginstall dependencies
# COPY api-server/requirements.txt /app/
# RUN pip install -r requirements.txt

# RUN chmod -R 777 /tmp

# # Menyalin seluruh kode aplikasi ke dalam container
# COPY . /app/

# # Menjalankan Flask API Server
# CMD ["python", "api-server/app.py"]


# Menggunakan Python sebagai base image
FROM python:3.9-slim

# Menentukan working directory
WORKDIR /app

# Install dependencies sistem
RUN apt-get update && apt-get install -y libgl1 libglib2.0-0 libsm6 libxrender1 libxext6

# Menyalin requirements.txt dan menginstall dependencies
COPY api-server/requirements.txt /app/
RUN pip install -r requirements.txt

# Menyalin seluruh kode aplikasi ke dalam container
COPY . /app/

# Menentukan perintah default
CMD ["python", "api-server/app.py"]
