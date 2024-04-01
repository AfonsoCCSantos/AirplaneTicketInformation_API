FROM python

RUN mkdir /database-ranking
COPY . /database-ranking

WORKDIR /database-ranking
RUN pip install -r requirements.txt

EXPOSE 50052
ENTRYPOINT ["python", "database-ranking.py"]