FROM python:3.12-slim
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt
ENV PORT=8000
EXPOSE 8000
CMD ["sh","-c","gunicorn -b 0.0.0.0:${PORT} server:app --workers 2 --threads 4 --timeout 60"]
