# Use slim Python base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy your files
COPY main.py .
COPY parser.py .
COPY emailgen.py .
COPY gleam_entry.py .
COPY requirements.txt .
# Install system dependencies for browsers and Selenium
RUN apt-get update && apt-get install -y \
    curl \
    chromium-driver \
    chromium \
    libglib2.0-0 \
    libnss3 \
    libgconf-2-4 \
    libxss1 \
    libasound2 \
    fonts-liberation \
    libappindicator3-1 \
    xdg-utils \
    && apt-get clean

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Environment variable so Selenium can find Chrome
ENV CHROME_BIN=/usr/bin/chromium

# Expose SMTP port
EXPOSE 25

# Start the SMTP server
CMD ["python", "main.py"]