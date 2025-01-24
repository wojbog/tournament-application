# Use the official Python image as the base image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt into the container
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project into the container
COPY . .

# Expose the port the app runs on (Flask defaults to port 5000)
EXPOSE 5000

# Set the command to run the Flask app
# Assumes your app's entry point is app.py and uses the default Flask port
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]