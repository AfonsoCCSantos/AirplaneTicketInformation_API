FROM python

RUN mkdir /visualization
COPY . /visualization

WORKDIR /visualization
RUN pip install -r requirements.txt

EXPOSE 8084
ENV FLASK_APP=visualization.py
ENTRYPOINT [ "flask", "run", "-p", "8084"]