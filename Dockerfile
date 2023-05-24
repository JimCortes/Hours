FROM python:3.9

WORKDIR /app
ENV TZ=America/Vancouver
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .



CMD ["streamlit", "run","1_\t🏡Home.py", "--server.port=8501"]
