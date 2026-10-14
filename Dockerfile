FROM python:3.12-slim
 
WORKDIR /app
 
# Install dependencies in a separate layer for better build caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
 
COPY agent.py api.py ./
 
EXPOSE 8000
 
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]