# Use a lightweight Python Linux image
FROM python:3.11-slim

# Install the actual Tesseract OCR engine and required image libraries
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    && rm -rf /var/lib/apt/lists/*

# Set up the working directory
WORKDIR /app

# Copy your backend requirements and install them
COPY requirements-render.txt .
RUN pip install --no-cache-dir -r requirements-render.txt

# Copy the rest of your application code
COPY . .

# Run the FastAPI backend using Render's dynamic port
CMD uvicorn app:app --host 0.0.0.0 --port $PORT
