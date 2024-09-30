FROM python:3.13.0rc2-slim

RUN apt update
RUN apt install -y openjdk-17-jdk
RUN apt clean
RUN rm -rf /var/lib/apt/lists/*

# Set JAVA_HOME environment variable
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
ENV PATH=$JAVA_HOME/bin:$PATH

RUN mkdir /forecast
COPY . /forecast
WORKDIR /forecast
COPY ml_models/ticket_price_pred /forecast/ml_models/ticket_price_pred
COPY ml_models/flightDateModel /forecast/ml_models/flightDateModel
COPY ml_models/startingAirportModel /forecast/ml_models/startingAirportModel
COPY ml_models/destinationAirportModel /forecast/ml_models/destinationAirportModel

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8080

ENV FLASK_APP=forecast.py

ENTRYPOINT ["flask", "run", "--host=0.0.0.0", "--port=8080"]