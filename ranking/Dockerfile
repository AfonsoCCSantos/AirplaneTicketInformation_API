FROM python

RUN mkdir /ranking
COPY . /ranking

WORKDIR /ranking
RUN pip install -r requirements.txt

EXPOSE 8082
ENV FLASK_APP=ranking.py
ENTRYPOINT [ "flask", "run", "--host=0.0.0.0", "--port=8082"]