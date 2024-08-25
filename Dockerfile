# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /fantasy-football-bot

### TO DO ###
# put env variables in compose.yml for security

# Set environment variables
ENV DISCORD_TOKEN=""
ENV CONSUMER_KEY=""
ENV CONSUMER_SECRET=""
ENV REFRESH_TOKEN=""

# Copy the requirements file into the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the bot directory into the container
COPY ./bot ./bot

# Specify the command
CMD ["python", "./bot/main.py"]