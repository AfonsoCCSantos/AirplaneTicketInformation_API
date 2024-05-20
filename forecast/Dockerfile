# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Install Java (OpenJDK)
RUN apt update
RUN apt install -y openjdk-17-jdk
RUN apt clean
RUN rm -rf /var/lib/apt/lists/*

# Set JAVA_HOME environment variable
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
ENV PATH=$JAVA_HOME/bin:$PATH

# Create and set the working directory
RUN mkdir /forecast
COPY . /forecast
WORKDIR /forecast
COPY ml_models/ticket_price_pred /forecast/ml_models/ticket_price_pred
COPY ml_models/flightDateModel /forecast/ml_models/flightDateModel
COPY ml_models/startingAirportModel /forecast/ml_models/startingAirportModel
COPY ml_models/destinationAirportModel /forecast/ml_models/destinationAirportModel

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port on which the app will run
EXPOSE 8080

# Set environment variable for Flask app
ENV FLASK_APP=forecast.py

# Define the entry point for the container to run the Flask app
ENTRYPOINT ["flask", "run", "--host=0.0.0.0", "--port=8080"]