# Use official Python base image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy required files and folders
COPY database/ml_controller.py /app/
COPY database/utils /app/utils/
COPY database/model_evaluation /app/model_evaluation/
COPY database/requirements.txt /app/

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    net-tools \
    iputils-ping \
    && apt-get clean

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt && \
    pip install eventlet==0.30.2

# Expose the Ryu controller port
EXPOSE 6633

# Run the Ryu controller
CMD ["ryu-manager", "/app/ml_controller.py"]

