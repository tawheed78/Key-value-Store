# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 80

# Define environment variables
# ENV REDIS_HOST=localhost \
#     REDIS_PORT=6379 \
#     MONGODB_URI=mongodb+srv://tawheedchilwan55:TiGelbhH31VpQtM0@keyvalue.ygllhpj.mongodb.net/?retryWrites=true&w=majority&appName=keyvalue

# Run app.py when the container launches
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]