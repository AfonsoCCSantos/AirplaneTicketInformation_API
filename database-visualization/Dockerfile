FROM python

RUN mkdir /database-visualization
COPY . /database-visualization

WORKDIR /database-visualization
RUN pip install -r requirements.txt

EXPOSE 50051
ENTRYPOINT ["python", "database-visualization.py"]