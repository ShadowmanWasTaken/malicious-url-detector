# Base Image: Start with a lightweight version of Python 3.9
FROM python:3.9-slim

# Work Directory: Create a folder inside the container
WORKDIR /app

# Copy Requirements: Move the requirements file into the container
COPY requirements.txt .

# Install Dependencies: Run pip inside the container
# --no-cache-dir keeps the image small
RUN pip install --no-cache-dir -r requirements.txt

# Copy Code: Move all your source code into the container
COPY . .

# Expose Port: Tell Docker we are listening on port 8000
EXPOSE 8000

# Run Command: The command to start the API when the container starts
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]