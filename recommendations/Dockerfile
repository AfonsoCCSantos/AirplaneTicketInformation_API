FROM python:3.13-slim

RUN apt update
RUN apt install -y openjdk-17-jdk
RUN apt clean
RUN rm -rf /var/lib/apt/lists/*

# Set JAVA_HOME environment variable
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
ENV PATH=$JAVA_HOME/bin:$PATH

RUN mkdir /recommendations
COPY . /recommendations
WORKDIR /recommendations
COPY ml_models/ticket_price_pred /recommendations/ml_models/ticket_price_pred
COPY ml_models/airline_price_pred /recommendations/ml_models/airline_price_pred
COPY ml_models/flightDateModel /recommendations/ml_models/flightDateModel
COPY ml_models/startingAirportModel /recommendations/ml_models/startingAirportModel
COPY ml_models/destinationAirportModel /recommendations/ml_models/destinationAirportModel

RUN pip install -r requirements.txt

EXPOSE 8083

ENV FLASK_APP=recommendations.py

ENTRYPOINT ["flask", "run", "--host=0.0.0.0", "--port=8083"]