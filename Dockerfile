# 1. Use an official Python runtime as a parent image
FROM python:3.10-slim

# 2. Set the working directory in the container
WORKDIR /app

# 3. Copy requirements file to the working directory
COPY requirements.txt /app/requirements.txt

# 4. Install dependencies
RUN pip install --no-cache-dir -r /app/requirements.txt

# 5. Copy the application code to the container
COPY . /app

# 6. Expose the port that the app runs on
EXPOSE 8081

# 7. Command to run the FastAPI application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8081", "--reload"]
