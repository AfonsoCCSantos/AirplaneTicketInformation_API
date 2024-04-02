FROM python

RUN mkdir /forecast
COPY . /forecast

WORKDIR /forecast
RUN pip install -r requirements.txt

EXPOSE 8080
ENV FLASK_APP=forecast.py
ENTRYPOINT [ "flask", "run", "--host=0.0.0.0", "--port=8080"]