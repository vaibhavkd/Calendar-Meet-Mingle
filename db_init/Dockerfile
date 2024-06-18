# Use the official Python image from the Docker Hub
FROM python:3.9

# Set the working directory
WORKDIR /scripts

# Copy the requirements file into the container
COPY requirements.txt .

# Install the required packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Command to run your Python script
# ENTRYPOINT ["python", "/scripts/run_sql_script.py"]
